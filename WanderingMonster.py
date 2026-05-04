import random
import gamefunctions


class WanderingMonster:

    def __init__(self, x, y, monster_type, color, hp, power=3, money=10):
        self.x = x
        self.y = y
        self.monster_type = monster_type
        self.color = color
        self.hp = hp
        self.power = power       
        self.money = money

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "monster_type": self.monster_type,
            "color": list(self.color),
            "hp": self.hp,
            "power": self.power,
            "money": self.money
        }
    
    @classmethod
    def from_dict(cls, data):
        x = data.get("x", 0)
        y = data.get("y", 0)
        monster_type = data["monster_type"]
        color = tuple(data["color"])
        hp = data["hp"]
        power = data.get("power", 3)
        money = data.get("money", 10)
        
        return cls(x, y, monster_type, color, hp)
    
    @staticmethod
    def random_spawn(occupied, forbidden, grid_w, grid_h):

        while True:
            x = random.randint(0, grid_w - 1)
            y = random.randint(0, grid_h - 1)

            if (x, y) not in occupied and (x, y) not in forbidden:
                monster_data = gamefunctions.new_random_monster()

                if monster_data["name"] == "Werewolf":
                    color = (100, 100, 100)
                elif monster_data["name"] == "Vampire":
                    color = (150, 0, 150)
                elif monster_data["name"] == "Dragon":
                    color = (255, 0, 0)
                else:
                    color = (255, 255, 255)

                return WanderingMonster(
                    x,
                    y,
                    monster_data["name"],
                    color,
                    monster_data["health"],
                    monster_data["power"],
                    monster_data["money"]
                )
    def move(self, occupied, forbidden, grid_w, grid_h):

        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0)
        ]

        random.shuffle(directions)

        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy


            if new_x < 0 or new_x >= grid_w:
                continue
            if new_y < 0 or new_y >= grid_h:
                continue


            if (new_x, new_y) in occupied:
                continue
            if (new_x, new_y) in forbidden:
                continue


            self.x = new_x
            self.y = new_y
            return True

        return False
