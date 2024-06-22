from random import randint
import json
import os


def roll_dice(n=6) -> int:
    return randint(1, n)


class Room:
    def __init__(self, num: int):
        with open("rooms.json", 'r') as file:
            content = file.read()

        self.all_rooms = json.loads(content)
        self.max_room = int(list(self.all_rooms.keys())[-1])
        self.room_number = num

    def check_enemies(self) -> bool:
        enemies = self.all_rooms[str(self.room_number)]["Enemies"]
        if enemies != "This room is clear" and enemies != "None" and "escaped" not in enemies:
            return True
        return False

    def get_enemies(self) -> str:
        plr = Player()
        if self.check_enemies():
            battle = plr.battle()
            if battle[0]:
                print("Won")
                plr.change_stat("health", -battle[1])
            else:
                print("Lost")
                plr.write_data("0,0,0,0")

        return self.all_rooms[str(self.room_number)]["Enemies"]

    def check_items(self):
        items = self.all_rooms[str(self.room_number)]["Items"]
        if items != "None":
            return True
        return False

    def get_items(self) -> str:
        items = self.all_rooms[str(self.room_number)]["Items"]
        plr = Player()
        if items != "None":
            stat_changes = {
                "health": ("health", 5),
                "starlit": ("health", 4),
                "herb": ("health", 3),
                "honey": ("health", 3),
                "phoenix": ("health", 1),
                "poison": ("health", -2),
                "poisonous": ("health", -2),
                "spikes": ("health", -1),
                "rotten": ("health", -1),
                "weakened potion": ("health", -1),

                "sword": ("damage", 3),
                "dagger": ("damage", 2),
                "broken axe": ("damage", -2),
                "damage potion": ("damage", -2),
                "strange vial": ("damage", -5),

                "map": ("luck", 2),
                "coin": ("luck", 1),
                "necklace": ("luck", 1),
                "locket": ("luck", 1),
                "pendant": ("luck", 1),
                "mysterious": ("luck", 1),
                "ring": ("luck", 1),
                "mirage": ("luck", 1),
                "gemstone": ("luck", 1),
                "charm": ("luck", 1),
                "amulet": ("luck", 1),
                "chain": ("luck", -2),
                "mirror": ("luck", -2),
                "cursed": ("luck", -3),
                "skull": ("luck", -3),

                "key": ("keys", 1),
            }
            for item, (stat, value) in stat_changes.items():
                if item in items.lower():
                    plr.change_stat(stat, value)
        return items

    def get_description(self) -> str:
        return self.all_rooms[str(self.room_number)]["Description"]


class Player:
    def __init__(self):
        if not os.path.isfile("player.mmr"):
            with open("player.mmr", 'w') as data:
                data.write("0,0,0,0")

    @staticmethod
    def wipe_data() -> None:
        with open("player.mmr", "w") as data:
            data.write("0,0,0,0")

    @staticmethod
    def write_data(arg) -> None:
        with open("player.mmr", 'w') as data:
            data.write(arg)

    @staticmethod
    def read_data() -> str:
        with open("player.mmr", 'r') as data:
            return data.read().strip()

    def generate_stats(self) -> None:
        health, damage, luck = roll_dice() * 2 + 6, roll_dice() * 2 + 3, roll_dice()
        self.write_data(f"{health},{damage},{luck},0")

    def change_stat(self, stat: str, n: int) -> None:
        stats = {
            "health": self.get_health(),
            "damage": self.get_damage(),
            "luck": self.get_luck(),
            "keys": self.get_keys()
        }
        old = stats[stat]
        new_values = {k: v for k, v in stats.items()}
        new_values[stat] = old + n
        self.write_data(f"{new_values['health']},{new_values['damage']},{new_values['luck']},{new_values['keys']}")

    def get_health(self) -> int:
        return int(self.read_data().split(',')[0])

    def get_damage(self) -> int:
        return int(self.read_data().split(',')[1])

    def get_luck(self) -> int:
        return int(self.read_data().split(',')[2])

    def get_keys(self) -> int:
        return int(self.read_data().split(',')[3])

    def battle(self):
        print("Fight")
        user_health = self.get_health()
        user_damage = self.get_damage()
        user_luck = self.get_luck()

        enemy_health, enemy_damage = randint(4, 12), randint(1, 8)
        user_luck *= 3

        damage_received = 0
        while True:
            crit = True if randint(1, 100) <= user_luck else False
            enemy_health -= user_damage * 2 if crit else user_damage
            if enemy_health <= 0:
                return True, damage_received

            user_health -= enemy_damage
            damage_received += enemy_damage
            if user_health <= 0:
                return False, None
