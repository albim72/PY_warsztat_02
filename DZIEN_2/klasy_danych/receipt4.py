from dataclasses import dataclass

@dataclass
class Recept:
    letters: float
    price_per_letter: float

    def __post_init__(self):
        if self.letters <= 0:
            raise ValueError("letters must be > 0:")
        if self.price_per_letter <= 0:
            raise ValueError("price_per_letter must be > 0:")
    @property
    def total_cost(self):
        return round(self.letters * self.price_per_letter,2)

r = Recept(letters=40, price_per_letter=7.7)
print(r.total_cost)

r = Recept(letters=4, price_per_letter=1)
print(r.total_cost)