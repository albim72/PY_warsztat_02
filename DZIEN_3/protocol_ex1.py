from typing import Protocol

print(...)
print(type(...))

class Pojazd(Protocol):
    def koszt_przejazdu(self,km: float) -> float:
        ...


class Samochod:
    def __init__(self, spalanie, cena):
        self.spalanie = spalanie
        self.cena = cena

    def koszt_przejazdu(self,km: float) -> float:
        return km * self.spalanie / 100 * self.cena


class Rower:
    def koszt_przejazdu(self,km: float) -> float:
        return 0.0

def raport(pojazd: Pojazd, dystans: float) -> float:
    return pojazd.koszt_przejazdu(dystans)

print(raport(Samochod(6, 6.8), 300))
print(raport(Rower(), 80))


