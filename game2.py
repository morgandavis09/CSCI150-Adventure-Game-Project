# game.py
import gamefunctions
import random

state = {
    "player_name": "",
    "player_hp": 30,
    "player_gold": 50,
    "player_inventory": [
        {"name": "sword", "type": "weapon", "maxDurability": 10, "currentDurability": 10, "equipped": False},
        {"name": "magic potion", "type": "special", "note": "defeats any monster", "equipped": False}
    ]
}

shop_items = [
    {"name": "sword", "type": "weapon", "price": 15, "maxDurability": 10},
    {"name": "shield", "type": "shield", "price": 10, "maxDurability": 6},
    {"name": "magic potion", "type": "special", "price": 20, "note": "defeats any monster"}
]

def display_inventory(item_type=None):
    """Display inventory with filter."""
    items = [item for item in state["player_inventory"] if item_type is None or item["type"] == item_type]
    if not items:
        print("No items of this type.")
        return
    for idx, item in enumerate(items, 1):
        equip_status = " (equipped)" if item.get("equipped") else ""
        print(f"{idx}) {item['name']}{equip_status}")
    return items

def equip_item():
    """Equip a weapon or armour."""
    choice_type = input("What type of item do you want to equip? (weapon/shield/special): ").lower()
    items = display_inventory(choice_type)
    if not items:
        return
    selection = int(input(f"Select an item to equip (1-{len(items)}), or 0 to cancel: "))
    if selection == 0:
        return
    
    for item in state["player_inventory"]:
        if item["type"] == choice_type:
            item["equipped"] = False
    items[selection - 1]["equipped"] = True
    print(f"{items[selection - 1]['name']} equipped.")

def visit_shop():
    """Visit shop and purchase items."""
    print("\nThis is the shop.")
    for idx, item in enumerate(shop_items, 1):
        print(f"{idx}) {item['name']} - ${item['price']}")
    choice = int(input(f"Select an item (1-{len(shop_items)}), or 0 to exit: "))
    if choice == 0:
        return
    item = shop_items[choice - 1]
    quantity = int(input(f"How many {item['name']}s would you like to buy? "))
    purchased, leftover = gamefunctions.purchase_item(item["price"], state["player_gold"], quantity)
    state["player_gold"] = leftover
    if purchased > 0:
        for _ in range(purchased):
            new_item = item.copy()
            new_item["equipped"] = False
            state["player_inventory"].append(new_item)
        print(f"Purchased {purchased} {item['name']}(s). Remaining gold: {state['player_gold']}")
    else:
        print("Not enough gold to purchase.")

def fight_monster():
    """Handles combat with a random monster, including special items."""
    monster = gamefunctions.new_random_monster()
    print(f"\nA wild {monster['name']} appears!")
    print(monster['description'])
    
    special_items = [i for i in state["player_inventory"] if i["type"] == "special"]
    if special_items:
        use_special = input("Use a special item to instantly defeat the monster? (yes/no): ").lower()
        if use_special == "yes":
            item = special_items[0]
            print(f"You used {item['name']} to defeat {monster['name']} instantly!")
            state["player_inventory"].remove(item)
            state["player_gold"] += monster["money"]
            print(f"You earned {monster['money']} gold!")
            return
    
    while state["player_hp"] > 0 and monster["health"] > 0:
        print(f"\nYour HP: {state['player_hp']} | {monster['name']} HP: {monster['health']}")
        action = input("Choose action: 1) Attack  2) Run: ")
        if action == "1":
            weapon = next((i for i in state["player_inventory"] if i["type"] == "weapon" and i["equipped"]), None)
            if weapon:
                damage = random.randint(5, 12) + weapon.get("maxDurability", 0)//2
                weapon["currentDurability"] -= 1
                if weapon["currentDurability"] <= 0:
                    print(f"Your {weapon['name']} broke!")
                    state["player_inventory"].remove(weapon)
            else:
                damage = random.randint(5, 12)
            monster["health"] -= damage
            state["player_hp"] -= monster["power"]
            print(f"You hit {monster['name']} for {damage} damage.")
            print(f"{monster['name']} hits you for {monster['power']} damage.")
        elif action == "2":
            print(f"You ran away from {monster['name']}.")
            break
        else:
            print("Invalid choice. Enter 1 or 2.")
    
    if monster["health"] <= 0:
        print(f"You defeated {monster['name']} and earned {monster['money']} gold!")
        state["player_gold"] += monster["money"]
    if state["player_hp"] <= 0:
        print("You have been defeated!")

def main():
    """Runs the main game loop."""
    state["player_name"] = input("What is your character's name? ")
    gamefunctions.print_welcome(state["player_name"], 40)

    while True:
        print(f"\nCurrent HP: {state['player_hp']}, Gold: {state['player_gold']}")
        print("1) Venture into the wilds (Fight a monster)")
        print("2) Rest (Restore 5 HP for 5 Gold)")
        print("3) Visit shop")
        print("4) Equip an item")
        print("5) Show inventory")
        print("6) Quit")
        choice = input("Select an option (1-6): ")
        if choice == "1":
            fight_monster()
        elif choice == "2":
            if state["player_gold"] >= 5:
                state["player_hp"] += 5
                state["player_gold"] -= 5
                print("You rested and regained 5 HP.")
            else:
                print("Not enough gold to rest.")
        elif choice == "3":
            visit_shop()
        elif choice == "4":
            equip_item()
        elif choice == "5":
            display_inventory()
        elif choice == "6":
            print(f"Farewell, {state['player_name']}. Thanks for playing!")
            break
        else:
            print("Invalid choice. Enter 1-6.")

if __name__ == "__main__":
    main()
