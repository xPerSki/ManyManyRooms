from random import randint
import json


class Room:
    def __init__(self, num: int):
        with open("rooms.json", 'r') as file:
            content = file.read()

        self.all_rooms = json.loads(content)
        self.room_number = num

    def get_enemies(self):
        return self.all_rooms[self.room_number]["Enemies"]

    def get_items(self):
        return self.all_rooms[self.room_number]["Items"]

    def get_description(self):
        return self.all_rooms[self.room_number]["Description"]


def roll_dice() -> int:
    return randint(1, 6)
