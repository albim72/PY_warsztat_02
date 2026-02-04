from dataclasses import dataclass, field
from typing import Callable, List


@dataclass(eq=False)
class Pracownik:
    imie: str
    _rola: str
    _on_role_change: List[Callable[["Pracownik", str, str], None]] = field(
        default_factory=list, init=False, repr=False
    )

    # Hash po tożsamości obiektu (stabilne dla klucza w dict nawet gdy rola się zmienia)
    __hash__ = object.__hash__

    @property
    def rola(self) -> str:
        return self._rola

    @rola.setter
    def rola(self, nowa_rola: str) -> None:
        stara_rola = self._rola
        if nowa_rola == stara_rola:
            return
        self._rola = nowa_rola
        # powiadom zainteresowane zespoły, że rola się zmieniła
        for cb in list(self._on_role_change):
            cb(self, stara_rola, nowa_rola)

    def _subscribe_role_change(self, callback: Callable[["Pracownik", str, str], None]) -> None:
        if callback not in self._on_role_change:
            self._on_role_change.append(callback)


class Zespol:
    def __init__(self, nazwa: str):
        self.nazwa = nazwa
        self.czlonkowie: list[Pracownik] = []
        # mapowanie: pracownik -> jego rola "zapamiętana" w kontekście zespołu
        self._role_w_zespole: dict[Pracownik, str] = {}
        self.prawocnik: Pracownik | None = None

    def dodaj(self, p: Pracownik) -> None:
        # AGREGACJA: zespół przyjmuje istniejący obiekt
        if p not in self.czlonkowie:
            self.czlonkowie.append(p)
            self._role_w_zespole[p] = p.rola
            p._subscribe_role_change(self._on_pracownik_role_change)

        # jeżeli nie ma jeszcze prawocnika, ustaw pierwszą dodaną osobę
        if self.prawocnik is None:
            self.prawocnik = p

    def ustaw_prawocnika(self, p: Pracownik) -> None:
        if p not in self.czlonkowie:
            self.dodaj(p)
        self.prawocnik = p

    def _on_pracownik_role_change(self, p: Pracownik, stara: str, nowa: str) -> None:
        # automatyczna aktualizacja roli w zespole
        if p in self._role_w_zespole:
            self._role_w_zespole[p] = nowa

    def sklad(self) -> str:
        osoby = ", ".join(
            f"{p.imie} ({self._role_w_zespole.get(p, p.rola)})" for p in self.czlonkowie
        )
        praw = (
            f"{self.prawocnik.imie} ({self._role_w_zespole.get(self.prawocnik, self.prawocnik.rola)})"
            if self.prawocnik
            else "brak"
        )
        return f"Zespół {self.nazwa}: {osoby} | Prawocnik: {praw}"


ania = Pracownik("Ania", "Data Scientist")
marek = Pracownik("Marek", "Backend")

ai_team = Zespol("AI")
rnd_team = Zespol("R&D")

ai_team.dodaj(ania)
rnd_team.dodaj(ania)   # ten sam obiekt pracownika może należeć do kilku zespołów
ai_team.dodaj(marek)

ai_team.ustaw_prawocnika(ania)

print(ai_team.sklad())
print(rnd_team.sklad())

# zmiana roli przez property -> automatycznie aktualizuje role "w zespołach"
ania.rola = "Data Architect"

print(ai_team.sklad())
print(rnd_team.sklad())
