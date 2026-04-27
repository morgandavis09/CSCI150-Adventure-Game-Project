import random


class WanderingMonster:

    def __init__(self, x, y, monster_type, color, hp):
        self.x = x
        self.y = y
        self.monster_type = monster_type
        self.color = color
        self.hp = hp

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "monster_type": self.monster_type,
            "color": list(self.color),
            "hp": self.hp
        }
    
    @classmethod
    def from_dict(cls, data):
        x = data.get("x", 0)
        y = data.get("y", 0)
        monster_type = data["monster_type"]
        color = tuple(data["color"])
        hp = data["hp"]

        return cls(x, y, monster_type, color, hp)
    
    @staticmethod
    def random_spawn(occupied, forbidden, grid_w, grid_h):

        while True:
            x = random.randint(0, grid_w - 1)
            y = random.randint(0, grid_h - 1)

            if (x, y) not in occupied and (x, y) not in forbidden:
                return WanderingMonster(x, y, "Goblin", (0, 255, 0), 10)

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
