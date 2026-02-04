data = b"\x00\x01\x02\x03"

with open("binary.bin", "wb") as f:
    f.write(data)

with open("binary.bin", "rb") as f:
    data = f.read()

print(type(data), data)