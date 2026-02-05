"""
xml_countries_viewer.py

Czyta plik XML z krajami i pokazuje:
1) listę krajów z danymi (wraz z atrybutami tagów, np. country/@continent, neighbour/@direction),
2) ramkę pandas.DataFrame, gdzie wierszem jest country.

Uruchomienie:
    python xml_countries_viewer.py /ścieżka/do/pliku.xml

Jeśli nie podasz ścieżki, program użyje: kraj.xml (jeśli istnieje obok skryptu).
"""

from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET

import pandas as pd


def parse_countries(xml_file: Path) -> tuple[list[dict], pd.DataFrame]:
    """
    Zwraca:
      - countries: list[dict] z pełnym opisem każdego <country> (w tym listą neighbourów)
      - df: DataFrame z indeksem = nazwa kraju
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    countries: list[dict] = []

    # Każdy <country> ma atrybuty (name, continent) i podtagi (<id>, <rok>, <wartP>, <neighbour .../>)
    for c in root.findall(".//country"):
        # --- Atrybuty tagu <country> (parametry wewnątrz tagów) ---
        country_name = c.get("name")
        continent = c.get("continent")

        record: dict = {
            "country": country_name,
            "continent": continent,
        }

        # --- Proste podtagi tekstowe (np. <id>1</id>) ---
        # Zbieramy wszystkie dzieci poza neighbour (bo neighbour jest "rekordem" z atrybutami)
        for child in c:
            if child.tag == "neighbour":
                continue
            record[child.tag] = (child.text or "").strip()

        # --- Neighbours: atrybuty wewnątrz <neighbour name="..." direction="..."/> ---
        neighbours: list[dict] = []
        for n in c.findall("neighbour"):
            neighbours.append(
                {
                    "name": n.get("name"),
                    "direction": n.get("direction"),
                }
            )

        record["neighbours"] = neighbours
        record["neighbour_count"] = len(neighbours)

        # Dodatkowe kolumny "wygodne do analizy/wyświetlania"
        record["neighbour_names"] = ", ".join([n["name"] for n in neighbours if n.get("name")])
        record["neighbour_pairs"] = "; ".join(
            [f'{n["name"]}({n["direction"]})' for n in neighbours if n.get("name")]
        )

        countries.append(record)

    df = pd.DataFrame(countries).set_index("country").sort_index()
    return countries, df


def pretty_print_countries(countries: list[dict]) -> None:
    """Czytelny wydruk listy krajów (JSON z wcięciami)."""
    print("=== LISTA KRAJÓW (list[dict]) ===")
    print(json.dumps(countries, ensure_ascii=False, indent=2))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Wyświetla kraje z pliku XML jako listę i DataFrame.")
    parser.add_argument(
        "xml_path",
        nargs="?",
        default=None,
        help="Ścieżka do pliku XML (opcjonalnie).",
    )
    args = parser.parse_args()

    # Domyślna ścieżka: plik 'kraj.xml' obok skryptu, jeśli użytkownik nie poda argumentu
    script_dir = Path(__file__).resolve().parent
    default_xml = script_dir / "kraj.xml"

    xml_file = Path(args.xml_path).expanduser().resolve() if args.xml_path else default_xml

    if not xml_file.exists():
        raise FileNotFoundError(
            f"Nie znaleziono pliku XML: {xml_file}\n"
            f"Podaj poprawną ścieżkę, np.: python {Path(__file__).name} /path/to/file.xml"
        )

    countries, df = parse_countries(xml_file)

    # 1) lista krajów z danymi (w tym atrybuty)
    pretty_print_countries(countries)

    # 2) DataFrame
    print("\n=== DATAFRAME (wiersz = country) ===")
    # print(df) pokazuje całą ramkę w konsoli
    print(df.to_string())
    df.to_html("countries.html")


if __name__ == "__main__":
    main()
