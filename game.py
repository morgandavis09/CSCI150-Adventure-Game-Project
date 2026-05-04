import gamefunctions
import random
import json
import os
from WanderingMonster import WanderingMonster


state = {
    "player_name": "",
    "player_hp": 30,
    "player_gold": 100,
    "player_inventory": []
}

state["monsters"] = []

map_state = {
    "player_pos": [0, 0],
    "town_pos": [0, 0],
    "in_town": True,
    "ruins": [(3, 3), (3, 4), (4, 4), (6, 7)],
    "shrines": [(1, 6), (8, 2)]
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


def fight_monster(player_hp, player_gold, monster):
    """Handles a simple combat loop with a random monster."""

    print(f"\nA wild {monster.monster_type} appears!")

    special_items = [i for i in state["player_inventory"] if i["type"] == "special"]

    if special_items:
        use_item = input("Use special item to defeat monster? (yes/no): ")
        if use_item.lower() == "yes":
            print("Monster defeated instantly!")
            state["player_inventory"].remove(special_items[0])
            state["player_gold"] += monster.money
            return player_hp, state["player_gold"]

    while player_hp > 0 and monster.hp > 0:
        print(f"\nYour HP: {player_hp} | {monster.monster_type} HP: {monster.hp}")
        action = input("Choose an action: 1) Quick Attack  2) Strong Attack  3) Run: ")

        if action == "1":
            base_damage = random.randint(3, 8)
            damage = base_damage

            monster.hp -= damage
            player_hp -= monster.power // 2

            print(f"You quickly strike {monster.monster_type} for {damage} damage.")
            print(f"{monster.monster_type} hits you lightly for {monster.power // 2} damage.")

        elif action == "2":
            base_damage = random.randint(8, 15)
            damage = base_damage

            monster.hp -= damage
            player_hp -= monster.power + 3

            print(f"You unleash a strong attack on {monster.monster_type} for {damage} damage!")
            print(f"{monster.monster_type} counters hard for {monster.power + 3} damage.")

        elif action == "3":
            print(f"You ran away from {monster.monster_type}.")
            break

    if monster.hp <= 0:
        print(f"You defeated the {monster.monster_type} and earned {monster.money} gold!")
        player_gold += monster.money

    return player_hp, player_gold


def move_player(game_state, direction):
    x, y = game_state["player_pos"]
    new_x, new_y = x, y

    if direction == "up":
        new_y -= 1
    elif direction == "down":
        new_y += 1
    elif direction == "left":
        new_x -= 1
    elif direction == "right":
        new_x += 1

    new_x = max(0, min(9, new_x))
    new_y = max(0, min(9, new_y))

    if (new_x, new_y) in map_state.get("ruins", []):
        print("The ruins block your path!")
        return "moved"

    x = max(0, min(9, x))
    y = max(0, min(9, y))

    game_state["player_pos"] = [new_x, new_y]

    if game_state["player_pos"] == game_state["town_pos"]:
        return "returned_to_town"
    
    return "moved"

def run_map(game_state):
    while True:
        visible_monsters = {(m.x, m.y) for m in state["monsters"]}
        
        for y in range(10):
            row = ""
            for x in range(10):

                pos = (x, y)

                if [x, y] == game_state["player_pos"]:
                    row += "P"

                elif [x, y] == game_state["town_pos"]:
                    row += "T"

                elif (x, y) in visible_monsters:
                    row += "M"

                elif pos in map_state.get("ruins", []):
                    row += "R"

                elif pos in map_state.get("shrines", []):
                    row += "S"

                else:
                    row += "."
                    
            print(row)

        move = input("Move (w/a/s/d, q to quit): ")

        if move == "q":
            return "town"

        direction = None
        if move == "w":
            direction = "up"
        elif move == "s":
            direction = "down"
        elif move == "a":
            direction = "left"
        elif move == "d":
            direction = "right"

        if direction:
            result = move_player(game_state, direction)

            if result == "returned_to_town":
                return "town"

            player_pos = tuple(game_state["player_pos"])
            encountered = False  

            for monster in state["monsters"]:
                if (monster.x, monster.y) == player_pos:
                    print(f"\nYou encountered a {monster.monster_type}!")

                    state["player_hp"], state["player_gold"] = fight_monster(
                        state["player_hp"],
                        state["player_gold"],
                        monster
                    )

                    if state["player_hp"] <= 0:
                        print("You were defeated!")
                        return "town"

                    if monster.hp <= 0:
                        print("Monster defeated!")
                        state["monsters"].remove(monster)

                    encountered = True
                    break

            if not encountered:
                occupied = [tuple(game_state["player_pos"])]

                for m in state["monsters"]:
                    occupied.append((m.x, m.y))

                for m in state["monsters"]:
                    m.move(
                        occupied,
                        [tuple(game_state["town_pos"])],
                        10,
                        10
                    )

                player_pos = tuple(game_state["player_pos"])

                if player_pos in map_state.get("shrines", []):
                    print("\nYou discovered a mysterious shrine...")

                    effect = random.randint(1, 3)

                    if effect == 1:
                        state["player_hp"] += 10
                        print("The shrine heals you for 10 HP!")

                    elif effect == 2:
                        state["player_gold"] += 20
                        print("You find 20 gold at the shrine!")

                    elif effect == 3:
                        state["player_hp"] -= 5
                        print("A cursed energy drains 5 HP!")

                    map_state["shrines"].remove(player_pos)
                    
def save_game(filename):
    """Saves current game state to a file."""

    save_data = {
        "state": {
            "player_name": state["player_name"],
            "player_hp": state["player_hp"],
            "player_gold": state["player_gold"],
            "player_inventory": state["player_inventory"]
        },
        "map_state": map_state,
        "monsters": [m.to_dict() for m in state["monsters"]]
    }

    with open(filename, "w") as file:
        json.dump(save_data, file, indent=4)

    print("Game saved successfully!")

    
def load_game(filename):
    """Loads game state from a file."""
    global state, map_state

    if not os.path.exists(filename):
        print("Save file not found.")
        return False

    with open(filename, "r") as file:
        data = json.load(file)

    state.update(data["state"])
    map_state.update(data["map_state"])

    state["monsters"] = [
        WanderingMonster.from_dict(d) for d in data["monsters"]
    ]

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
        

    if "monsters" not in state:
        state["monsters"] = []

    if not state.get("monsters"):
        state["monsters"] = [
            WanderingMonster.random_spawn(
                occupied=[tuple(map_state["player_pos"]), tuple(map_state["town_pos"])],
                forbidden=[],
                grid_w=10,
                grid_h=10
            )
        ]


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
            result = run_map(map_state)


            player_pos = tuple(map_state["player_pos"])

                
            if len(state["monsters"]) == 0:
                for _ in range(2):
                    state["monsters"].append(
                        WanderingMonster.random_spawn(
                            occupied=[tuple(map_state["player_pos"]), tuple(map_state["town_pos"])],
                            forbidden=[],
                            grid_w=10,
                            grid_h=10
                        )
                    )

            if result == "town":
                print("You returned to town.")


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
            




if __name__ == "__main__":
    main()
