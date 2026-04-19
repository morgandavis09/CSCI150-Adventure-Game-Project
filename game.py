import gamefunctions
import random
import json
import os


state = {
    "player_name": "",
    "player_hp": 30,
    "player_gold": 100,
    "player_inventory": []
}


shop_items = [
    {"name": "sword", "type": "weapon", "price": 15, "maxDurability": 10, "currentDurability": 10, "equipped": False},
    {"name": "monster potion", "type": "special", "price": 10, "note": "defeats monster instantly"}
]


def show_inventory():
    """
    """
    print("\nInventory:")
    if not state["player_inventory"]:
        print("Empty")
        return

    for item in state["player_inventory"]:
        status = "(equipped)" if item.get("equipped") else ""
        print(f"- {item['name']} {status}")


def visit_shop():
    """
    """
    print("\nShop:")
    for i, item in enumerate(shop_items, 1):
        print(f"{i}) {item['name']} - {item['price']} gold")
    print("0) Exit")

    try:
        choice = int(input("Choose item: "))
    except ValueError:
        return

    if choice == 0:
        return

    if choice < 1 or choice > len(shop_items):
        return

    item = shop_items[choice - 1]

    if state["player_gold"] < item["price"]:
        print("Not enough gold.")
        return

    state["player_gold"] -= item["price"]
    state["player_inventory"].append(item.copy())

    print(f"You bought {item['name']}")


def equip_weapon():
    """
    """
    weapons = [i for i in state["player_inventory"] if i["type"] == "weapon"]

    if not weapons:
        print("No weapons to equip.")
        return

    print("\nWeapons:")
    for i, item in enumerate(weapons, 1):
        print(f"{i}) {item['name']}")

    try:
        choice = int(input("Choose weapon: ")) - 1
    except ValueError:
        return

    if choice < 0 or choice >= len(weapons):
        return

    for item in state["player_inventory"]:
        if item["type"] == "weapon":
            item["equipped"] = False

    weapons[choice]["equipped"] = True
    print(f"{weapons[choice]['name']} equipped.")


def fight_monster(player_hp, player_gold):
    """Handles a simple combat loop with a random monster."""
    monster = gamefunctions.new_random_monster()
    print(f"\nA wild {monster['name']} appears!")
    print(monster["description"])

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

            base_damage = random.randint(5, 12)

            if weapon:
                damage = base_damage + 5

                if "currentDurability" in weapon:
                    weapon["currentDurability"] -= 1
                    print(f"{weapon['name']} increases your damage!")

                    if weapon["currentDurability"] <= 0:
                        print(f"{weapon['name']} broke!")
                        state["player_inventory"].remove(weapon)
            else:
                damage = base_damage

            monster["health"] -= damage
            player_hp -= monster["power"]

            print(f"You hit {monster['name']} for {damage} damage.")
            print(f"{monster['name']} hits you for {monster['power']} damage.")

        elif action == "2":
            print(f"You ran away from {monster['name']}.")
            break

    if monster["health"] <= 0:
        print(f"You defeated the {monster['name']} and earned {monster['money']} gold!")
        player_gold += monster["money"]

    if player_hp <= 0:
        print("You have been defeated!")

    return player_hp, player_gold



def save_game(filename):
    """Saves current game state to a file."""
    with open(filename, "w") as file:
        json.dump(state, file, indent=4)

    print("Game saved successfully!")

    
def load_game(filename):
    """Loads game state from a file."""
    global state

    if not os.path.exists(filename):
        print("Save file not found.")
        return False

    with open(filename, "r") as file:
        state = json.load(file)

    print("Game loaded successfully!")
    return True



def main():
    """Runs the main game loop."""

    print("1) New Game")
    print("2) Load Game")

    choice = input("> ")

    if choice == "2":
        filename = input("Enter save file name: ")

        success = load_game(filename)

        if not success:
            state["player_name"] = input("What is your character's name? ")
            state["player_hp"] = 30
            state["player_gold"] = 100
            state["player_inventory"] = []
    else:
        state["player_name"] = input("What is your character's name? ")
        state["player_hp"] = 30
        state["player_gold"] = 100
        state["player_inventory"] = []

    name = state["player_name"]

   
    while True:
        print(f"\nYou are in town. Current HP: {state['player_hp']}, Gold: {state['player_gold']}")
        print("1) Venture into the wilds (Fight a monster)")
        print("2) Rest (Restore 5 HP for 5 Gold)")
        print("3) Visit shop")
        print("4) Equip weapon")
        print("5) Show inventory")
        print("6) Save and Quit")

        choice = input("Select an option (1-6): ")

        if choice == "1":
            state["player_hp"], state["player_gold"] = fight_monster(
                state["player_hp"],
                state["player_gold"]
            )


        elif choice == "2":
            if state["player_gold"] >= 5:
                state["player_hp"] += 5
                state["player_gold"] -= 5
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
            filename = input("Enter save file name: ")
            save_game(filename)
            print(f"Farewell, {name}. Thanks for playing!")
            break

        else:
            print("Invalid choice. Enter 1-6.")
            

def save_game(filename):
    """Saves current game state to a file."""
    with open(filename, "w") as file:
        json.dump(state, file, indent=4)

    print("Game saved successfully!")



if __name__ == "__main__":
    main()
