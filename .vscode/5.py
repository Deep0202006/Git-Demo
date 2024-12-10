def outer_function(msg):
    def inner_function():
        print(msg)
    inner_function()

outer_function("Hello from the inner function!") 

def data(**kwargs):
    for name,id_no in kwargs.items():
        print(f"{name}: {id_no}")

A=input("Enter name:")

B=int(input("Enter id number:"))

data(name=A,id_no=B)

def update(f):
    if f==0:
        print(f"{f} is the solution for {f-1}") 
    else:
        print("invalid input!")

A=int(input("Enter a number:"))
update(A) 
my_dict={
    'Name':'Deep',
    'Age':18,
    'City':'XYZ'
}
my_dict=dict(Name='Deep',Age='18',City='XYZ')

print(my_dict['Name'])
print(my_dict['Age'])
print(my_dict['City'])
if A<1:
   print(f"{A}: {B}") 
elif A==1:
         Item_name=input("Enter name of the item you want to edit:")
         Quantity=int(input("Enter the updated quantity:"))
elif A == 3:
            Item_name=input("Enter name of item you want to update:")
            Quantity=int(input("Enter the new quantity for selected item:"))
            Item_name(Item_name,Quantity)
elif A == 4:
        Item_name=input("Enter the name of item you want to delete.")
        print(Item_name)
elif A == 5:
    print("\nExiting the program !")
    
elif A==7:
     print("Existing file has been terminated\n")

elif A==8:
     print("Existing file has been declared invalid\n")

elif A==11:
     Item_name=input("Enter a valid name:")
     print(f"{Item_name} is for the entitled body.")
elif A==21:
     Item_name=input("Enter valid:")
     print(f"{Item_name}:{Item_name+1}")

else:
      print("Exiting!")

file=open(r"Example.txt","r")
content= file.read()

file.seek(0)
line=file.readline()
print(line)
file.seek(0)
lines=file.readlines()
print(lines)
#Read(size) in this function if the size is not specified than  
#It reads whole file 
file.seek(0)
Newline=file.write("Demo lines added in the file.")
print(Newline)
print(f"{Newline} is the updated form of the document\n")
with open(rb"Example.bin","rb") as file:
     content=file.read()
     print(content)
file.seek(0)
line=file.readline()

file.seek(0)
lines=file.readlines()

file.seek(0)
Newlines=file.write("New line that is added to the content of the file.\n")


file.close()


      












# def make_pizza(*toppings):
#     print("Making a pizza with the following toppings:")
#     for topping in toppings:
#         print(f"- {topping}")

# make_pizza("pepperoni", "mushrooms", "extra cheese")