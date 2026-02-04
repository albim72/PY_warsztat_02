def koszt_przejazdu(typ_pojazdu: str, km: float, **dane) -> float:
    # globalne "reguły"
    sezon = dane.get("sezon", "lato")             # "lato" / "zima"
    rabat_flota = dane.get("rabat_flota", 0.0)    # np. 0.06
    oplata_stala = dane.get("oplata_stala", 0.0)  # np. autostrada

    if sezon == "zima":
        modyfikator = 1.10
    else:
        modyfikator = 1.00

    if typ_pojazdu == "spalinowy":
        spalanie = dane["spalanie_l_na_100km"] * modyfikator
        cena_paliwa = dane["cena_paliwa"]
        koszt = km * spalanie / 100 * cena_paliwa + oplata_stala

    elif typ_pojazdu == "elektryczny":
        zuzycie = dane["zuzycie_kwh_na_100km"] * modyfikator
        cena_kwh = dane["cena_kwh"]
        koszt = km * zuzycie / 100 * cena_kwh + oplata_stala

    elif typ_pojazdu == "hybryda":
        # ile % trasy jedziemy na prądzie?
        udzial_prad = dane["udzial_prad"]  # np. 0.4
        spalanie = dane["spalanie_l_na_100km"] * modyfikator
        cena_paliwa = dane["cena_paliwa"]
        zuzycie = dane["zuzycie_kwh_na_100km"] * modyfikator
        cena_kwh = dane["cena_kwh"]

        km_prad = km * udzial_prad
        km_paliwo = km - km_prad

        koszt = (
            km_prad * zuzycie / 100 * cena_kwh
            + km_paliwo * spalanie / 100 * cena_paliwa
            + oplata_stala
        )

    else:
        raise ValueError("Nieznany typ pojazdu")

    # rabat dopiero na końcu, ale czy opłata stała też ma rabat? a może nie?
    # i co z rabatami progowymi? i podatkiem? i walutą?
    koszt = koszt * (1.0 - rabat_flota)
    return koszt
