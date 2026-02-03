def oblicz_zuzycie_paliwa(dystans_km: float, srednie_spalanie_na_100km: float) -> float:
    """
    Oblicza łączne zużycie paliwa w litrach.

    Args:
        dystans_km: Długość trasy w kilometrach (musi być > 0).
        srednie_spalanie_na_100km: Średnie spalanie w litrach na 100 km (musi być > 0).

    Returns:
        Łączne zużycie paliwa w litrach.

    Raises:
        ValueError: Gdy dane wejściowe są niepoprawne (<= 0).
        TypeError: Gdy podano wartości nie-numeryczne.
    """
    if not isinstance(dystans_km, (int, float)) or not isinstance(srednie_spalanie_na_100km, (int, float)):
        raise TypeError("dystans_km i srednie_spalanie_na_100km muszą być liczbami (int/float).")

    if dystans_km <= 0:
        raise ValueError("dystans_km musi być > 0.")
    if srednie_spalanie_na_100km <= 0:
        raise ValueError("srednie_spalanie_na_100km musi być > 0.")

    return (dystans_km / 100.0) * srednie_spalanie_na_100km


def oblicz_koszt_przejazdu(zuzycie_paliwa_l: float, cena_paliwa_za_litr: float) -> float:
    """
    Oblicza całkowity koszt przejazdu.

    Args:
        zuzycie_paliwa_l: Ilość zużytego paliwa w litrach (musi być >= 0).
        cena_paliwa_za_litr: Cena paliwa za 1 litr (musi być > 0).

    Returns:
        Całkowity koszt przejazdu.

    Raises:
        ValueError: Gdy dane wejściowe są niepoprawne.
        TypeError: Gdy podano wartości nie-numeryczne.
    """
    if not isinstance(zuzycie_paliwa_l, (int, float)) or not isinstance(cena_paliwa_za_litr, (int, float)):
        raise TypeError("zuzycie_paliwa_l i cena_paliwa_za_litr muszą być liczbami (int/float).")

    if zuzycie_paliwa_l < 0:
        raise ValueError("zuzycie_paliwa_l nie może być < 0.")
    if cena_paliwa_za_litr <= 0:
        raise ValueError("cena_paliwa_za_litr musi być > 0.")

    return zuzycie_paliwa_l * cena_paliwa_za_litr


if __name__ == "__main__":
    # Scenariusz testowy (z treści zadania)
    dystans = 350.0
    spalanie = 7.2
    cena = 6.85

    zuzycie = oblicz_zuzycie_paliwa(dystans, spalanie)
    koszt = oblicz_koszt_przejazdu(zuzycie, cena)

    print(f"Dystans: {dystans} km")
    print(f"Średnie spalanie: {spalanie} l/100km")
    print(f"Zużycie paliwa: {zuzycie:.2f} l")
    print(f"Cena paliwa: {cena:.2f} zł/l")
    print(f"Koszt przejazdu: {koszt:.2f} zł")
