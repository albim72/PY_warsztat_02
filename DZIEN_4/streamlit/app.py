from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# =========================
# 1) USTAWIENIA APLIKACJI
# =========================
st.set_page_config(
    page_title="Data Observatory (Streamlit)",
    page_icon="📡",
    layout="wide"
)

st.title("Data Observatory")
st.caption("Mini-dashboard: generowanie danych / upload CSV, filtry, KPI, wykresy, heatmapa, eksport.")

# =========================
# 2) GENEROWANIE DANYCH (cache)
# =========================
@st.cache_data(show_spinner=False)
def generate_data(n_rows: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    categories = np.array(["food", "fuel", "books", "tools", "travel", "other"])
    cities = np.array(["Warszawa", "Kraków", "Gdańsk", "Wrocław", "Poznań"])

    # Oś czasu (minuty)
    ts = pd.date_range("2026-01-01", periods=n_rows, freq="min")

    df = pd.DataFrame({
        "id": np.arange(1, n_rows + 1, dtype=np.int64),
        "ts": ts,
        "category": rng.choice(categories, size=n_rows),
        "city": rng.choice(cities, size=n_rows),
        "amount": rng.lognormal(mean=3.1, sigma=0.8, size=n_rows).round(2),
        "flag": (rng.random(n_rows) < 0.07),
    })

    # Dodatkowe kolumny do analityki
    df["date"] = df["ts"].dt.date
    df["hour"] = df["ts"].dt.hour
    df["weekday"] = df["ts"].dt.day_name()

    # Lekka „anomalizacja” (żeby były outliery, a dashboard wyglądał ciekawiej)
    bump_idx = rng.choice(n_rows, size=max(10, n_rows // 5000), replace=False)
    df.loc[bump_idx, "amount"] = (df.loc[bump_idx, "amount"] * rng.uniform(8, 20, size=len(bump_idx))).round(2)

    return df


# =========================
# 3) SIDEBAR: ŹRÓDŁO DANYCH + FILTRY
# =========================
st.sidebar.header("Źródło danych")

mode = st.sidebar.radio("Dane", ["Generuj (demo)", "Wgraj CSV"], index=0)

if mode == "Wgraj CSV":
    uploaded = st.sidebar.file_uploader("Wgraj plik CSV", type=["csv"])
    if uploaded is None:
        st.info("Wgraj CSV, albo przełącz na tryb generowania danych.")
        st.stop()

    # Prosty odczyt: oczekujemy kolumn minimum: ts, category, amount (city opcjonalnie)
    df = pd.read_csv(uploaded)

    # Próba konwersji czasu (jeśli jest)
    if "ts" in df.columns:
        df["ts"] = pd.to_datetime(df["ts"], errors="coerce")
        df = df.dropna(subset=["ts"])
        df["date"] = df["ts"].dt.date
        df["hour"] = df["ts"].dt.hour
        df["weekday"] = df["ts"].dt.day_name()
    else:
        # Jeśli nie ma czasu, tworzymy sztuczny
        df["ts"] = pd.date_range("2026-01-01", periods=len(df), freq="min")
        df["date"] = df["ts"].dt.date
        df["hour"] = df["ts"].dt.hour
        df["weekday"] = df["ts"].dt.day_name()

    # Bezpieczne minimum
    if "category" not in df.columns or "amount" not in df.columns:
        st.error("CSV musi mieć kolumny: category, amount. (ts opcjonalnie)")
        st.stop()

    if "city" not in df.columns:
        df["city"] = "N/A"

else:
    n_rows = st.sidebar.slider("Liczba wierszy", 50_000, 500_000, 150_000, step=50_000)
    seed = st.sidebar.number_input("Seed", min_value=0, max_value=9999, value=42, step=1)
    df = generate_data(n_rows, seed)

st.sidebar.header("Filtry")

categories = ["ALL"] + sorted(df["category"].astype(str).unique().tolist())
cities = ["ALL"] + sorted(df["city"].astype(str).unique().tolist())

cat = st.sidebar.selectbox("Kategoria", categories, index=0)
city = st.sidebar.selectbox("Miasto", cities, index=0)

min_amount, max_amount = float(df["amount"].min()), float(df["amount"].max())
amount_range = st.sidebar.slider("Kwota (amount)", min_amount, max_amount, (min_amount, max_amount))

flag_only = st.sidebar.checkbox("Tylko flag=True (np. podejrzane)", value=False)

# =========================
# 4) APLIKACJA FILTRÓW
# =========================
f = df.copy()

if cat != "ALL":
    f = f[f["category"].astype(str) == cat]
if city != "ALL":
    f = f[f["city"].astype(str) == city]

f = f[(f["amount"] >= amount_range[0]) & (f["amount"] <= amount_range[1])]

if flag_only:
    f = f[f["flag"] == True]

if len(f) == 0:
    st.warning("Po filtrach nie ma danych. Zmień filtry.")
    st.stop()

# =========================
# 5) KPI (NA GÓRZE)
# =========================
col1, col2, col3, col4 = st.columns(4)

total = f["amount"].sum()
avg = f["amount"].mean()
count = len(f)
p95 = np.percentile(f["amount"], 95)

col1.metric("Suma", f"{total:,.2f}")
col2.metric("Średnia", f"{avg:,.2f}")
col3.metric("Liczba rekordów", f"{count:,}")
col4.metric("95 percentyl", f"{p95:,.2f}")

st.divider()

# =========================
# 6) WIDOK: wykresy i tabela
# =========================
left, right = st.columns([1.2, 1])

# ---- 6a) Ranking kategorii
rank = (
    f.groupby("category", as_index=False)["amount"]
     .sum()
     .sort_values("amount", ascending=False)
)

fig_rank = px.bar(
    rank,
    x="category",
    y="amount",
    title="Suma kwot per kategoria",
)
left.plotly_chart(fig_rank, use_container_width=True)

# ---- 6b) Time series: suma per dzień
daily = (
    f.groupby("date", as_index=False)["amount"]
     .sum()
     .sort_values("date")
)
fig_ts = px.line(
    daily,
    x="date",
    y="amount",
    title="Suma kwot w czasie (per dzień)",
)
right.plotly_chart(fig_ts, use_container_width=True)

# ---- 6c) Heatmap: dzień tygodnia x godzina
st.subheader("Heatmapa: tydzień × godzina (średnia kwota)")
pivot = (
    f.pivot_table(index="weekday", columns="hour", values="amount", aggfunc="mean")
)

# uporządkuj dni tygodnia (estetyka)
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
pivot = pivot.reindex([d for d in weekday_order if d in pivot.index])

fig_heat = px.imshow(
    pivot,
    aspect="auto",
    title="Średnia kwota (amount) w zależności od dnia tygodnia i godziny",
)
st.plotly_chart(fig_heat, use_container_width=True)

# ---- 6d) Outliery: top 30 transakcji
st.subheader("🪨 Outliery: największe kwoty")
top = f.sort_values("amount", ascending=False).head(30)
st.dataframe(top, use_container_width=True, height=280)

# ---- 6e) Eksport filtrowanych danych
st.subheader("⬇️ Eksport")
csv_bytes = f.to_csv(index=False).encode("utf-8")
st.download_button(
    "Pobierz filtrowane dane (CSV)",
    data=csv_bytes,
    file_name="filtered_data.csv",
    mime="text/csv"
)

st.caption("Tip: Streamlit jest idealny do szybkich dashboardów demo i aplikacji AI/BI bez pisania frontendu.")
