import xml.sax
from dataclasses import dataclass


@dataclass
class Transaction:
    tx_id: str
    category: str
    amount: float
    currency: str


class TransactionHandler(xml.sax.ContentHandler):
    """
    ContentHandler to zestaw callbacków (haków), które parser wywołuje podczas czytania XML.

    Najważniejsze callbacki:
    - startElement(name, attrs): gdy parser widzi <tag ...>
    - characters(content): gdy parser widzi tekst pomiędzy tagami
    - endElement(name): gdy parser widzi </tag>
    """

    def __init__(self):
        super().__init__()

        # Gdzie jesteśmy w dokumencie (jaki element aktualnie czytamy)
        self.current_tag = None

        # Bufor na tekst, bo SAX może podać tekst w kawałkach:
        # characters() może zostać wywołane kilka razy dla jednego elementu
        self.text_buffer = []

        # Dane „w trakcie składania” dla jednej transakcji
        self._tx_id = None
        self._category = None
        self._amount = None
        self._currency = None

        # Wynik: lista transakcji (w realnym streamingu mógłbyś yieldować / liczyć statystyki)
        self.transactions = []

    def startElement(self, name, attrs):
        # Parser widzi <name ...>
        self.current_tag = name
        self.text_buffer.clear()  # zaczynamy zbierać tekst dla danego tagu

        if name == "transaction":
            # atrybuty są w attrs (map-like)
            self._tx_id = attrs.get("id")
            # reset pól transakcji
            self._category = None
            self._amount = None
            self._currency = None

        elif name == "amount":
            # amount ma atrybut currency="PLN"
            self._currency = attrs.get("currency", "")

    def characters(self, content):
        # Tekst pomiędzy tagami: może przychodzić po kawałku
        if self.current_tag in {"category", "amount"}:
            self.text_buffer.append(content)

    def endElement(self, name):
        # Parser widzi </name> i to jest najlepszy moment, by "zamknąć" element.
        text = "".join(self.text_buffer).strip()

        if name == "category":
            self._category = text

        elif name == "amount":
            # konwersja do float (tu może polecieć ValueError, jeśli XML jest błędny)
            self._amount = float(text)

        elif name == "transaction":
            # Koniec transakcji: składamy obiekt i odkładamy do wyniku
            tx = Transaction(
                tx_id=self._tx_id or "",
                category=self._category or "",
                amount=float(self._amount or 0.0),
                currency=self._currency or ""
            )
            self.transactions.append(tx)

        # czyścimy stan tagu i bufor
        self.current_tag = None
        self.text_buffer.clear()


def parse_transactions(xml_path: str) -> list[Transaction]:
    """
    Funkcja pomocnicza: odpala parser SAX z naszym handlerem.
    """
    handler = TransactionHandler()
    xml.sax.parse(xml_path, handler)
    return handler.transactions


if __name__ == "__main__":
    # Zmień na swoją ścieżkę pliku XML
    transactions = parse_transactions("transactions.xml")

    for t in transactions:
        print(t)

    total = sum(t.amount for t in transactions)
    print("Suma:", total)
