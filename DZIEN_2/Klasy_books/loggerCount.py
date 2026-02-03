import dis

class BaseCounter:
    def __init__(self):
        self.__count = 0

    def inc(self):
        self.__count += 1

    def value(self):
        return self.__count

#programista myśli  __count jest nie do ruszenia!

class LoggingCounter(BaseCounter):
    def __init__(self):
        super().__init__()
        self.__count = 100 #ustawienie startowej wartości

    def inc(self):
        print("Inkrementacja...")
        super().inc()

c = LoggingCounter()
c.inc()
print(c.value()) #oczekiwanie -> 101

#bytecode
print(dis.dis(BaseCounter.inc))
print("_"*70)
print(dis.dis(LoggingCounter.inc))