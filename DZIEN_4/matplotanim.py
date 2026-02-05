import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --------- Koncepcja ----------
# Tworzymy układ "orbitujących" punktów z modulacją fazy i promienia.
# Efekt: żywa, hipnotyczna animacja, świetna do pokazania:
# - danych parametrycznych
# - animacji w matplotlib
# - wektorowych obliczeń w numpy

def main():
    np.random.seed(7)

    # Liczba punktów/orbit
    n = 1200

    # Każdy punkt ma swój "promień bazowy" i "częstotliwość"
    base_r = np.random.uniform(0.2, 1.0, n)
    omega  = np.random.uniform(0.5, 3.0, n) * np.random.choice([-1, 1], n)
    phase  = np.random.uniform(0, 2*np.pi, n)

    # Kolor = funkcja promienia (ładny gradient)
    c = base_r

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal", "box")
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    ax.axis("off")

    # Tło i delikatne „centrum”
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.scatter([0], [0], s=50, alpha=0.9)

    # Startowa pozycja
    theta0 = phase
    r0 = base_r

    x0 = r0 * np.cos(theta0)
    y0 = r0 * np.sin(theta0)

    sc = ax.scatter(x0, y0, s=6, c=c, alpha=0.9)

    # Delikatna "poświata" w postaci śladu: kilka warstw przezroczystych
    trail = []
    for k in range(1, 6):
        tsc = ax.scatter(x0, y0, s=6, c=c, alpha=0.18 / k)
        trail.append(tsc)

    def update(frame: int):
        # Czas w sekundach (umownie)
        t = frame / 30.0

        # „Oddychanie” promienia: modulacja zależna od czasu i promienia bazowego
        r = base_r * (0.78 + 0.22*np.sin(2*np.pi*(0.15*t + base_r)))

        # Kąt rośnie z własną prędkością (omega)
        theta = phase + omega * t

        x = r * np.cos(theta)
        y = r * np.sin(theta)

        # Aktualizacja śladów: przesuwamy historię
        # Najnowszy punkt idzie do sc, starsze do trail
        prev_offsets = sc.get_offsets()
        for i in range(len(trail)-1, 0, -1):
            trail[i].set_offsets(trail[i-1].get_offsets())
        trail[0].set_offsets(prev_offsets)

        sc.set_offsets(np.c_[x, y])
        return [sc, *trail]

    ani = FuncAnimation(fig, update, frames=2000, interval=33, blit=True)
    plt.show()

if __name__ == "__main__":
    main()
