#przykład 1
def liczby():
    lb = []
    for i in range(16):
        lb.append(i)
    return lb

print(liczby())

def liczbygen():
    for i in range(16):
        yield i*3-1

print(liczbygen())
print(list(liczbygen()))

for p in liczbygen():
    print(p)

#przykład 2
