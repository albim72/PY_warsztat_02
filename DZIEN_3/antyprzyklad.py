"""
ANTYPRZYKŁAD ABSTRAKCJI + POPRAWNA WERSJA
========================================

Uruchom:
    python antyprzyklad_abstrakcja.py

Cel dydaktyczny:
- pokazać, jak brak abstrakcji prowadzi do rozpadu kodu
- pokazać tę samą logikę po naprawie architektonicznej
"""

from abc import ABC, abstractmethod


# =========================================================
# 1) ANTYPRZYKŁAD – KOD BEZ ABSTRAKCJI (IF-LOGIA)
# =========================================================

def koszt_przejazdu_bez_abstrakcji(typ_pojazdu: str, km: float, **dane) -> float:
    """
    Jedna funkcja robi wszystko:
    - zna wszystkie typy pojazdów
    - zna wszystkie reguły biznesowe
    - miesza odpowiedzialności
    """

    sezon = dane.get("sezon", "lato")          # lato / zima
    rabat_flota = dane.get("rabat_flota", 0.0)
    oplata_stala = dane.get("oplata_stala", 0.0)

    modyfikator = 1.10 if sezon == "zima" else 1.00

    if typ_pojazdu == "spalinowy":
        spalanie = dane["spalanie"] * modyfikator
        cena = dane["cena_paliwa"]
        koszt = km * spalanie / 100 * cena + oplata_stala

    elif typ_pojazdu == "elektryczny":
        zuzycie = dane["zuzycie"] * modyfikator
        cena = dane["cena_kwh"]
        koszt = km * zuzycie / 100 * cena + oplata_stala

    elif typ_pojazdu == "hybryda":
        udzial_prad = dane["udzial_prad"]
        spalanie = dane["spalanie"] * modyfikator
        zuzycie = dane["zuzycie"] * modyfikator

        km_prad = km * udzial_prad
        km_paliwo = km - km_prad

        koszt = (
            km_prad * zuzycie / 100 * dane["cena_kwh"]
            + km_paliwo * spalanie / 100 * dane["cena_paliwa"]
            + oplata_stala
        )

    else:
        raise ValueError("Nieznany typ pojazdu")

    return koszt * (1 - rabat_flota)


# =========================================================
# 2) WERSJA POPRAWNA – ABSTRAKCJA + POLIMORFIZM
# =========================================================

class Pojazd(ABC):
    """
    Abstrakcyjny kontrakt:
    każdy pojazd MUSI umieć policzyć koszt przejazdu.
    """

    @abstractmethod
    def koszt_przejazdu(self, km: float) -> float:
        pass


class SamochodSpalinowy(Pojazd):
    def __init__(self, spalanie, cena_paliwa):
        self.spalanie = spalanie
        self.cena = cena_paliwa

    def koszt_przejazdu(self, km: float) -> float:
        return km * self.spalanie / 100 * self.cena


class SamochodElektryczny(Pojazd):
    def __init__(self, zuzycie, cena_kwh):
        self.zuzycie = zuzycie
        self.cena = cena_kwh

    def koszt_przejazdu(self, km: float) -> float:
        return km * self.zuzycie / 100 * self.cena


class Hybryda(Pojazd):
    def __init__(self, spalanie, cena_paliwa, zuzycie, cena_kwh, udzial_prad):
        self.spalanie = spalanie
        self.cena_paliwa = cena_paliwa
        self.zuzycie = zuzycie
        self.cena_kwh = cena_kwh
        self.udzial_prad = udzial_prad

    def koszt_przejazdu(self, km: float) -> float:
        km_prad = km * self.udzial_prad
        km_paliwo = km - km_prad

        return (
            km_prad * self.zuzycie / 100 * self.cena_kwh
            + km_paliwo * self.spalanie / 100 * self.cena_paliwa
        )


# =========================================================
# 3) WARSTWY POLITYK (niezależne od pojazdu)
# =========================================================

class PolitykaZimowa:
    def __init__(self, pojazd: Pojazd):
        self.pojazd = pojazd

    def koszt_przejazdu(self, km: float) -> float:
        return self.pojazd.koszt_przejazdu(km) * 1.10


class RabatFlotowy:
    def __init__(self, pojazd: Pojazd, rabat: float):
        self.pojazd = pojazd
        self.rabat = rabat

    def koszt_przejazdu(self, km: float) -> float:
        return self.pojazd.koszt_przejazdu(km) * (1 - self.rabat)


# =========================================================
# 4) MAIN – PORÓWNANIE
# =========================================================

def main():
    print("\n=== ANTYPRZYKŁAD (bez abstrakcji) ===")
    koszt1 = koszt_przejazdu_bez_abstrakcji(
        "hybryda",
        300,
        spalanie=6.0,
        cena_paliwa=6.8,
        zuzycie=18.0,
        cena_kwh=1.2,
        udzial_prad=0.4,
        sezon="zima",
        rabat_flota=0.06,
        oplata_stala=50,
    )
    print(f"Koszt (chaos): {koszt1:.2f} zł")

    print("\n=== WERSJA Z ABSTRAKCJĄ ===")
    pojazd = Hybryda(
        spalanie=6.0,
        cena_paliwa=6.8,
        zuzycie=18.0,
        cena_kwh=1.2,
        udzial_prad=0.4,
    )

    pojazd = PolitykaZimowa(pojazd)
    pojazd = RabatFlotowy(pojazd, 0.06)

    koszt2 = pojazd.koszt_przejazdu(300)
    print(f"Koszt (struktura): {koszt2:.2f} zł")


if __name__ == "__main__":
    main()
