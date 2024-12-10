# file= open(r"C:\Users\dcp69\Desktop\Python proj\.vscode\Eample.txt","r")
# content=file.read()
# # print(content)
# file = open(r"C:\Users\dcp69\Desktop\Python proj\.vscode\Example.txt", "r")
# content = file.read()
# print(content)

# Open the file using 'with' statement

file=open(r"C:\Users\dcp69\Desktop\Python proj\.vscode\Example.txt", "r") 
content = file.read()
print(content)

file.seek(0)
line=file.readline()
print(line)

file.seek(0)
lines=file.readlines()
print(lines)

file.close 