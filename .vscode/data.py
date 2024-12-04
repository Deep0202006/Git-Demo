def display_menu():
    "Display menu option."
    print("\nData list")
    print("1. Add data")
    print("2. View data")
    print("3. Remove data")
    print("4. Exit")

def Add_data(data_list):
    """Add a new data to data list"""
    data=input("Enter the data you want to add:")
    data_list.append(data)
    print(f"New data {data} is added.")

def View_data(data_list):
    "View all data in data list."
    if not data_list:
        print("Your data list is empty.")
    else:
        print("\n Your Data is:")
        for index,data in enumerate(data_list, start=1):
            print(f"{index}.{data}")

def Remove_data(data_list):
    "Remove data from data list."
    View_data(data_list)
    if data_list:
        try:
            data_index=int(input("Enter the data number you want to remove:"))-1
            if 0 <= data_index < len(data_list):
                removed_data = data_list.pop(data_index)
            else:
                print("Invalid data number.")
        except ValueError:
            print("Please enter a valid number")

def main():
    "Main function to run the data list."
    data_list=[]
    while True:
    
        display_menu()
        choice = input("Enter choice (1 to 4): ")
        try:
            choice = int(choice)  # Convert choice to an integer
        except ValueError:
            print("Invalid input. Please enter a valid option.")
            continue  
        
        
        if choice==1:
            Add_data(data_list)
        elif choice==2:
            View_data(data_list)
        elif choice==3:
            Remove_data(data_list)
        elif choice==4:
            print("Exiting the Data list.")
            break
        else:
            print("Inalid input.Please enter a valid option.")

if __name__ == "__main__":
    main()

