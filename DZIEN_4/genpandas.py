from __future__ import annotations

import os
import time
from pathlib import Path

import numpy as np
import pandas as pd


def generate_big_df(n_rows: int = 1_000_000, seed: int = 42) -> pd.DataFrame:
    """
    Generuje dużą ramkę danych w sposób wektorowy (szybko),
    bez pętli for po wierszach.

    Kolumny:
    - id: rosnący identyfikator
    - ts: daty (co minutę)
    - category: kategoria losowana z kilku wartości
    - amount: kwota (rozkład lognormalny)
    - score: liczba zmiennoprzecinkowa
    - flag: bool
    """
    rng = np.random.default_rng(seed)

    categories = np.array(["food", "fuel", "books", "tools", "travel", "other"])

    df = pd.DataFrame(
        {
            "id": np.arange(1, n_rows + 1, dtype=np.int64),
            "ts": pd.date_range("2024-01-01", periods=n_rows, freq="min"),
            "category": rng.choice(categories, size=n_rows, replace=True),
            "amount": rng.lognormal(mean=3.2, sigma=0.7, size=n_rows).round(2),
            "score": rng.random(n_rows, dtype=np.float64),
            "flag": rng.random(n_rows) < 0.05,
        }
    )

    # Drobna optymalizacja pamięci: category jako typ kategoryczny
    df["category"] = df["category"].astype("category")

    return df


def timed_save(label: str, func) -> None:
    """
    Mała pomocnicza funkcja: mierzy czas zapisu.
    """
    t0 = time.perf_counter()
    func()
    t1 = time.perf_counter()
    print(f"{label:12s} -> {t1 - t0:.2f}s")


def main():
    out_dir = Path("pandas_exports")
    out_dir.mkdir(exist_ok=True)

    n = 1_000_000  # zmień na 5_000_000 jeśli masz mocny sprzęt
    print(f"Generuję DataFrame: {n:,} wierszy...")
    df = generate_big_df(n_rows=n)

    print(df.head())
    print("Memory usage (MB):", df.memory_usage(deep=True).sum() / (1024**2))

    # ---------------------------------------------------------
    # 1) CSV - uniwersalny, ale duży i wolniejszy
    # ---------------------------------------------------------
    csv_path = out_dir / "data.csv"
    timed_save("CSV", lambda: df.to_csv(csv_path, index=False))

    # CSV skompresowany (często sensowny kompromis)
    csv_gz_path = out_dir / "data.csv.gz"
    timed_save("CSV.GZ", lambda: df.to_csv(csv_gz_path, index=False, compression="gzip"))

    # ---------------------------------------------------------
    # 2) Parquet - najlepszy do analytics (kolumnowy, kompresja)
    # Wymaga pyarrow albo fastparquet
    # ---------------------------------------------------------
    parquet_path = out_dir / "data.parquet"
    try:
        timed_save("Parquet", lambda: df.to_parquet(parquet_path, index=False))
    except Exception as e:
        print("Parquet pominięty (brak pyarrow/fastparquet?):", repr(e))

    # ---------------------------------------------------------
    # 3) Feather - bardzo szybki zapis/odczyt (kolumnowy)
    # Wymaga pyarrow
    # ---------------------------------------------------------
    feather_path = out_dir / "data.feather"
    try:
        timed_save("Feather", lambda: df.to_feather(feather_path))
    except Exception as e:
        print("Feather pominięty (brak pyarrow?):", repr(e))

    # ---------------------------------------------------------
    # 4) Pickle - Python-only (nie dla wymiany z innymi językami)
    # ---------------------------------------------------------
    pkl_path = out_dir / "data.pkl"
    timed_save("Pickle", lambda: df.to_pickle(pkl_path))

    # ---------------------------------------------------------
    # 5) Excel - raczej do małych danych (limit wierszy ~1,048,576)
    # Tu uważaj: 1 mln wierszy to granica. Lepiej dać mniejsze n.
    # ---------------------------------------------------------
    xlsx_path = out_dir / "data.xlsx"
    if len(df) <= 1_048_000:  # zostawiamy margines
        timed_save("Excel", lambda: df.to_excel(xlsx_path, index=False))
    else:
        print("Excel pominięty (za dużo wierszy).")

    # ---------------------------------------------------------
    # 6) JSON - do API/transferu, ale duży i wolniejszy
    # ---------------------------------------------------------
    json_path = out_dir / "data.jsonl"
    # JSON Lines: jedna linia = jeden rekord, dobry do streamingu
    timed_save(
        "JSONL",
        lambda: df.to_json(json_path, orient="records", lines=True, force_ascii=False),
    )

    # Podsumowanie: rozmiary plików
    print("\nRozmiary plików:")
    for p in sorted(out_dir.glob("data.*")):
        size_mb = p.stat().st_size / (1024**2)
        print(f"{p.name:15s} {size_mb:8.1f} MB")


if __name__ == "__main__":
    main()
