def przelicz_walute(kwota, kurs, waluta_z, waluta_na):
    """
    Przelicza kwotę z jednej waluty na inną na podstawie podanego kursu.

    :param kwota: (float) kwota do przeliczenia
    :param kurs: (float) kurs wymiany (1 waluta_z = kurs waluta_na)
    :param waluta_z: (str) kod waluty źródłowej
    :param waluta_na: (str) kod waluty docelowej
    :return: (float) przeliczona kwota
    """

    try:
        # Walidacja typów i wartości
        kwota = float(kwota)
        kurs = float(kurs)

        if kwota <= 0:
            raise ValueError("Kwota musi być większa od zera.")

        if kurs <= 0:
            raise ValueError("Kurs musi być większy od zera.")

        if not waluta_z.isalpha() or not waluta_na.isalpha():
            raise ValueError("Kod waluty musi zawierać tylko litery.")

        wynik = kwota * kurs
        return round(wynik, 2)

    except ValueError as e:
        print(f"Błąd danych wejściowych: {e}")
        return None

    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        return None


def test_przelicz_walute():
    print("=== TESTY FUNKCJI PRZELICZ_WALUTE ===")

    print("Test 1 – poprawne dane:")
    print(przelicz_walute(100, 4.32, "EUR", "PLN"))  # oczekiwane: 432.00

    print("\nTest 2 – kwota ujemna:")
    print(przelicz_walute(-50, 4.32, "EUR", "PLN"))

    print("\nTest 3 – kurs = 0:")
    print(przelicz_walute(100, 0, "EUR", "PLN"))

    print("\nTest 4 – niepoprawny kod waluty:")
    print(przelicz_walute(100, 4.32, "EU1", "PLN"))

    print("\nTest 5 – dane tekstowe zamiast liczbowych:")
    print(przelicz_walute("sto", "cztery", "EUR", "PLN"))


if __name__ == "__main__":
    test_przelicz_walute()
