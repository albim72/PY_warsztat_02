from funkcja_no2 import gx,rank_list

#przykład 1
n = 100
def policz(a:int,b:int,c:float,y:int=100) -> float:
    global n
    n = (a+b)*gx(a,b,c,y) + n
    return n

print(policz(1,2,3))
print(policz(7,5,8.2,66))
print(policz(23,6.23,True,12))
print(policz(2,8,3,-3))

#przykład2

print(gx(5,2,6,3)**2 - 5)

#przykład3

rank_list("Python","Java","C#","C++",nrrank=54)
