class A:
    pass

class B:
    pass

class C(B,A):
    pass


print(C.__mro__)

print("_"*8)

#klasa bazowa
class Processor:
    def process(self, data):
        print("Processor: prztwarzam dane")
        return data**2-1

#klasa Mixin - doklejana umiejętnośc
class LogMixin:
    def process(self, data):
        print("LogMixin: START")
        result = super().process(data)
        print("LogMixin: END")
        return result

#klasa końcowa
class MyProcessor(LogMixin,Processor):
    pass

p = MyProcessor()
print(p.process(3))