from flask import Flask, render_template
import game

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


@app.route("/game/room<int:room_number>")
def room(room_number):
    game_room = game.Room(room_number)
    game_player = game.Player()

    if room_number == 0:
        game_player.wipe_data()
        game_player.generate_stats()

    elif game_room.max_room < room_number < 777:
        room_number, game_room.room_number = 777, 777
    elif room_number > 777:
        room_number, game_room.room_number = 1337, 1337

    game_variables = {
        "room": room_number,
        "max_rooms": game_room.max_room,
        "description": game_room.get_description(),
        "items": game_room.get_items(),
        "enemies": game_room.get_enemies(),
        "health": game_player.get_health(),
        "damage": game_player.get_damage(),
        "luck": game_player.get_luck(),
        "keys": game_player.get_keys(),
        "left": game.roll_dice(m=2),
        "straight": game.roll_dice(m=4),
        "right": game.roll_dice(m=3),
        "fight": 1 if game_room.check_enemies() else 0
    }

    return render_template("game.html", **game_variables)


if __name__ == "__main__":
    app.run(debug=True)
