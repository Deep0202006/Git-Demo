while True:
    try:
        number=int(input("Enter an integer:"))
        number=abs(number)
        square= number ** 2   
        print(f"Square of {number} is: {square}")
        break
    except ValueError:
        print("Enter a valid integer")