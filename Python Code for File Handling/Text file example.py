
# Writing to a text file
with open("example.txt", "w") as file:
    file.write("Hello, this is a text file.\n")
    file.write("Each line is stored as plain text.")

# Reading from a text file
with open("example.txt", "r") as file:
    content = file.read()
    print(content)


