from figura import Figura
from kwadrat import Kwadrat

class Prostokat(Figura):
    def __new__(cls, a, b):
        if a == b:
            return Kwadrat(bok=a)
        return object.__new__(Prostokat)
    
    def oblicz_pole(self):
        return self.a * self.b
        
