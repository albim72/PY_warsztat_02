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
