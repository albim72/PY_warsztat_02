import math

#funkcja 1
def gx(n,m=4,k=3,b=7):
    return math.sqrt(n+m)*k-b

#funkcja 2
def rank_list(*lang,nrrank):
    print(f'ranking nr {nrrank}: 1. {lang[0]} 2. {lang[1]} 3. {lang[2]}')
