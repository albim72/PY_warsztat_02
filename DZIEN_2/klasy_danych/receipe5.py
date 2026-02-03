class Receipt:
    __slots__ = ("__letters", "__price_per_letter", "_finalized")

    def __init__(self, letters: float, price_per_letter: float):
        if letters <= 0:
            raise ValueError("letters must be > 0")
        if price_per_letter <= 0:
            raise ValueError("price_per_letter must be > 0")

        object.__setattr__(self, "_finalized", False)
        object.__setattr__(self, "_Receipt__letters", float(letters))
        object.__setattr__(self, "_Receipt__price_per_letter", float(price_per_letter))

    def __setattr__(self, name, value):
        # Blokujemy bezpośrednie modyfikacje danych po finalizacji.
        if getattr(self, "_finalized", False):
            raise AttributeError("Receipt is finalized and cannot be modified")
        # Dodatkowo nie pozwalamy ustawiać pól danych „ręcznie” (użyj update_price()).
        if name in ("__letters", "__price_per_letter", "_Receipt__letters", "_Receipt__price_per_letter"):
            raise AttributeError("Direct modification is not allowed; use methods (e.g. update_price).")
        object.__setattr__(self, name, value)

    # _____________ API publiczne ___________
    @property
    def letters(self) -> float:
        return self.__letters

    @property
    def price_per_letter(self) -> float:
        return self.__price_per_letter

    @property
    def total_cost(self) -> float:
        return round(self.letters * self.price_per_letter, 2)

    def finalize(self) -> None:
        """
        Zamyka paragon: po tym nie wolno zmieniać danych.
        """
        object.__setattr__(self, "_finalized", True)

    # _________ API chronione ___________
    def update_price(self, new_price: float) -> None:
        if self._finalized:
            raise RuntimeError("Receipt is finalized and cannot be modified")
        if new_price <= 0:
            raise ValueError("new_price must be > 0")
        object.__setattr__(self, "_Receipt__price_per_letter", float(new_price))


if __name__ == "__main__":
    r = Receipt(40, 7.7)
    print(r.total_cost)
    print(r.price_per_letter)
    print()

    r = Receipt(4, 1)
    print(r.total_cost)