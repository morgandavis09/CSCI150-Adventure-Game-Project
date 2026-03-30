import gamefunctions
import random

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



def fight_monster(player_hp, player_gold):
    """Handles a simple combat loop with a random monster."""
    monster = gamefunctions.new_random_monster()
    print(f"\nA wild {monster['name']} appears!")
    print(monster['description'])

    while player_hp > 0 and monster["health"] > 0:
        print(f"\nYour HP: {player_hp} | {monster['name']} HP: {monster['health']}")
        action = input("Choose an action: 1) Attack  2) Run: ")
        if action == "1":
            damage = random.randint(5, 12)
            monster["health"] -= damage
            player_hp -= monster["power"]
            print(f"You hit {monster['name']} for {damage} damage.")
            print(f"{monster['name']} hits you for {monster['power']} damage.")
        elif action == "2":
            print(f"You ran away from {monster['name']}.")
            break
        else:
            print("Invalid choice. Enter 1 or 2.")

    if monster["health"] <= 0:
        print(f"You defeated the {monster['name']} and earned {monster['money']} gold!")
        player_gold += monster["money"]
    if player_hp <= 0:
        print("You have been defeated!")

    return player_hp, player_gold


def main():
    """Runs the main game loop."""
    name = input("What is your character's name? ")
    gamefunctions.print_welcome(name, 40)

    hp = 30
    gold = 10

    while True:
        print(f"\nYou are in town. Current HP: {hp}, Gold: {gold}")
        print("1) Venture into the wilds (Fight a monster)")
        print("2) Rest (Restore 5 HP for 5 Gold)")
        print("3) Visit shop")
        print("4) Quit")

        choice = input("Select an option (1-4): ")
        if choice == "1":
            hp, gold = fight_monster(hp, gold)
        elif choice == "2":
            if gold >= 5:
                hp += 5
                gold -= 5
                print("You rest and regain 5 HP.")
            else:
                print("Not enough gold to rest.")
        elif choice == "3":
            gamefunctions.print_shop_menu("Milk", 3.49, "Eggs", 4.89)
        elif choice == "4":
            print(f"Farewell, {name}. Thanks for playing!")
            break
        else:
            print("Invalid choice. Enter 1-4.")




if __name__ == "__main__":
    main()
    
