class Temperature:
    def __init__(self, celsius):
        self._celsius = None
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError('Temperature below absolute zero')
        self._celsius = float(value)

    @property
    def kelvin(self):
        return self.celsius + 273.15

t = Temperature(20)
print(t.celsius)
print(t.kelvin)

t.celsius = -170
print(t.celsius)
print(t._celsius) # self._celsius  --> self.Temperature__.celsius
