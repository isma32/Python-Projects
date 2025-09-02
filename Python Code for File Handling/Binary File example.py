# Writing binary data to a file
data = b'\x42\x69\x6e\x61\x72\x79\x20\x64\x61\x74\x61'
with open("example.bin", "wb") as file:
    file.write(data)

# Reading binary data from a file
with open("example.bin", "rb") as file:
    content = file.read()
    print(content)
