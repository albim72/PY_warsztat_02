import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, HoverTool, Slider, Select
from bokeh.plotting import figure

# --------- Koncepcja ----------
# Generujemy "chmurę" punktów z parametrem czasu t (0..T).
# Bokeh serwer daje:
# - suwak czasu
# - filtr kategorii
# - hover z danymi
# - zoom/pan w przeglądarce
#
# To wygląda jak mini-dashboard analityczny, ale jest też widowiskowe.

rng = np.random.default_rng(123)

N = 8000
T = 200  # liczba kroków czasu

categories = np.array(["food", "fuel", "books", "tools", "travel", "other"])
cat = rng.choice(categories, size=N)

# Dla każdego punktu: "orbitalny" ruch w czasie
base_r = rng.uniform(0.1, 1.0, size=N)
omega  = rng.uniform(0.5, 3.5, size=N) * rng.choice([-1, 1], size=N)
phase  = rng.uniform(0, 2*np.pi, size=N)

# "Wartość" jak w danych biznesowych
amount = rng.lognormal(mean=3.1, sigma=0.7, size=N)

# Precompute pozycji dla wielu t (żeby suwak był natychmiastowy)
# x[t, i], y[t, i]
ts = np.linspace(0, 18, T)
x_all = np.empty((T, N), dtype=np.float32)
y_all = np.empty((T, N), dtype=np.float32)

for ti, t in enumerate(ts):
    r = base_r * (0.78 + 0.22*np.sin(2*np.pi*(0.12*t + base_r)))
    theta = phase + omega * t
    x_all[ti] = (r * np.cos(theta)).astype(np.float32)
    y_all[ti] = (r * np.sin(theta)).astype(np.float32)

# Start od t=0
t0 = 0

source = ColumnDataSource(data=dict(
    x=x_all[t0],
    y=y_all[t0],
    category=cat,
    amount=amount,
))

p = figure(
    title="Data Nebula (Bokeh Server) – hover, zoom, filtr, czas",
    width=900,
    height=700,
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

# Punkty: rozmiar zależy od amount (ale delikatnie)
# Bokeh wymaga kolumny rozmiaru, więc tworzymy ją dynamicznie
size = 4 + 8 * (amount / np.percentile(amount, 95))
source.data["size"] = np.clip(size, 3, 12)

r = p.scatter(
    x="x", y="y",
    size="size",
    alpha=0.55,
    source=source,
)

p.add_tools(HoverTool(
    tooltips=[
        ("category", "@category"),
        ("amount", "@amount{0.00}"),
        ("x", "@x{0.000}"),
        ("y", "@y{0.000}"),
    ],
    renderers=[r]
))

p.xaxis.visible = False
p.yaxis.visible = False
p.grid.visible = False

time_slider = Slider(title="Czas (krok)", start=0, end=T-1, value=0, step=1)
cat_select = Select(title="Filtr kategorii", value="ALL", options=["ALL", *list(categories)])

def apply_filter(cat_value: str):
    # Filtrujemy dane przez maskę, ale zachowujemy płynność
    if cat_value == "ALL":
        mask = np.ones(N, dtype=bool)
    else:
        mask = (cat == cat_value)

    return mask

def update():
    t = time_slider.value
    mask = apply_filter(cat_select.value)

    # Aktualizacja ColumnDataSource: tylko dane przefiltrowane
    new_data = dict(
        x=x_all[t][mask],
        y=y_all[t][mask],
        category=cat[mask],
        amount=amount[mask],
        size=np.clip(source.data["size"][mask], 3, 12),
    )
    source.data = new_data

def on_slider(attr, old, new):
    update()

def on_select(attr, old, new):
    update()

time_slider.on_change("value", on_slider)
cat_select.on_change("value", on_select)

curdoc().add_root(column(row(time_slider, cat_select), p))
curdoc().title = "Bokeh Data Nebula"
