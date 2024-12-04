def sum_of_cube(num):
    sum
    if num==0:
       return 0
    else:   
       return num**3 + sum_of_cube(num-1)
        
        
    
user_input=int(input("Enter a number:"))
result= sum_of_cube(user_input)
print(f"Sum of cube of {user_input} is: {result}")

# a = []
# a= input("Enter string")
# b= 12
# print(int(a)+b)