"""
QuantumDice – demo (v0.1)
========================

Cel:
- Mamy 5 funkcji (strategii) rozwiązujących ten sam problem.
- QuantumDice wybiera tę, która ma największą "jakość decyzji" przy rozsądnym koszcie.

Problem demo:
- Minimalizacja funkcji f(x) na przedziale [a, b].

5 strategii:
1) random_search
2) hill_climb
3) simulated_annealing
4) golden_section_search  (bardzo mocna na unimodalne funkcje)
5) grid_search

Uruchomienie:
    python quantumdice_demo.py

Wynik:
- Ranking strategii z metrykami + wybrana strategia.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple
import math
import random
import statistics
import time


# -----------------------------
# 1) Problem (funkcja celu)
# -----------------------------

def objective(x: float) -> float:
    """
    Funkcja celu: mieszanka 'ładnej doliny' + lokalne zakłócenia.
    Ma sens w demo, bo część metod może się nabrać na lokalne minima.

    Minimum globalne jest w praktyce do znalezienia, ale nie jest "za łatwe".
    """
    # bazowa dolina
    base = (x - 1.7) ** 2
    # drobne fale (lokalne minima)
    ripple = 0.15 * math.sin(8 * x) + 0.08 * math.sin(22 * x)
    return base + ripple


# -----------------------------
# 2) Struktury danych
# -----------------------------

@dataclass(frozen=True)
class SolveResult:
    """
    Wynik pojedynczego uruchomienia (1 rollout).
    """
    x_best: float
    f_best: float
    evaluations: int
    duration_ms: float


@dataclass
class StrategyStats:
    """
    Agregacja wielu rolloutów danej strategii.
    """
    name: str
    results: List[SolveResult]

    def summary(self) -> Dict[str, float]:
        f_vals = [r.f_best for r in self.results]
        evals = [r.evaluations for r in self.results]
        durs = [r.duration_ms for r in self.results]

        return {
            "f_best_mean": statistics.mean(f_vals),
            "f_best_min": min(f_vals),
            "f_best_std": statistics.pstdev(f_vals) if len(f_vals) > 1 else 0.0,
            "eval_mean": statistics.mean(evals),
            "dur_ms_mean": statistics.mean(durs),
        }


# -----------------------------
# 3) Pięć strategii (funkcji)
# -----------------------------

def random_search(f: Callable[[float], float], a: float, b: float, budget: int, rng: random.Random) -> SolveResult:
    """
    Strategia 1: Random Search
    - najprostsza: losujemy punkty i bierzemy najlepszy
    - plus: nie grzęźnie w lokalnych minimach (bo skacze)
    - minus: może być mało efektywna w gładkich problemach
    """
    start = time.perf_counter()
    x_best = None
    f_best = float("inf")
    for _ in range(budget):
        x = rng.uniform(a, b)
        fx = f(x)
        if fx < f_best:
            f_best = fx
            x_best = x
    dur_ms = (time.perf_counter() - start) * 1000
    return SolveResult(x_best=x_best, f_best=f_best, evaluations=budget, duration_ms=dur_ms)


def grid_search(f: Callable[[float], float], a: float, b: float, budget: int, rng: random.Random) -> SolveResult:
    """
    Strategia 2: Grid Search (siatka)
    - deterministycznie skanuje przedział w równych krokach
    - plus: stabilna (mała wariancja)
    - minus: nie adaptuje się; jak budżet mały, może "minąć" dolinę
    """
    start = time.perf_counter()
    if budget < 2:
        budget = 2
    step = (b - a) / (budget - 1)
    x_best = a
    f_best = f(a)
    evals = 1

    for i in range(1, budget):
        x = a + i * step
        fx = f(x)
        evals += 1
        if fx < f_best:
            f_best = fx
            x_best = x

    dur_ms = (time.perf_counter() - start) * 1000
    return SolveResult(x_best=x_best, f_best=f_best, evaluations=evals, duration_ms=dur_ms)


def hill_climb(f: Callable[[float], float], a: float, b: float, budget: int, rng: random.Random) -> SolveResult:
    """
    Strategia 3: Hill Climbing (w praktyce: gradient-free local search)
    - start w losowym punkcie, potem lokalne kroki +/- step, step maleje
    - plus: szybko poprawia wynik, jeśli start jest "sensowny"
    - minus: lubi utknąć w lokalnym minimum
    """
    start = time.perf_counter()

    x = rng.uniform(a, b)
    fx = f(x)
    evals = 1

    step = (b - a) * 0.1  # startowy rozmiar kroku
    x_best, f_best = x, fx

    # każda iteracja zużywa 1 lub 2 ewaluacje, więc pilnujemy budżetu
    while evals < budget and step > 1e-9:
        # spróbuj w lewo i w prawo
        candidates = []
        if evals < budget:
            xl = max(a, x - step)
            fl = f(xl); evals += 1
            candidates.append((xl, fl))
        if evals < budget:
            xr = min(b, x + step)
            fr = f(xr); evals += 1
            candidates.append((xr, fr))

        # wybierz najlepszy ruch, jeśli poprawia
        x_new, f_new = min(candidates, key=lambda t: t[1])
        if f_new < fx:
            x, fx = x_new, f_new
            if fx < f_best:
                x_best, f_best = x, fx
        else:
            # brak poprawy: zmniejszamy krok (schodzimy do drobniejszej skali)
            step *= 0.5

    dur_ms = (time.perf_counter() - start) * 1000
    return SolveResult(x_best=x_best, f_best=f_best, evaluations=evals, duration_ms=dur_ms)


def simulated_annealing(f: Callable[[float], float], a: float, b: float, budget: int, rng: random.Random) -> SolveResult:
    """
    Strategia 4: Simulated Annealing
    - lokalne kroki, ale czasem akceptujemy gorszy wynik (ucieczka z pułapek)
    - temperatura maleje => z czasem stajemy się bardziej "zachowawczy"
    """
    start = time.perf_counter()

    x = rng.uniform(a, b)
    fx = f(x)
    evals = 1

    x_best, f_best = x, fx

    # parametry annealingu (proste, ale działające w demo)
    T0 = 1.0
    step0 = (b - a) * 0.15

    k = 0
    while evals < budget:
        # temperatura i krok maleją z iteracją
        t = T0 * (0.995 ** k)
        step = step0 * (0.997 ** k)

        # propozycja ruchu
        x_new = x + rng.uniform(-step, step)
        x_new = min(b, max(a, x_new))
        f_new = f(x_new)
        evals += 1

        # kryterium akceptacji
        delta = f_new - fx
        if delta < 0:
            accept = True
        else:
            # im wyższa temperatura, tym chętniej przyjmujemy gorsze rozwiązania
            accept_prob = math.exp(-delta / max(t, 1e-12))
            accept = rng.random() < accept_prob

        if accept:
            x, fx = x_new, f_new
            if fx < f_best:
                x_best, f_best = x, fx

        k += 1

    dur_ms = (time.perf_counter() - start) * 1000
    return SolveResult(x_best=x_best, f_best=f_best, evaluations=evals, duration_ms=dur_ms)


def golden_section_search(f: Callable[[float], float], a: float, b: float, budget: int, rng: random.Random) -> SolveResult:
    """
    Strategia 5: Golden Section Search
    - klasyk dla funkcji unimodalnych na przedziale
    - adaptacyjnie zwęża przedział poszukiwań bez pochodnych
    - uwaga: przy wielu lokalnych minimach może zwężać się w złą dolinę,
      ale często i tak daje świetny wynik w gładkich problemach.

    W demo działa zaskakująco dobrze, bo dolina bazowa dominuje.
    """
    start = time.perf_counter()

    phi = (1 + math.sqrt(5)) / 2
    invphi = 1 / phi

    # inicjalizacja punktów
    c = b - (b - a) * invphi
    d = a + (b - a) * invphi
    fc = f(c)
    fd = f(d)
    evals = 2

    x_best, f_best = (c, fc) if fc < fd else (d, fd)

    while evals < budget and abs(b - a) > 1e-12:
        if fc < fd:
            # minimum jest w [a, d]
            b, d, fd = d, c, fc
            c = b - (b - a) * invphi
            fc = f(c); evals += 1
            if fc < f_best:
                x_best, f_best = c, fc
        else:
            # minimum jest w [c, b]
            a, c, fc = c, d, fd
            d = a + (b - a) * invphi
            fd = f(d); evals += 1
            if fd < f_best:
                x_best, f_best = d, fd

    dur_ms = (time.perf_counter() - start) * 1000
    return SolveResult(x_best=x_best, f_best=f_best, evaluations=evals, duration_ms=dur_ms)


# -----------------------------
# 4) QuantumDice – wybór strategii
# -----------------------------

def quantumdice_score(stats: StrategyStats, w_quality=0.70, w_stability=0.15, w_cost=0.15) -> float:
    """
    Rdzeń QuantumDice: scoring strategii.

    Intuicja (Twoja koncepcja, przełożona na praktyczny scoring):
    - QUALITY: jak dobry wynik dostarcza strategia (średnio i w najlepszym rolloucie)
    - STABILITY: jak powtarzalna jest (niska wariancja = mniej "chaosu")
    - COST: ile kosztuje (czas / ewaluacje)

    Ponieważ minimalizujemy f(x), "lepsza jakość" = mniejsze f.
    Żeby zrobić z tego dodatni score: używamy odwrotności (1/(eps + f)).
    """
    s = stats.summary()
    eps = 1e-12

    # QUALITY: miks średniego i najlepszego wyniku
    quality = 0.6 * (1 / (eps + s["f_best_mean"])) + 0.4 * (1 / (eps + s["f_best_min"]))

    # STABILITY: im mniejszy std, tym lepiej (odwrotność)
    stability = 1 / (eps + s["f_best_std"] + 1e-6)

    # COST: łączymy czas i liczbę ewaluacji
    # (tu budżet podobny dla wszystkich, ale czas może się różnić)
    cost = 1 / (eps + 0.7 * s["dur_ms_mean"] + 0.3 * s["eval_mean"])

    # Składamy wynik QuantumDice
    return w_quality * quality + w_stability * stability + w_cost * cost


def run_quantumdice(
    f: Callable[[float], float],
    a: float,
    b: float,
    budget: int = 200,
    rollouts: int = 20,
    seed: int = 123,
) -> Tuple[List[Tuple[str, float, Dict[str, float]]], str]:
    """
    Uruchamia wszystkie strategie, zbiera statystyki, liczy scoring i wybiera zwycięzcę.

    Zwraca:
    - ranking: lista (nazwa, score, summary)
    - winner_name
    """
    strategies: Dict[str, Callable[..., SolveResult]] = {
        "random_search": random_search,
        "grid_search": grid_search,
        "hill_climb": hill_climb,
        "simulated_annealing": simulated_annealing,
        "golden_section_search": golden_section_search,
    }

    rng_master = random.Random(seed)
    all_stats: List[StrategyStats] = []

    for name, fn in strategies.items():
        # Każda strategia dostaje własny RNG, ale z deterministycznym seedem
        # żeby wyniki były powtarzalne między uruchomieniami.
        strategy_rng = random.Random(rng_master.randint(0, 10**9))

        results: List[SolveResult] = []
        for _ in range(rollouts):
            # Dla każdego rolloutu jeszcze jeden seed (kontrolowana różnorodność)
            rollout_rng = random.Random(strategy_rng.randint(0, 10**9))
            res = fn(f=f, a=a, b=b, budget=budget, rng=rollout_rng)
            results.append(res)

        all_stats.append(StrategyStats(name=name, results=results))

    ranking = []
    for st in all_stats:
        score = quantumdice_score(st)
        ranking.append((st.name, score, st.summary()))

    # sort malejąco po score
    ranking.sort(key=lambda t: t[1], reverse=True)

    winner_name = ranking[0][0]
    return ranking, winner_name


# -----------------------------
# 5) Prezentacja wyników
# -----------------------------

def pretty_print_ranking(ranking: List[Tuple[str, float, Dict[str, float]]]) -> None:
    print("\nQuantumDice Ranking (higher = better) 🎲")
    print("=" * 72)
    print(f"{'Strategy':24} {'Score':>12} | {'f_mean':>10} {'f_min':>10} {'std':>10}")
    print("-" * 72)
    for name, score, s in ranking:
        print(
            f"{name:24} {score:12.4f} | "
            f"{s['f_best_mean']:10.6f} {s['f_best_min']:10.6f} {s['f_best_std']:10.6f}"
        )
    print("=" * 72)


def show_winner_details(ranking: List[Tuple[str, float, Dict[str, float]]], winner: str) -> None:
    # znajdź zwycięzcę
    for name, score, s in ranking:
        if name == winner:
            print(f"\nWinner: {winner} 🏆")
            print(f"Score: {score:.4f}")
            print("Why it won (signals):")
            print(f"  - Mean best f(x): {s['f_best_mean']:.6f}")
            print(f"  - Min best  f(x): {s['f_best_min']:.6f}")
            print(f"  - Std (stability): {s['f_best_std']:.6f}")
            print(f"  - Mean evaluations: {s['eval_mean']:.1f}")
            print(f"  - Mean duration ms: {s['dur_ms_mean']:.3f}")
            break


# -----------------------------
# 6) MAIN
# -----------------------------

if __name__ == "__main__":
    # Parametry problemu
    a, b = -2.0, 5.0

    # Parametry QuantumDice
    budget = 200     # ile ewaluacji na rollout (na uruchomienie strategii)
    rollouts = 25    # ile rolloutów na strategię (estymacja stabilności)
    seed = 42

    print("QuantumDice demo: selecting the best solver among 5 strategies 🎲")
    print(f"Domain: [{a}, {b}] | budget={budget} | rollouts={rollouts} | seed={seed}")

    ranking, winner = run_quantumdice(
        f=objective,
        a=a, b=b,
        budget=budget,
        rollouts=rollouts,
        seed=seed
    )

    pretty_print_ranking(ranking)
    show_winner_details(ranking, winner)

    # Pokaz przykładowego "użycia zwycięzcy" na jednej dodatkowej próbie:
    # (tu tylko demonstrujemy, że da się łatwo odpalić wskazaną strategię)
    print("\nRunning winner once more for a concrete solution:")
    strategies_map = {
        "random_search": random_search,
        "grid_search": grid_search,
        "hill_climb": hill_climb,
        "simulated_annealing": simulated_annealing,
        "golden_section_search": golden_section_search,
    }
    rng = random.Random(2026)
    res = strategies_map[winner](objective, a, b, budget, rng)
    print(f"  x_best = {res.x_best:.6f}")
    print(f"  f_best = {res.f_best:.6f}")
    print(f"  evaluations = {res.evaluations}")
    print(f"  duration_ms = {res.duration_ms:.3f}")
    print("\nDone.")
