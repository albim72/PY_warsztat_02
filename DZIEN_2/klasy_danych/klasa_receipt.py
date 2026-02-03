from dataclasses import dataclass
@dataclass
class Receipt:
    letters: float
    price_per_letter: float


r1 = Receipt(letters=10, price_per_letter=100)
print(r1)
r2 = Receipt(123,25)
print(r2)