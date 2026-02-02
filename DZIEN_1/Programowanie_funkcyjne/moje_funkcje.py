# przykład 1  - funkcje wyższego rzędu
def witaj(imie):
    return f"witaj {imie}!"

def konkurs(imie,miejsce,punkty):
    return f"uczestnik konkursu: {imie}, miejsce: {miejsce}, punkty: {punkty}"

def bonus(punkty):
    if punkty > 50:
        bn = punkty+10
    else:
        bn = punkty
    return f'liczba punktów z bonusem: {bn}'

def multiosoba(*args):
    return f"opublikowane wyniki konkursu! {bonus(args[1])}, {konkurs(*args)}"


#funkcja wyższego rzędu
def osoba(funkcja,*args):
    return funkcja(*args)

print(osoba(witaj,"Jan"))
print(osoba(konkurs,"Aga",34,45))
print(osoba(multiosoba,"Jan",70,45))

# przykład 2 - funkcje anonimowe
print((lambda f:f*2-3)(6))

b = lambda u,w:u+101*w
print(b(11,3))
print(b(45,2))

print(b)

def b(u,w):
    return u+101*w

print(b(11,3))
print(b(45,2))
print(b)

def multi(n):
    return lambda a:a*n

print(multi(8)(10))
print(multi(2)(10))


def licz(a):
    return a

d = multi(2)
print(d(10))


def dodawanie(funkcja,a,b):
    return funkcja(a)+funkcja(b)

def pw(n):
    return n**2

b = dodawanie(pw,5,8)
print(b)

c = dodawanie

print(c)
print(c(pw,5,8))

#przyklad3
liczby = [45,2,5,256,34,222,42,-345,-23,56,789,34,43]

liczby_parz = list(filter(lambda x:x%2==0,liczby))
print(liczby_parz)

cube = list(map(lambda x:x**3,liczby))
print(cube)

import numpy as np

npliczby = np.array(liczby)

print(type(liczby))
print(type(npliczby))

laprz = npliczby[npliczby%2==0]
print(laprz)

npcube = npliczby**3
print(npcube)
