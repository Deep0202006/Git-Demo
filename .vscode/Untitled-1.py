def add(x,y):
    return x+y
def subtract(x,y):
    return x-y
def multiply(x,y):
    return x*y
def divide(x,y):
    if y== 0:
        return "Cannot divide"
    else :
        return x/y
choice=input("Select operation(1/2/3/4):")    
num1= float(input("Enter first number:"))
num2= float(input("Enter secod umber: "))
if choice =='1':
    print(f"{num1}+{num2}={add(num1,num2)}")
elif choice =='2':
    print(f"{num1}-{num2}={subtract(num1,num2)}")
elif choice =='3':
    print(f"{num1}*{num2}={multiply(num1,num2)}")
elif choice =='4':
    print(f"{num1}/{num2}={divide(num1,num2)}")
else:
    print("Invalid Input")