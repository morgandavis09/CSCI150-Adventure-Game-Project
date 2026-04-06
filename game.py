import gamefunctions
import random

state = {
    "player_name": "",
    "player_hp": 30,
    "player_gold": 50,
    "player_inventory": []
}

shop_items = [
    {"name": "sword", "type": "weapon", "price": 15, "maxDurability": 10, "currentDurability": 10, "equipped": False},
    {"name": "monster potion", "type": "special", "price": 10, "note": "defeats monster instantly"}
]


def show_inventory():
    print("\nInventory:")
    if not state["player_inventory"]:
        print("Empty")
        return
    for item in state["player_inventory"]:
        status = "(equipped)" if item.get("equipped") else ""
        print(f"- {item['name']} {status}")


def visit_shop():
    print("\nShop:")
    for i, item in enumerate(shop_items, 1):
        print(f"{i}) {item['name']} - {item['price']} gold")
    print("0) Exit")

    choice = int(input("Choose item: "))
    if choice == 0:
        return

    item = shop_items[choice - 1]

    purchased, leftover = gamefunctions.purchase_item(
        item["price"], state["player_gold"], 1
    )

    if purchased > 0:
        state["player_gold"] = leftover
        state["player_inventory"].append(item.copy())
        print(f"You bought {item['name']}")
    else:
        print("Not enough gold.")


def equip_weapon():
    weapons = [i for i in state["player_inventory"] if i["type"] == "weapon"]

    if not weapons:
        print("No weapons to equip.")
        return

    print("\nWeapons:")
    for i, item in enumerate(weapons, 1):
        print(f"{i}) {item['name']}")

    choice = int(input("Choose weapon: ")) - 1

    for item in state["player_inventory"]:
        if item["type"] == "weapon":
            item["equipped"] = False

    weapons[choice]["equipped"] = True
    print(f"{weapons[choice]['name']} equipped.")

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
    monster = gamefunctions.new_random_monster()
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

    special_items = [i for i in state["player_inventory"] if i["type"] == "special"]
    if special_items:
        use_item = input("Use special item to defeat monster? (yes/no): ")
        if use_item.lower() == "yes":
            print("Monster defeated instantly!")
            state["player_inventory"].remove(special_items[0])
            player_gold += monster["money"]
            return player_hp, player_gold


    while player_hp > 0 and monster["health"] > 0:
        print(f"\nYour HP: {player_hp} | {monster['name']} HP: {monster['health']}")
        action = input("Choose an action: 1) Attack  2) Run: ")
        if action == "1":
            weapon = next((i for i in state["player_inventory"] if i.get("equipped")), None)

            if weapon:
                damage = random.randint(5, 12) + 5
            else:
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
    state["player_hp"] = hp
    state["player_gold"] = gold
    state["player_name"] = name


    while True:
        print(f"\nYou are in town. Current HP: {hp}, Gold: {gold}")
        print("1) Venture into the wilds (Fight a monster)")
        print("2) Rest (Restore 5 HP for 5 Gold)")
        print("3) Visit shop")
        print("4) Equip weapon")
        print("5) Show inventory")
        print("6) Quit")


        choice = input("Select an option (1-6): ")

        if choice == "1":
            hp, gold = fight_monster(hp, gold)
            state["player_hp"] = hp
            state["player_gold"] = gold


        elif choice == "2":
            if gold >= 5:
                hp += 5
                gold -= 5
                state["player_hp"] = hp
                state["player_gold"] = gold
                print("You rest and regain 5 HP.")
            else:
                print("Not enough gold to rest.")

        elif choice == "3":
            visit_shop()

        elif choice == "4":
            equip_weapon()

        elif choice == "5":
            show_inventory()

        elif choice == "6":
            print(f"Farewell, {name}. Thanks for playing!")
            break

        else:
            print("Invalid choice. Enter 1-6.")





if __name__ == "__main__":
    main()
    
