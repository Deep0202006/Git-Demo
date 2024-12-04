def sum_of_square(num):
    if num==1:
        return 1
    else:
        return num**2 + sum_of_square(num-1)

"""A=int(input("Enter number:"))
print(f"Sum of square of numbers upto {A} is {sum_of_square(A)}")"""
def main():
    B=int(input("Enter number:"))
    print(f"Sum of square of numbers upto {B} is {sum_of_square(B)}")

if __name__ == '__main__':
  main()
