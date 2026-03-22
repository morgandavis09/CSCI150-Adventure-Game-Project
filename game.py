import gamefunctions

def main():
    """
        Introduces each function briefly, with some user input."""
    
    name = input("What is your name?: ")
    gamefunctions.print_welcome(name, 30)
    
    money = float(input("How much money are you shopping with?: "))
    price = float(input("WHat is the item price?: "))
    quantity = int(input("What is the quantity?: "))

    purchased, leftover = gamefunctions.purchase_item(price, money, quantity)

    print(f"You have ${leftover:.2f} left.")

    print("\nLet's create a monster.")
    monster = gamefunctions.new_random_monster
    print(monster)

    choice = input("Do you want to see a shop menu? (yes/no): ")

    if choice.lower() == "yes":
    print("\nShop Menu:")
    gamefunctions.print_shop_menu("Milk", 3.49, "Eggs", 4.89)

if __name__ == "__main__":
    main()
    
