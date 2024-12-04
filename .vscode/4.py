def display_contacts(contacts):
    if not contacts:
        print("Your contact book is empty.")
    else:
        print("Your Contacts:")
        for index, (name, phone) in enumerate(contacts, start=1):
            print(f"{index}. Name: {name}, Phone: {phone}")

def main():
    contacts = []

    while True:
        print("\nContact Book Menu:")
        print("1. Add Contact")
        print("2. Remove Contact")
        print("3. View Contacts")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            name = input("Enter the contact's name: ")
            phone = input("Enter the contact's phone number: ")
            contacts.append((name, phone))  # Store as a tuple (name, phone)
            print(f"Contact '{name}' added to the contact book.")
        elif choice == '2':
            display_contacts(contacts)
            contact_index = input("Enter the contact number you want to remove: ")
            if contact_index.isdigit() and 1 <= int(contact_index) <= len(contacts):
                removed_contact = contacts.pop(int(contact_index) - 1)
                print(f"Contact '{removed_contact[0]}' removed from the contact book.")
            else:
                print("Invalid contact number.")
        elif choice == '3':
            display_contacts(contacts)
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()