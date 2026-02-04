from abc import ABC, abstractmethod

class Figura(ABC):

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.info()

    @abstractmethod
    def oblicz_pole(self):
        pass
    
    def info(self):
        print(f"Figura  oparta na bazowych prametrach: a = {self.a}, b = {self.b}")
