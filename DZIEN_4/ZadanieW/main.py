"""
JEDEN SPÓJNY PROGRAM: ABC + Protocol + pliki (TXT/CSV) + asocjacja + agregacja

Cel dydaktyczny (dla kursantów):
- zobaczyć PO CO jest Protocol (kontrakt zachowania bez dziedziczenia)
- zrozumieć różnicę: ABC vs Protocol
- rozdzielić logikę I/O od logiki biznesowej
- zrobić to w sposób rozszerzalny (Open/Closed)

Program:
- czyta transakcje z pliku wejściowego: CSV lub TXT
- przetwarza je (filtrowanie + statystyki)
- zapisuje raport do pliku wyjściowego (TXT)
- umożliwia łatwą rozbudowę o nowe formaty wejściowe/wyjściowe

Uruchomienie:
python program.py

W ramach demo program sam tworzy przykładowe pliki w katalogu roboczym.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Protocol, runtime_checkable
from abc import ABC, abstractmethod
import csv
from pathlib import Path


# ============================================================
# 1) MODEL DANYCH (logika biznesowa, zero I/O)
# ============================================================

@dataclass(frozen=True)
class Transaction:
    """
    Jeden rekord transakcji.
    frozen=True -> niemutowalny obiekt: bezpieczniej, prościej, mniej bugów.
    """
    tx_id: str
    category: str
    amount: float


@dataclass(frozen=True)
class Report:
    """
    Wynik przetwarzania: prosty raport statystyczny.
    To też jest logika biznesowa – nie zapisujemy tu do pliku.
    """
    total_count: int
    total_amount: float
    avg_amount: float
    by_category: dict[str, float]


# ============================================================
# 2) ABC: źródła danych (wspólne zachowanie + wymuszenie implementacji)
# ============================================================

class DataSource(ABC):
    """
    ABC (Abstract Base Class) = „sztywna” rama:
    - definiuje wymagane metody
    - nie pozwala utworzyć niekompletnej implementacji
    - dobry punkt rozszerzeń: dodajesz nowy format -> nowa klasa dziedziczy
    """

    @abstractmethod
    def read_transactions(self) -> Iterator[Transaction]:
        """
        Zwraca strumień (iterator) transakcji.
        Ważne: iterator => możemy czytać po jednej linii, bez RAM-owego „wszystko naraz”.
        """
        raise NotImplementedError


class CsvTransactionSource(DataSource):
    """
    Źródło danych: CSV.
    Uwaga dydaktyczna: tu jest czyste I/O.
    """
    def __init__(self, path: Path, delimiter: str = ","):
        self._path = path
        self._delimiter = delimiter

    def read_transactions(self) -> Iterator[Transaction]:
        # Bezpieczne otwieranie i zamykanie pliku: context manager.
        try:
            with self._path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f, delimiter=self._delimiter)

                # Streaming: yield po jednym rekordzie
                for row in reader:
                    # Walidacja minimalna: brak klucza -> KeyError -> obsłużymy wyżej albo przerwiemy
                    tx_id = row["id"].strip()
                    category = row["category"].strip()

                    # Konwersja amount: może się wywalić na ValueError
                    amount = float(row["amount"])

                    yield Transaction(tx_id=tx_id, category=category, amount=amount)

        except FileNotFoundError:
            # Podnosimy czytelny błąd domenowy dla aplikacji:
            raise FileNotFoundError(f"Nie znaleziono pliku CSV: {self._path}") from None


class TxtTransactionSource(DataSource):
    """
    Źródło danych: TXT.
    Format linii (prosty dla początkujących):
    id;category;amount
    np.  T001;food;12.50
    """
    def __init__(self, path: Path, separator: str = ";"):
        self._path = path
        self._sep = separator

    def read_transactions(self) -> Iterator[Transaction]:
        try:
            with self._path.open("r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, start=1):
                    line = line.strip()
                    if not line:
                        continue  # pomijamy puste linie

                    parts = [p.strip() for p in line.split(self._sep)]
                    if len(parts) != 3:
                        # Błąd formatu: podajemy numer linii -> łatwiejszy debug
                        raise ValueError(f"Błędny format TXT w linii {line_no}: {line!r}")

                    tx_id, category, amount_str = parts
                    amount = float(amount_str)

                    yield Transaction(tx_id=tx_id, category=category, amount=amount)

        except FileNotFoundError:
            raise FileNotFoundError(f"Nie znaleziono pliku TXT: {self._path}") from None


# ============================================================
# 3) Protocol: kontrakt „piszący raport”, bez dziedziczenia
# ============================================================

@runtime_checkable
class ReportWriter(Protocol):
    """
    Protocol = kontrakt zachowania, bez narzucania pochodzenia.

    KLUCZ:
    - Nie zmuszamy implementacji do dziedziczenia po jakiejś klasie bazowej.
    - Wymagamy tylko: „umiesz write(report)”.
    - Dzięki temu możemy:
      * wstrzyknąć prawdziwy writer (plik)
      * wstrzyknąć testowy writer (do pamięci)
      * wstrzyknąć writer logujący, sieciowy, bazodanowy itd.
    """
    def write(self, report: Report) -> None:
        ...


class TextFileReportWriter:
    """
    Konkretna implementacja: zapis raportu do pliku TXT.
    UWAGA: Nie dziedziczymy po niczym.
    I o to chodzi: Protocol ma działać przez „duck typing”.
    """
    def __init__(self, output_path: Path):
        self._output_path = output_path

    def write(self, report: Report) -> None:
        # I/O: zapis do pliku
        with self._output_path.open("w", encoding="utf-8") as f:
            f.write("=== RAPORT TRANSAKCJI ===\n")
            f.write(f"Liczba transakcji: {report.total_count}\n")
            f.write(f"Suma kwot: {report.total_amount:.2f}\n")
            f.write(f"Średnia kwota: {report.avg_amount:.2f}\n")
            f.write("\nSuma wg kategorii:\n")
            for cat, total in sorted(report.by_category.items()):
                f.write(f"  - {cat}: {total:.2f}\n")


class MemoryReportWriter:
    """
    Implementacja testowa / demonstracyjna:
    zapisuje wynik do pamięci (string), bez plików.
    To jest moment, w którym kursanci widzą PO CO Protocol.

    Bez Protocol:
    - musielibyśmy dziedziczyć po jakiejś bazie „WriterBase”
    - albo przekazywać „cokolwiek” i liczyć, że ma metodę write()
      (czyli brak bezpieczeństwa / brak komunikacji kontraktu)

    Z Protocol:
    - IDE / type checker mówią, czy obiekt pasuje do kontraktu
    - łatwo testować logikę bez I/O
    """
    def __init__(self):
        self.content: str = ""

    def write(self, report: Report) -> None:
        lines = []
        lines.append("=== RAPORT TRANSAKCJI ===")
        lines.append(f"Liczba transakcji: {report.total_count}")
        lines.append(f"Suma kwot: {report.total_amount:.2f}")
        lines.append(f"Średnia kwota: {report.avg_amount:.2f}")
        lines.append("Suma wg kategorii:")
        for cat, total in sorted(report.by_category.items()):
            lines.append(f"  - {cat}: {total:.2f}")
        self.content = "\n".join(lines)


# ============================================================
# 4) Procesor danych: czysta logika biznesowa (bez plików)
# ============================================================

class TransactionProcessor:
    """
    Klasa przetwarzająca dane.
    Ona NIE czyta plików i NIE zapisuje plików.
    Dostaje iterator Transaction i zwraca Report.

    To jest fundament „oddziel logikę biznesową od I/O”.
    """

    def __init__(self, min_amount: float = 0.0):
        # np. filtr: ignoruj transakcje poniżej jakiegoś progu
        self._min_amount = min_amount

    def build_report(self, transactions: Iterable[Transaction]) -> Report:
        total_count = 0
        total_amount = 0.0
        by_category: dict[str, float] = {}

        # streaming: iterujemy po wejściu, nie trzymamy całej listy
        for tx in transactions:
            if tx.amount < self._min_amount:
                continue

            total_count += 1
            total_amount += tx.amount
            by_category[tx.category] = by_category.get(tx.category, 0.0) + tx.amount

        avg_amount = (total_amount / total_count) if total_count else 0.0

        return Report(
            total_count=total_count,
            total_amount=total_amount,
            avg_amount=avg_amount,
            by_category=by_category
        )


# ============================================================
# 5) Orkiestrator: asocjacja + agregacja
# ============================================================

class Pipeline:
    """
    Pipeline zarządza przepływem: źródła -> procesor -> writer.

    W tym miejscu celowo pokazujemy:
    - ASOCJACJĘ: Pipeline współpracuje z writerem (ReportWriter),
      ale Pipeline NIE tworzy writera i NIE jest jego właścicielem.
      Writer może istnieć niezależnie, może być podmieniony.

    - AGREGACJĘ: Pipeline ma kolekcję źródeł danych (DataSource).
      Źródła są niezależnymi obiektami, mogą istnieć poza Pipeline.
      Pipeline tylko je „używa jako zbioru”.
    """

    def __init__(self, writer: ReportWriter, processor: TransactionProcessor):
        # Asocjacja: trzymamy referencję do obiektu z zewnątrz
        self._writer = writer
        self._processor = processor

        # Agregacja: kolekcja źródeł (nie tworzymy ich tu na sztywno)
        self._sources: list[DataSource] = []

    def add_source(self, source: DataSource) -> None:
        # Pipeline nie przejmuje „własności” w sensie cyklu życia.
        self._sources.append(source)

    def run(self) -> Report:
        """
        Wykonuje cały pipeline:
        - czyta dane ze wszystkich źródeł
        - buduje raport
        - zapisuje raport przez writer
        """
        # Łączymy strumienie z wielu źródeł w jeden iterator.
        transactions_stream = self._merge_sources()

        # Logika biznesowa: budujemy raport
        report = self._processor.build_report(transactions_stream)

        # I/O: zapis raportu, ale przez Protocol, bez „sztywnej” zależności od klasy plikowej
        self._writer.write(report)

        return report

    def _merge_sources(self) -> Iterator[Transaction]:
        """
        Generator: scala dane ze źródeł, nadal streamingowo.
        """
        for src in self._sources:
            yield from src.read_transactions()


# ============================================================
# 6) Demo / Main: tworzymy przykładowe pliki i uruchamiamy program
# ============================================================

def _create_demo_files(base_dir: Path) -> tuple[Path, Path]:
    """
    Tworzymy minimalne przykładowe dane.
    Dzięki temu kursanci mogą uruchomić program od razu.
    """
    csv_path = base_dir / "transactions.csv"
    txt_path = base_dir / "transactions.txt"

    csv_content = [
        {"id": "C001", "category": "food", "amount": "12.50"},
        {"id": "C002", "category": "fuel", "amount": "210.00"},
        {"id": "C003", "category": "food", "amount": "8.90"},
        {"id": "C004", "category": "books", "amount": "55.00"},
    ]

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "category", "amount"])
        writer.writeheader()
        writer.writerows(csv_content)

    txt_lines = [
        "T001;food;19.99",
        "T002;fuel;180.00",
        "T003;tools;39.50",
        "T004;food;3.20",
    ]
    txt_path.write_text("\n".join(txt_lines), encoding="utf-8")

    return csv_path, txt_path


def main() -> None:
    """
    Tu widać „sklejanie systemu”:
    - wybieramy źródła (ABC)
    - wybieramy writer (Protocol)
    - wybieramy processor (logika)
    - uruchamiamy pipeline

    To miejsce jest proste i czytelne: to jest cel architektury.
    """
    base_dir = Path(".").resolve()
    csv_path, txt_path = _create_demo_files(base_dir)

    # Writer: wybieramy implementację plikową
    out_path = base_dir / "report.txt"
    file_writer = TextFileReportWriter(out_path)

    # Processor: np. filtrujemy mikrotransakcje < 10
    processor = TransactionProcessor(min_amount=10.0)

    # Pipeline: asocjacja (writer), agregacja (źródła)
    pipeline = Pipeline(writer=file_writer, processor=processor)

    pipeline.add_source(CsvTransactionSource(csv_path))
    pipeline.add_source(TxtTransactionSource(txt_path))

    report = pipeline.run()

    print("Pipeline ukończony ✅")
    print(f"Zapisano raport do: {out_path}")
    print(f"Suma kwot (po filtrze >= 10): {report.total_amount:.2f}")

    # --- DEMO: dlaczego Protocol jest „prawie niezbędny” ---
    # Podmieniamy writer na MemoryReportWriter bez ruszania Pipeline.
    # To jest nieosiągalne w tak prosty sposób, jeśli wymusisz dziedziczenie bazowe.
    mem_writer = MemoryReportWriter()
    pipeline2 = Pipeline(writer=mem_writer, processor=processor)
    pipeline2.add_source(CsvTransactionSource(csv_path))
    pipeline2.add_source(TxtTransactionSource(txt_path))
    pipeline2.run()

    print("\n--- Raport w pamięci (bez plików) ---")
    print(mem_writer.content)

    # Dodatkowo: runtime_checkable pozwala pokazać kursantom, że obiekt spełnia Protocol
    print("\nCzy file_writer spełnia ReportWriter?", isinstance(file_writer, ReportWriter))
    print("Czy mem_writer spełnia ReportWriter?", isinstance(mem_writer, ReportWriter))


if __name__ == "__main__":
    main()
