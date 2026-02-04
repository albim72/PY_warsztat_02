from dataclasses import dataclass

@dataclass
class Konto:
    numer: str
    saldo: float


@dataclass
class Klient:
    imie: str
    konto: Konto | None = None   # asocjacja (opcjonalna)

    def pokaz_saldo(self) -> None:
        if self.konto is None:
            print("Brak przypisanego konta")
        else:
            print(f"Saldo: {self.konto.saldo:.2f} zł")

konto = Konto("PL12 9999 0000", 1500.0)
klient = Klient("Ewa")

klient.pokaz_saldo()      # brak relacji
klient.konto = konto      # UTWORZENIE ASOCJACJI
klient.pokaz_saldo()

