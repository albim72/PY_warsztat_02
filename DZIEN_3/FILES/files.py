with open("dane.txt","r",encoding="utf-8") as f:
    content = f.read()

print(content)

with open("danedrugie.txt","w",encoding="utf-8") as f:
    f.write(content + "\n")
    f.write("dodano tekst\n")
    f.write("koniec\n")

with open("danedrugie.txt","a",encoding="utf-8") as f:
    f.write("dodano tekst no 3\n")
    f.write("ekstra\n")
    f.write("......\n")