"""
DEMO: ZŁA WERSJA WIELODZIEDZICZENIA (BEZ super()) + JAK SIĘ PSUJE
=================================================================

Cel
- pokazać, że bez super() mixiny nie układają się w pipeline
- pokazać typowe symptomy: pomijanie logiki, brak walidacji, brak cache, „znikające” warstwy

"""


# =========================================================
# 1) ZŁE MIXINY – KAŻDY PRÓBUJE „BYĆ OSTATNI”
#    (nie woła super(), więc odcina resztę łańcucha)
# =========================================================

class BadLogMixin:
    def process(self, data):
        print("[BAD LOG] start")
        # błąd: bez super() nie przejdzie dalej w MRO
        result = data * 2  # "na skróty" udaje core
        print("[BAD LOG] end")
        return result


class BadValidationMixin:
    def process(self, data):
        # walidacja jest, ale...
        if not isinstance(data, int):
            raise ValueError("data must be int")
        # błąd: bez super() reszta warstw nigdy się nie wykona
        return data * 2  # znowu "na skróty"


class BadCacheMixin:
    _cache = {}

    def process(self, data):
        if data in self._cache:
            print("[BAD CACHE] hit")
            return self._cache[data]

        # błąd: bez super() cache zapisze wynik,
        # ale pominie logowanie i walidację (jeśli jest przed nim w MRO)
        result = data * 2
        self._cache[data] = result
        return result


class CoreProcessor:
    def process(self, data):
        # Tu jest prawdziwe "core"
        return data * 2


# =========================================================
# 2) „DZIAŁA” ALE ŹLE – MRO WYBIERA PIERWSZĄ METODĘ process()
#    i na tym KONIEC, bo nie ma super()
# =========================================================

class BadProcessor(BadCacheMixin, BadValidationMixin, BadLogMixin, CoreProcessor):
    pass


# =========================================================
# 3) DEMO PROBLEMÓW
# =========================================================

def main():
    p = BadProcessor()

    print("=== MRO (kolejność wyszukiwania metod) ===")
    for cls in BadProcessor.__mro__:
        print(" -", cls.__name__)

    print("\n=== Test 1: Wywołanie z int ===")
    # Zadziała, ale wykonana będzie TYLKO pierwsza warstwa (BadCacheMixin.process)
    print("Wynik:", p.process(10))

    print("\n=== Test 2: Cache hit ===")
    print("Wynik:", p.process(10))

    print("\n=== Test 3: Wywołanie z błędnym typem (str) ===")
    # UWAGA: ponieważ pierwsza metoda jest z BadCacheMixin i NIE WALIDUJE,
    # to walidacja z BadValidationMixin nigdy się nie wykona.
    # Symptom: błąd będzie inny niż oczekiwany, albo w ogóle nie będzie kontrolowany.
    try:
        print("Wynik:", p.process("x"))  # typ powinien być odrzucony walidacją
    except Exception as e:
        print("Błąd:", type(e).__name__, "-", e)

    print("\n=== Co tu się popsuło? (podsumowanie) ===")
    print(
        "1) Wykonuje się tylko pierwsza metoda process() z MRO.\n"
        "2) Pozostałe mixiny są 'martwe', bo nie ma super().\n"
        "3) Walidacja może zostać całkowicie pominięta.\n"
        "4) Logowanie może się nigdy nie pojawić.\n"
        "5) CoreProcessor może nie być wywołany wcale.\n"
        "Wniosek: bez super() wielodziedziczenie przestaje być pipeline'em."
    )


if __name__ == "__main__":
    main()
