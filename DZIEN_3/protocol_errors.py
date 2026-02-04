"""
DEMO: PO CO JEST PROTOCOL (A NIE ABC)
====================================


"""

# =========================================================
# ETAP 1: PROBLEM – BRAK PROTOCOL (duck typing bez kontroli)
# =========================================================

def zaplac_bez_protocol(gateway):
    # Python NIE WIE, czego oczekujemy od gateway
    gateway.pay(100)


class PayPal:
    def pay(self, amount):
        print(f"[PayPal] Zapłacono {amount}")


class Stripe:
    def pey(self, amount):  # literówka
        print(f"[Stripe] Zapłacono {amount}")


def demo_bez_protocol():
    print("\n=== DEMO 1: Bez Protocol ===")
    zaplac_bez_protocol(PayPal())

    try:
        zaplac_bez_protocol(Stripe())  # runtime error
    except AttributeError as e:
        print("BŁĄD RUNTIME:", e)


# =========================================================
# ETAP 2: TEN SAM KOD, ALE Z PROTOCOL
# =========================================================

from typing import Protocol


class PaymentGateway(Protocol):
    def pay(self, amount: float) -> None:
        ...


def zaplac_z_protocol(gateway: PaymentGateway):
    gateway.pay(100)


def demo_z_protocol():
    print("\n=== DEMO 2: Z Protocol ===")
    zaplac_z_protocol(PayPal())

    # UWAGA DYDAKTYCZNA:
    # Ten kod URUCHOMI SIĘ w runtime,
    # ale IDE / mypy / pyright ZGŁOSI BŁĄD WCZEŚNIEJ.
    #
    # zaplac_z_protocol(Stripe())  # <- IDE krzyczy


# =========================================================
# ETAP 3: TESTY – Fake bez dziedziczenia
# =========================================================

class FakeGateway:
    def __init__(self):
        self.called_with = None

    def pay(self, amount: float) -> None:
        self.called_with = amount


def demo_test():
    print("\n=== DEMO 3: Test z FakeGateway ===")
    fake = FakeGateway()
    zaplac_z_protocol(fake)

    assert fake.called_with == 100
    print("TEST OK – zapłata wywołana z kwotą:", fake.called_with)


# =========================================================
# ETAP 4: OBCY KOD (nie możesz zmienić klasy)
# =========================================================

class ExternalGateway:
    # Wyobraź sobie: kod z zewnętrznej biblioteki
    def pay(self, amount):
        print(f"[External] Zapłacono {amount}")


def demo_external():
    print("\n=== DEMO 4: Obcy kod ===")
    zaplac_z_protocol(ExternalGateway())  # działa + jest typowane


# =========================================================
# ETAP 5: KONTRAST – ABC (krótko, dla porównania)
# =========================================================

from abc import ABC, abstractmethod


class GatewayABC(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


# class BadGateway(GatewayABC):
#     pass
#
# Tego nie da się nawet uruchomić – ABC BLOKUJE runtime


# =========================================================
# MAIN – uruchamiamy wszystko po kolei
# =========================================================

def main():
    demo_bez_protocol()
    demo_z_protocol()
    demo_test()
    demo_external()

    print("\n=== PODSUMOWANIE ===")
    print(
        "Protocol:\n"
        "- NIE blokuje runtime\n"
        "- DAJE kontrakt dla IDE i type-checkerów\n"
        "- POZWALA na testy i integrację z obcym kodem\n"
        "- NIE wymusza dziedziczenia\n"
    )


if __name__ == "__main__":
    main()
