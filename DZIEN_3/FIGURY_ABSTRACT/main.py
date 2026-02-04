from trojkat import Trojkat
from prostokat import Prostokat

tr = Trojkat(5,7)
print(f"pole figry: {tr.__class__.__name__} wynosi: {tr.oblicz_pole():.2f} cm2")

pr1 = Prostokat(3.5,4.7)
print(f"pole figry: {pr1.__class__.__name__} wynosi: {pr1.oblicz_pole():.2f} cm2")
print(f"typ obiektu pr1: {type(pr1)}")

pr2 = Prostokat(5.1,5.1)
print(f"pole figry: {pr2.__class__.__name__} wynosi: {pr2.oblicz_pole():.2f} cm2")
print(f"typ obiektu pr2: {type(pr2)}")
