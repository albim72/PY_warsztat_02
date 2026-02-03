#przykład problematyczny
class A:
    def __init__(self):
        self.value=10

class B(A):
    def __init__(self):

        self.value=20

oba = A()
print(oba.value)

obb = B()
print(oba.value)

print(oba.__dict__)
print(obb.__dict__)

#przykład z __nazwa
class C:
    def __init__(self):
        self.__value=10

class D(A):
    def __init__(self):
        # super().__init__()
        self.__value=20

obc = C()
print(obc.__dict__)
obd = D()
print(obd.__dict__)

# print(obd.value)
print(obd._D__value)