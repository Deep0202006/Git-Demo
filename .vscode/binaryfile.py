import struct

def write_binary_file(filename, numbers):
    """Write a list of integers to a binary file."""
    with open(filename, 'wb') as file:
        for number in numbers:
            # Pack the integer as a binary data using struct
            file.write(struct.pack('i', number))
    print(f"Data written to {filename}.")

def read_binary_file(filename):
    """Read integers from a binary file and return them as a list."""
    numbers = []
    with open(filename, 'rb') as file:
        while True:
            # Read 4 bytes (size of an integer)
            bytes_read = file.read(4)
            if not bytes_read:
                break  # End of file
            # Unpack the binary data to an integer
            number = struct.unpack('i', bytes_read)[0]
            numbers.append(number)
    return numbers
def min():
    print("Enter suitable inputs\n")
    
def main():
    filename = 'numbers.bin'
    numbers_to_write = [10, 20, 30, 40, 50]
    min()
    # Write numbers to binary file
    write_binary_file(filename, numbers_to_write)
    read_binary_file(filename)  
   #Enter a new variable named A
    A=input("Enter the most values:")
    # Read numbers from binary file
    read_numbers = read_binary_file(filename)
    print("Numbers read from the binary file:", read_numbers)
    bytes_read=filename.read(4)
    if not bytes_read:
     return "There is no storage occupied by the file"
    else:
        print(f"{filename} occupys {bytes_read} in the folder")
    print(f"{filename}: {bytes_read}")
    filename.seek(0)
    newfile= filename.readlines()
    print(newfile),filename,read_binary_file, min
    # sorted (None, reversed: bool = False)
    for bool in numbers_to_write:
        print(f"{newfile}: {numbers_to_write+1}")
        return 0
    if A==0:
        return 1
    else:
        return "invalid"
print(f"objects are the taken values for inital stage\n")
B=int(input("Enter a value:")) 
print(B)
print(B+1)
A=int(input("Enter the value:"))
if A==12:
    print(f"{A}:{B}")
else:
    print("Invalid input.")
#Distributed values across the scope 
D=int(input("Enter suitable value:"))
for D in read_binary_file():
    D=A+B 
    print(D)
    print(f"{A} is the value alloted to the {B}")
    D+=1
#calling predefined functions in main
if A==0:
    min()
else:
    print(f"{A}")

# Run the program
if __name__ == "__main__":
   main()


   