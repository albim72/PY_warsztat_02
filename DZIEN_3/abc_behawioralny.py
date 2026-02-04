# ========= abstrkcja behawioralna ==========
def wykonaj_symulacje(silnik):
    """
    Abstrakcja: obiekt musi posiada metodę uruchom()
    :param silnik:
    :return:
    """
    return silnik.uruchom()

# ========= RÓŻNE IMPLEMENTACJE ===========
class SilnikLosowy:
    def uruchom(self):
        return "uruchomiono silnik losowy"

class SilnikDeterministyczny:
    def uruchom(self):
        return "uruchomiono silnik deterministyczny"

class SilnikTestowy:
    def uruchom(self):
        return "uruchomiono silnik testowy"

# ======= uruchomnienie ==========

silniki = [SilnikLosowy(), SilnikDeterministyczny(), SilnikTestowy()]

for silnik in silniki:
    print(wykonaj_symulacje(silnik))

