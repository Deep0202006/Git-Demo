def average():
    numbers = []
    while True:
        user_input= input("Enter a number (or type done to finish):")
        if user_input.lower()=='done':
            break
        try:
                 number=float(user_input)
                 numbers.append(number)
        except ValueError:
             print("Please enter a valid number")
    if numbers:
             total=0
             for num in numbers:
              total+=num
              average= total/len(numbers)
              print(f"Average of entered numbers is:{average:.2f}")
    else:
             print("Invalid input")
average()
 
