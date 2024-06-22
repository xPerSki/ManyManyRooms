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

    game_variables = {
        "room": room_number,
        "description": game_room.get_description(),
        "enemies": game_room.get_enemies(),
        "items": game_room.get_items(),
        "health": game_player.get_health(),
        "damage": game_player.get_damage(),
        "luck": game_player.get_luck(),
        "keys": game_player.get_keys(),
        "left": game.roll_dice(3),
        "straight": game.roll_dice(3),
        "right": game.roll_dice(3),
    }
    return render_template("game.html", **game_variables)


if __name__ == "__main__":
    app.run(debug=True)
