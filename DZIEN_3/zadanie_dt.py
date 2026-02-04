from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


# =========================
# Walidacja (wspólne klocki)
# =========================

def _is_number(x: Any) -> bool:
    # bool jest podklasą int w Pythonie, więc wykluczamy go jawnie
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _validate_positive_number(value: Any, field_name: str, *, allow_zero: bool = False) -> float:
    """
    Sprawdza, czy value jest liczbą (int/float), oraz czy jest dodatnia
    (lub nieujemna, jeśli allow_zero=True). Zwraca float.
    """
    if not _is_number(value):
        raise TypeError(f"{field_name} musi być liczbą (int/float), a nie: {type(value).__name__}")

    v = float(value)

    if allow_zero:
        if v < 0:
            raise ValueError(f"{field_name} nie może być ujemne (podano: {v}).")
    else:
        if v <= 0:
            raise ValueError(f"{field_name} musi być > 0 (podano: {v}).")

    return v


# =========================
# 1) Model danych (dataclass)
# =========================

@dataclass(frozen=True)
class PodrozSamochodowa:
    dystans_km: float
    srednie_spalanie_na_100km: float
    cena_paliwa_za_litr: float

    def __post_init__(self) -> None:
        # Walidacja w konstruktorze dataclass (zgodnie z wymaganiami zadania)
        object.__setattr__(
            self,
            "dystans_km",
            _validate_positive_number(self.dystans_km, "dystans_km", allow_zero=False),
        )
        object.__setattr__(
            self,
            "srednie_spalanie_na_100km",
            _validate_positive_number(self.srednie_spalanie_na_100km, "srednie_spalanie_na_100km", allow_zero=False),
        )
        object.__setattr__(
            self,
            "cena_paliwa_za_litr",
            _validate_positive_number(self.cena_paliwa_za_litr, "cena_paliwa_za_litr", allow_zero=False),
        )


# =========================
# 2) Funkcje obliczeniowe
# =========================

def oblicz_zuzycie_paliwa_l(dystans_km: float, srednie_spalanie_na_100km: float) -> float:
    """
    Zwraca zużycie paliwa w litrach dla zadanej odległości (km)
    i średniego spalania (l/100km).
    """
    d = _validate_positive_number(dystans_km, "dystans_km", allow_zero=False)
    s = _validate_positive_number(srednie_spalanie_na_100km, "srednie_spalanie_na_100km", allow_zero=False)
    return d * s / 100.0


def oblicz_koszt_przejazdu_zl(zuzycie_paliwa_l: float, cena_paliwa_za_litr: float) -> float:
    """
    Zwraca koszt przejazdu (zł) dla danego zużycia paliwa (l)
    i ceny paliwa (zł/l).
    """
    z = _validate_positive_number(zuzycie_paliwa_l, "zuzycie_paliwa_l", allow_zero=True)
    c = _validate_positive_number(cena_paliwa_za_litr, "cena_paliwa_za_litr", allow_zero=False)
    return z * c


# =========================
# 5) Scenariusz testowy + 4) try/except
# =========================

def uruchom_scenariusz_pojedynczy() -> None:
    print("=== Analiza pojedynczej podróży ===")

    try:
        # Scenariusz z zadania: 350 km, 7.2 l/100km, 6.85 zł/l
        podroz = PodrozSamochodowa(
            dystans_km=350,
            srednie_spalanie_na_100km=7.2,
            cena_paliwa_za_litr=6.85,
        )

        zuzycie = oblicz_zuzycie_paliwa_l(podroz.dystans_km, podroz.srednie_spalanie_na_100km)
        koszt = oblicz_koszt_przejazdu_zl(zuzycie, podroz.cena_paliwa_za_litr)

        print(f"Dystans: {podroz.dystans_km:.0f} km")
        print(f"Średnie spalanie: {podroz.srednie_spalanie_na_100km:.2f} l/100km")
        print(f"Cena paliwa: {podroz.cena_paliwa_za_litr:.2f} zł/l")
        print(f"Zużycie paliwa: {zuzycie:.2f} l")
        print(f"Koszt przejazdu: {koszt:.2f} zł")

    except (TypeError, ValueError) as e:
        print(f"[BŁĄD DANYCH] {e}")
    except Exception as e:
        # awaryjnie, gdyby coś poszło nie tak poza walidacją
        print(f"[NIEOCZEKIWANY BŁĄD] {type(e).__name__}: {e}")


# =========================
# Zadanie rozszerzające (dla chętnych)
# - lista wielu podróży
# - suma kosztów i zużycia
# - zaokrąglanie do 2 miejsc
# - słownikowa struktura wyników
# =========================

def policz_podroze(podroze: Iterable[PodrozSamochodowa]) -> dict[str, Any]:
    """
    Przyjmuje listę/iterowalny zbiór podróży i zwraca:
    - listę wyników cząstkowych (słowniki)
    - sumy zużycia i kosztów
    Wszystko zaokrąglone do 2 miejsc.
    """
    wyniki: list[dict[str, Any]] = []
    suma_zuzycia = 0.0
    suma_kosztu = 0.0

    for idx, p in enumerate(podroze, start=1):
        zuzycie = oblicz_zuzycie_paliwa_l(p.dystans_km, p.srednie_spalanie_na_100km)
        koszt = oblicz_koszt_przejazdu_zl(zuzycie, p.cena_paliwa_za_litr)

        suma_zuzycia += zuzycie
        suma_kosztu += koszt

        wyniki.append(
            {
                "nr": idx,
                "dystans_km": round(p.dystans_km, 2),
                "spalanie_l_na_100km": round(p.srednie_spalanie_na_100km, 2),
                "cena_zl_na_l": round(p.cena_paliwa_za_litr, 2),
                "zuzycie_l": round(zuzycie, 2),
                "koszt_zl": round(koszt, 2),
            }
        )

    return {
        "liczba_podrozy": len(wyniki),
        "podroze": wyniki,
        "suma_zuzycia_l": round(suma_zuzycia, 2),
        "suma_kosztu_zl": round(suma_kosztu, 2),
    }


def uruchom_scenariusz_dla_chetnych() -> None:
    print("\n=== Analiza wielu podróży (dla chętnych) ===")

    try:
        podroze = [
            PodrozSamochodowa(350, 7.2, 6.85),
            PodrozSamochodowa(120, 6.5, 6.60),
            PodrozSamochodowa(80, 8.1, 6.95),
        ]

        raport = policz_podroze(podroze)

        for p in raport["podroze"]:
            print(
                f"#{p['nr']}: dystans={p['dystans_km']} km | "
                f"spalanie={p['spalanie_l_na_100km']} l/100km | "
                f"cena={p['cena_zl_na_l']} zł/l | "
                f"zużycie={p['zuzycie_l']} l | "
                f"koszt={p['koszt_zl']} zł"
            )

        print(f"Suma zużycia: {raport['suma_zuzycia_l']:.2f} l")
        print(f"Suma kosztu: {raport['suma_kosztu_zl']:.2f} zł")

    except (TypeError, ValueError) as e:
        print(f"[BŁĄD DANYCH] {e}")
    except Exception as e:
        print(f"[NIEOCZEKIWANY BŁĄD] {type(e).__name__}: {e}")


def main() -> None:
    uruchom_scenariusz_pojedynczy()
    uruchom_scenariusz_dla_chetnych()


if __name__ == "__main__":
    main()
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


# =========================
# Walidacja (wspólne klocki)
# =========================

def _is_number(x: Any) -> bool:
    # bool jest podklasą int w Pythonie, więc wykluczamy go jawnie
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _validate_positive_number(value: Any, field_name: str, *, allow_zero: bool = False) -> float:
    """
    Sprawdza, czy value jest liczbą (int/float), oraz czy jest dodatnia
    (lub nieujemna, jeśli allow_zero=True). Zwraca float.
    """
    if not _is_number(value):
        raise TypeError(f"{field_name} musi być liczbą (int/float), a nie: {type(value).__name__}")

    v = float(value)

    if allow_zero:
        if v < 0:
            raise ValueError(f"{field_name} nie może być ujemne (podano: {v}).")
    else:
        if v <= 0:
            raise ValueError(f"{field_name} musi być > 0 (podano: {v}).")

    return v


# =========================
# 1) Model danych (dataclass)
# =========================

@dataclass(frozen=True)
class PodrozSamochodowa:
    dystans_km: float
    srednie_spalanie_na_100km: float
    cena_paliwa_za_litr: float

    def __post_init__(self) -> None:
        # Walidacja w konstruktorze dataclass (zgodnie z wymaganiami zadania)
        object.__setattr__(
            self,
            "dystans_km",
            _validate_positive_number(self.dystans_km, "dystans_km", allow_zero=False),
        )
        object.__setattr__(
            self,
            "srednie_spalanie_na_100km",
            _validate_positive_number(self.srednie_spalanie_na_100km, "srednie_spalanie_na_100km", allow_zero=False),
        )
        object.__setattr__(
            self,
            "cena_paliwa_za_litr",
            _validate_positive_number(self.cena_paliwa_za_litr, "cena_paliwa_za_litr", allow_zero=False),
        )


# =========================
# 2) Funkcje obliczeniowe
# =========================

def oblicz_zuzycie_paliwa_l(dystans_km: float, srednie_spalanie_na_100km: float) -> float:
    """
    Zwraca zużycie paliwa w litrach dla zadanej odległości (km)
    i średniego spalania (l/100km).
    """
    d = _validate_positive_number(dystans_km, "dystans_km", allow_zero=False)
    s = _validate_positive_number(srednie_spalanie_na_100km, "srednie_spalanie_na_100km", allow_zero=False)
    return d * s / 100.0


def oblicz_koszt_przejazdu_zl(zuzycie_paliwa_l: float, cena_paliwa_za_litr: float) -> float:
    """
    Zwraca koszt przejazdu (zł) dla danego zużycia paliwa (l)
    i ceny paliwa (zł/l).
    """
    z = _validate_positive_number(zuzycie_paliwa_l, "zuzycie_paliwa_l", allow_zero=True)
    c = _validate_positive_number(cena_paliwa_za_litr, "cena_paliwa_za_litr", allow_zero=False)
    return z * c


# =========================
# 5) Scenariusz testowy + 4) try/except
# =========================

def uruchom_scenariusz_pojedynczy() -> None:
    print("=== Analiza pojedynczej podróży ===")

    try:
        # Scenariusz z zadania: 350 km, 7.2 l/100km, 6.85 zł/l
        podroz = PodrozSamochodowa(
            dystans_km=350,
            srednie_spalanie_na_100km=7.2,
            cena_paliwa_za_litr=6.85,
        )

        zuzycie = oblicz_zuzycie_paliwa_l(podroz.dystans_km, podroz.srednie_spalanie_na_100km)
        koszt = oblicz_koszt_przejazdu_zl(zuzycie, podroz.cena_paliwa_za_litr)

        print(f"Dystans: {podroz.dystans_km:.0f} km")
        print(f"Średnie spalanie: {podroz.srednie_spalanie_na_100km:.2f} l/100km")
        print(f"Cena paliwa: {podroz.cena_paliwa_za_litr:.2f} zł/l")
        print(f"Zużycie paliwa: {zuzycie:.2f} l")
        print(f"Koszt przejazdu: {koszt:.2f} zł")

    except (TypeError, ValueError) as e:
        print(f"[BŁĄD DANYCH] {e}")
    except Exception as e:
        # awaryjnie, gdyby coś poszło nie tak poza walidacją
        print(f"[NIEOCZEKIWANY BŁĄD] {type(e).__name__}: {e}")


# =========================
# Zadanie rozszerzające (dla chętnych)
# - lista wielu podróży
# - suma kosztów i zużycia
# - zaokrąglanie do 2 miejsc
# - słownikowa struktura wyników
# =========================

def policz_podroze(podroze: Iterable[PodrozSamochodowa]) -> dict[str, Any]:
    """
    Przyjmuje listę/iterowalny zbiór podróży i zwraca:
    - listę wyników cząstkowych (słowniki)
    - sumy zużycia i kosztów
    Wszystko zaokrąglone do 2 miejsc.
    """
    wyniki: list[dict[str, Any]] = []
    suma_zuzycia = 0.0
    suma_kosztu = 0.0

    for idx, p in enumerate(podroze, start=1):
        zuzycie = oblicz_zuzycie_paliwa_l(p.dystans_km, p.srednie_spalanie_na_100km)
        koszt = oblicz_koszt_przejazdu_zl(zuzycie, p.cena_paliwa_za_litr)

        suma_zuzycia += zuzycie
        suma_kosztu += koszt

        wyniki.append(
            {
                "nr": idx,
                "dystans_km": round(p.dystans_km, 2),
                "spalanie_l_na_100km": round(p.srednie_spalanie_na_100km, 2),
                "cena_zl_na_l": round(p.cena_paliwa_za_litr, 2),
                "zuzycie_l": round(zuzycie, 2),
                "koszt_zl": round(koszt, 2),
            }
        )

    return {
        "liczba_podrozy": len(wyniki),
        "podroze": wyniki,
        "suma_zuzycia_l": round(suma_zuzycia, 2),
        "suma_kosztu_zl": round(suma_kosztu, 2),
    }


def uruchom_scenariusz_dla_chetnych() -> None:
    print("\n=== Analiza wielu podróży (dla chętnych) ===")

    try:
        podroze = [
            PodrozSamochodowa(350, 7.2, 6.85),
            PodrozSamochodowa(120, 6.5, 6.60),
            PodrozSamochodowa(80, 8.1, 6.95),
        ]

        raport = policz_podroze(podroze)

        for p in raport["podroze"]:
            print(
                f"#{p['nr']}: dystans={p['dystans_km']} km | "
                f"spalanie={p['spalanie_l_na_100km']} l/100km | "
                f"cena={p['cena_zl_na_l']} zł/l | "
                f"zużycie={p['zuzycie_l']} l | "
                f"koszt={p['koszt_zl']} zł"
            )

        print(f"Suma zużycia: {raport['suma_zuzycia_l']:.2f} l")
        print(f"Suma kosztu: {raport['suma_kosztu_zl']:.2f} zł")

    except (TypeError, ValueError) as e:
        print(f"[BŁĄD DANYCH] {e}")
    except Exception as e:
        print(f"[NIEOCZEKIWANY BŁĄD] {type(e).__name__}: {e}")


def main() -> None:
    uruchom_scenariusz_pojedynczy()
    uruchom_scenariusz_dla_chetnych()


if __name__ == "__main__":
    main()
