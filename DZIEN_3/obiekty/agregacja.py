from dataclasses import dataclass

@dataclass
class Pracownik:
    imie: str
    rola: str


class Zespol:
    def __init__(self, nazwa: str):
        self.nazwa = nazwa
        self.czlonkowie: list[Pracownik] = []

    def dodaj(self, p: Pracownik) -> None:
        # AGREGACJA: zespół przyjmuje istniejący obiekt
        self.czlonkowie.append(p)

    def sklad(self) -> str:
        osoby = ", ".join(f"{p.imie} ({p.rola})" for p in self.czlonkowie)
        return f"Zespół {self.nazwa}: {osoby}"


ania = Pracownik("Ania", "Data Scientist")
marek = Pracownik("Marek", "Backend")

ai_team = Zespol("AI")
rnd_team = Zespol("R&D")

ai_team.dodaj(ania)
rnd_team.dodaj(ania)   # ten sam obiekt pracownika może należeć do kilku zespołów
ai_team.dodaj(marek)

print(ai_team.sklad())
print(rnd_team.sklad())
