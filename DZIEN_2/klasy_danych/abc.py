class abc:
    def abc(self):
        return 1
    def klasydanych(self):
        return 2


a = abc()
print(a.abc())
print(a)
klasydanych = abc()
print(klasydanych)

#to jest bardzo zła praktyka - nadawanie tych samych nazw różnym obiektom

abc = abc()
print(abc.klasydanych())

c= abc()