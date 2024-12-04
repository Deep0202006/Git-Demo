inventory = {}

def Add_items(item_name,quantity):
    if item_name in inventory:
        inventory[item_name] += quantity
        print(f"Updated {item_name} quantity to: {inventory[item_name]}")
    else:
        inventory[item_name] = quantity 
        print(f"{item_name} added with quantity {inventory[item_name]}")

def View_items():
    if not inventory:
        print("Inventory is empty!")
    else:
        print("Current Inventory:")
        for item_name,quantity in inventory.items():
            print(f"{item_name}: {quantity}")
            
