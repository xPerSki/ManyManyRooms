from flask import Flask, render_template
import game

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


@app.route("/game")
def game():
    game_variables = {
        "room": 0,
        "health": 0,
        "damage": 0,
        "luck": 0,
    }
    return render_template("game.html", **game_variables)


if __name__ == "__main__":
    app.run(debug=True)
