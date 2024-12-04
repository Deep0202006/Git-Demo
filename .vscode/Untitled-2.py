def is_prime(num):
    if num <= 1:  
        return False
    for i in range(2, int(num**0.5) + 1):  
        if num % i == 0:
            return False
    return True 

def prime_numbers_up_to(n):
    primes = []
    for num in range(0, n + 1): 
        if is_prime(num):
            primes.append(num)
    return primes

A = int(input("Enter a number: "))
primes = prime_numbers_up_to(A)
print(f"Prime numbers up to {A} are: {primes}")