"""
DEMO: WIELODZIEDZICZENIE W PYTHONIE (MIXINY + MRO)

Cel:
- pokazać sens wielodziedziczenia
- pokazać poprawne użycie super()
- zobaczyć MRO w praktyce

Uruchom:
    python multiple_inheritance_demo.py
"""


# =========================
# MIXINY – POJEDYNCZE CECHY
# =========================

class LogMixin(object):
    def process(self, data):
        print("[LOG] start")
        result = super().process(data) #type(self).mro
        print("[LOG] end")
        return result


class ValidationMixin:
    def process(self, data):
        if not isinstance(data, int):
            raise ValueError("data must be int")
        return super().process(data)


class CacheMixin:
    _cache = {}

    def process(self, data):
        if data in self._cache:
            print("[CACHE] hit")
            return self._cache[data]

        result = super().process(data)
        self._cache[data] = result
        return result


# =========================
# KLASA BAZOWA (CORE)
# =========================

class CoreProcessor:
    def process(self, data):
        return data * 2


# =========================
# WIELODZIEDZICZENIE
# =========================

class Processor(CacheMixin, ValidationMixin, LogMixin, CoreProcessor):
    """
    Kolejność klas MA ZNACZENIE.
    Python zbuduje liniowy pipeline wg MRO.
    """
    pass


# =========================
# DEMO
# =========================

def main():
    p = Processor()

    print("=== Pierwsze wywołanie ===")
    print("Wynik:", p.process(10))

    print("\n=== Drugie wywołanie (cache) ===")
    print("Wynik:", p.process(10))

    # print("\n=== Próba błędnych danych ===")
    # try:
    #     p.process("x")
    # except ValueError as e:
    #     print("Błąd:", e)

    p.process(23)
    p.process(111)

    #GŁÓWNA LOGIKA BIZNESOWA - CoreProcessor
    print(p.process(21))
    p.process(21)
    p.process(34)

    print("\n=== MRO (Method Resolution Order) ===")
    for cls in Processor.__mro__:
        print(" -", cls.__name__)


if __name__ == "__main__":
    main()
