inventory={}

def Add_item(item_name,quantity):
    if item_name in inventory:
        inventory[item_name] += quantity
        print(f"Updated {item_name} quantity to {inventory[item_name]}")
    else:
        inventory[item_name] = quantity
        print(f"Added {item_name} with quantity {quantity}")

def View_item():
    if not inventory:
        print("Inventory is empty.")
    else:
        print("Current Inventory:")
        for item_name,quantity in inventory.items():
          print(f"{item_name}: {quantity}")

def Update_item(item_name,quantity):
    if item_name in inventory:
        inventory[item_name] = quantity
        print(f"Updated {item_name} quantity to {inventory[item_name]}")
    else:
        print(f"Item {item_name} not found in inventory.")

def Delete_item(item_name):
    if item_name in inventory:
        del inventory[item_name]
    else:
        print(f"Item {item_name} not found in inventory.")

def main():
    while True:
        print("\n Inventory Managment menu:")
        print("1.Add Item")
        print("2.View Item")
        print("3.Update Item Quantity")
        print("4.Delete Item")
        print("5.Exiting ")

        choice= int(input("Enter an option from(1to5):"))
        if choice == 1:
            Item_name=input("Enter name of item you want to add:")
            Quantity=int(input("Enter the quantity of item to be added:"))
            Add_item(Item_name,Quantity)
        elif choice == 2:
            View_item()
        elif choice == 3:
            Item_name=input("Enter name of item you want to update:")
            Quantity=int(input("Enter the new quantity for selected item:"))
            Update_item(Item_name,Quantity)
        elif choice == 4:
            Item_name=input("Enter the name of item you want to delete.")
            Delete_item(Item_name)
        elif choice == 5:
            print("\nExiting the program !")
            break
        else:
            print("Invalid input")

if __name__ == '__main__':
    main()



