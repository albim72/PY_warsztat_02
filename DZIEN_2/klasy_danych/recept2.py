from dataclasses import dataclass

@dataclass
class Recept:
    letters: float
    price_per_letter: float

    def total_cost(self):
        return round(self.letters * self.price_per_letter,2)

r = Recept(letters=40, price_per_letter=7.7)
print(r.total_cost())