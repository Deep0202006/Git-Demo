def multiply(num):
    i=1
    result=[]
    while True:
        
        result.append(num*i)
        i+=1
        
        if i>10:
            break

    return result

A=int(input("Enter number:"))
print(f"Table of {A} is: {multiply(A)}")

