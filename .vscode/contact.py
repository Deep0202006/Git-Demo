def display_contacts(contacts):
    if not contacts:
        print("Your contact book is empty")
    else:
        print("Your contact:")
        for index,(name,phone) in enumerate(contacts,start=1):
            print(f"{index}.Name:{name},Phone:{phone}")

def main():
    contacts=[]

    while True:
        print("\n Contact book menu.")
        print("1. Add contact")
        print("2. Remove contacts")
        print("3. View contact")
        print("4. Exit")

        choice=int(input("chose any one option (1 to 4):"))
        if choice==1:
            name=input("Enter name of contact:")
            phone=int(input("Enter contact no:"))
            contacts.append((name,phone))
        elif choice==2:
            display_contacts(contacts)
            contact_index=input("Enter the contact number you want to remove:")
            if contact_index.isdigit() and 1<= int(contact_index) <= len(contacts):
                removed_contact = contacts.pop(int(contact_index)-1)
                print(f"Contact '{removed_contact[0]}' is removed from contacts")
            else:
                print("Invalid contact no.")
        elif choice==3:
            display_contacts(contacts)
        elif choice==4:
            print("Exiting contact list.")  
            break
        else:
            print("Invalid option.")

__name__ == '_main_'
main()