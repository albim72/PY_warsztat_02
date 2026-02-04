from abc import ABC,abstractmethod

class Figura(ABC):
    def __init__(self,a,b=None):
        self.a=a
        if b:
            self.b=b
        self.info()

    @abstractmethod
    def oblicz_pole(self):
        pass

    def info(self):
        print(f"Figura  oparta na bazowych prametrach własnych")
