def is_pelindrome(s):
    normalized_string= ''.join(filter(str.isalnum,s)).lower()
    return normalized_string == normalized_string[::-1]

def main():

 user_input=input("Enter the string for which you want to check palindrome:")
 result=is_pelindrome(user_input)

 if result:
    print(f"The string {user_input} is palindrome {is_pelindrome(user_input)}")

 else:
    print("The string is not a palindrome")

__name__='_main_'
main()
