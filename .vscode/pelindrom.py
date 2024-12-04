def sum_of_digits(number):
    print("string:",str(number))
    
    return sum(int(digit) for digit in str(number) if digit.isdigit())

user_input = input("Please enter a number: ")


result = sum_of_digits(user_input)


print(f"The sum of the digits in {user_input} is: {result}")