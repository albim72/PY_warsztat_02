
import csv
import math
import sys

import pandas as pd
import numpy as np

sys.set_int_max_str_digits(0x1000000)

data = {
    "name":["Anna","Jan","Ewa"],
    "age":[28,57,32],
    "city":["Warszawa","Krakow","Poznań"]

}
import csv
import math
import sys

import pandas as pd
import numpy as np

sys.set_int_max_str_digits(0x1000000)

data = {
    "name":["Anna","Jan","Ewa"],
    "age":[28,57,32],
    "city":["Warszawa","Krakow","Poznań"]

}

df = pd.DataFrame(data)
print(df)

df.to_csv(
    "people.csv",
    sep = "|",
    index = False,
    quoting = csv.QUOTE_NONNUMERIC
)

df.to_excel("people.xlsx",index=False)

#pierwsza opcja n! gdzie n=10000
n:int = 1000000
fact_n = math.factorial(n)
# print(fact_n)


fact_str = str(fact_n)

CHUNK_SIZE = 30000
chunks = [
    fact_str[i:i + CHUNK_SIZE]
    for i in range(0, len(fact_str), CHUNK_SIZE)
]

df = pd.DataFrame({
    "part": range(1,len(chunks)+1),
    "value_chunk":chunks
})

df.to_excel("fact_10000_chunk.xlsx",index=False)

df = pd.DataFrame(data)
print(df)

df.to_csv(
    "people.csv",
    sep = "|",
    index = False,
    quoting = csv.QUOTE_NONNUMERIC
)

df.to_excel("people.xlsx",index=False)

#pierwsza opcja n! gdzie n=10000
n:int = 1000000
fact_n = math.factorial(n)
# print(fact_n)


fact_str = str(fact_n)

CHUNK_SIZE = 30000
chunks = [
    fact_str[i:i + CHUNK_SIZE]
    for i in range(0, len(fact_str), CHUNK_SIZE)
]

df = pd.DataFrame({
    "part": range(1,len(chunks)+1),
    "value_chunk":chunks
})

df.to_excel("fact_10000_chunk.xlsx",index=False)
