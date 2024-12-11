#Program to find the facorial of a number
def factorial(n):
    if n==0:
        return 1
    else:
        return n*factorial(n-1)

A=int(input("Enter a number:"))
print(f"Factorial of {A} is: {factorial(A)}")

#Program to find the fibonacci series 
def fibonacci(n):
    fib=[]
    if n<=0:
        return 0
    elif n==1:
        return 1
    else:
        result=fibonacci(n - 1)+fibonacci(n - 2)
        
        return result
      
B=int(input("Enter a number:"))
print(f"Fibonacci series upto{B} is: {fibonacci(B)}")

# print(f"{A} : {B} : {factorial(A)}: {fibonacci(B)}") 
# print(f"{factorial(A,B)}: {fibonacci(A,B)}")

#Program to find sum of the list of number
def sum_list(lst):
    if not lst:  # Base case: if the list is empty
        return 0
    else:
        return lst[0] + sum_list(lst[1:])  # Recursive case: sum the first element and the sum of the rest

print(sum_list([1, 2, 3, 4, 5]))  

def check(n):
    if n==0:
        return check(n)* check(n-1)
    else:
        return n*check(n-1)
    
def merge_sort(arr):
    if len(arr)>1:
        mid=len(arr)
        left_half=arr[:mid]
        right_half=arr[mid:]
        merge_sort(left_half)
        merge_sort(right_half)
    i=j=k=0

def get_first_element(lst):
   return lst[0]

def binary_searcher(arr,target):
    low,high=0 , len(arr)-1
    while True:
        print("Enter a value:")
        


