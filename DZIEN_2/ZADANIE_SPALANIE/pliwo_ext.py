from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Trasa:
    dystans_km: float
    srednie_spalanie_na_100km: float
    cena_paliwa_za_litr: float


def oblicz_zuzycie_paliwa(dystans_km: float, srednie_spalanie_na_100km: float) -> float:
    """Jak w wersji podstawowej: zużycie paliwa w litrach."""
    if not isinstance(dystans_km, (int, float)) or not isinstance(srednie_spalanie_na_100km, (int, float)):
        raise TypeError("Parametry muszą być liczbami (int/float).")
    if dystans_km <= 0:
        raise ValueError("dystans_km musi być > 0.")
    if srednie_spalanie_na_100km <= 0:
        raise ValueError("srednie_spalanie_na_100km musi być > 0.")
    return (dystans_km / 100.0) * srednie_spalanie_na_100km


def oblicz_koszt_przejazdu(zuzycie_paliwa_l: float, cena_paliwa_za_litr: float) -> float:
    """Jak w wersji podstawowej: koszt przejazdu."""
    if not isinstance(zuzycie_paliwa_l, (int, float)) or not isinstance(cena_paliwa_za_litr, (int, float)):
        raise TypeError("Parametry muszą być liczbami (int/float).")
    if zuzycie_paliwa_l < 0:
        raise ValueError("zuzycie_paliwa_l nie może być < 0.")
    if cena_paliwa_za_litr <= 0:
        raise ValueError("cena_paliwa_za_litr musi być > 0.")
    return zuzycie_paliwa_l * cena_paliwa_za_litr


def analiza_podrozy(dystans_km: float, spalanie_na_100km: float, cena_za_litr: float) -> dict:
    """
    Wykonuje pełną analizę podróży:
    - liczy zużycie
    - liczy koszt
    - zaokrągla wartości użytkowe

    Returns:
        Słownik z wynikami.
    """
    zuzycie = oblicz_zuzycie_paliwa(dystans_km, spalanie_na_100km)
    koszt = oblicz_koszt_przejazdu(zuzycie, cena_za_litr)
    return {
        "dystans_km": float(dystans_km),
        "spalanie_l_100km": float(spalanie_na_100km),
        "cena_zl_l": float(cena_za_litr),
        "zuzycie_l": round(zuzycie, 2),
        "koszt_zl": round(koszt, 2),
    }


def analiza_wielu_tras(trasy: Iterable[Trasa]) -> dict:
    """
    Bonus: analiza wielu tras i zsumowanie wyników.
    """
    suma_zuzycia = 0.0
    suma_kosztu = 0.0
    szczegoly = []

    for t in trasy:
        wynik = analiza_podrozy(t.dystans_km, t.srednie_spalanie_na_100km, t.cena_paliwa_za_litr)
        suma_zuzycia += wynik["zuzycie_l"]
        suma_kosztu += wynik["koszt_zl"]
        szczegoly.append(wynik)

    return {
        "suma_zuzycia_l": round(suma_zuzycia, 2),
        "suma_kosztu_zl": round(suma_kosztu, 2),
        "trasy": szczegoly,
    }


if __name__ == "__main__":
    # Try/except: kontrolowany “interfejs konsolowy”
    try:
        # Przykład pojedynczej analizy (jak w treści zadania)
        wynik = analiza_podrozy(350, 7.2, 6.85)
        print("Analiza jednej trasy:")
        print(wynik)

        # Bonus: wiele tras
        trasy = [
            Trasa(350, 7.2, 6.85),
            Trasa(120, 6.5, 6.60),
            Trasa(480, 8.1, 6.95),
        ]
        zbiorczo = analiza_wielu_tras(trasy)
        print("\nAnaliza wielu tras:")
        print(zbiorczo)

    except (ValueError, TypeError) as e:
        print(f"Błąd danych wejściowych: {e}")
