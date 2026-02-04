import csv

rows = [
    {"name":"Anna","age":30},
    {"name":"Bob","age":40},
    {"name":"Charlie","age":50}
]

with open("people.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(rows)