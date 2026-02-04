from abc import ABC, abstractmethod

class Figura(ABC):
    
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    @abstractmethod
    def oblicz_pole(self):
        pass
