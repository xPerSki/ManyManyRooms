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
        self.room_number = num

    def get_enemies(self) -> str:
        return self.all_rooms[str(self.room_number)]["Enemies"]

    def get_items(self) -> str:
        return self.all_rooms[str(self.room_number)]["Items"]

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

    def get_health(self):
        return self.read_data().split(',')[0]

    def get_damage(self):
        return self.read_data().split(',')[1]

    def get_luck(self):
        return self.read_data().split(',')[2]

    def get_keys(self):
        return self.read_data().split(',')[3]
