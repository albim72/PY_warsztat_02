from dataclasses import dataclass

@dataclass
class Silnik:
    moc_km: int

    def uruchom(self) -> str:
        return f"Silnik {self.moc_km} KM uruchomiony"


@dataclass
class SkrzyniaBiegow:
    typ: str  # "manual" / "auto"

    def zmien_bieg(self, bieg: int) -> str:
        return f"Zmieniono bieg na {bieg} ({self.typ})"


class Samochod:
    def __init__(self, moc_km: int, typ_skrzyni: str):
        # KOMPOZYCJA: Samochod tworzy części i nimi zarządza
        self.silnik = Silnik(moc_km)
        self.skrzynia = SkrzyniaBiegow(typ_skrzyni)

    def jedz(self) -> None:
        print(self.silnik.uruchom())
        print(self.skrzynia.zmien_bieg(1))
        print("Samochód jedzie.")


auto = Samochod(150, "manual")
auto.jedz()
