class Drukarka:
    def drukuj(self, tekst: str) -> None:
        print(f"[DRUK] {tekst}")
def wydrukuj_fakture(drukarka: Drukarka, numer: int) -> None:
    # ZALEŻNOŚĆ: drukarka używana tylko w czasie wywołania
    drukarka.drukuj(f"Faktura nr {numer}")
drukarka = Drukarka()
wydrukuj_fakture(drukarka, 123)
