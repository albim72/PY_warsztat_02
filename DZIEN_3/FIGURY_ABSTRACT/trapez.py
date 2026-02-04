from figura import Figura

class Trapez(Figura):
    def __init__(self, a, b, h):
        super().__init__(a,b)
        self.h = h

    def oblicz_pole(self):
        return (self.a + self.b) * self.h / 2
