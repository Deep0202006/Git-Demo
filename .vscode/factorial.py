def factorial(num):
    if num == 0 or num== 1:
        return 1
    else:
        return num*factorial(num-1)
    
n=int(input("Enter a number:" ))
print(f"Factorial of {n} is:{factorial(n)}")
