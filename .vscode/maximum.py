def maximum(num1,num2):
     if num1> num2:
          return num1
     elif num1==num2:
          return "Both are Equal"
     else:
          return num2

A=int(input("Enter first number: "))
B=int(input("Enter second number: "))  

print(f"Maximum from {A} and {B} is: {maximum(A,B)}")