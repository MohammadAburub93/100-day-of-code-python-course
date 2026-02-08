from flask import Flask
from random import randint

app = Flask(__name__)


@app.route("/")
def main_title():
    return ("<h1>Guess a number between 0 and 9</h1>"
            "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'/>")


random_num = randint(0,9)


@app.route("/<int:number>")
def user_choice(number):
    if number > random_num:
        return ("<h1 style='color:purple;'>Too High, try again</h1>"
                "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'/>")
    elif number < random_num:
        return ("<h1 style='color:red;'>Too Low, try again</h1>"
                "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'/>")
    elif number == random_num:
        return ("<h1 style='color:green;'>You found me</h1>"
                "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'/>")




if __name__ == "__main__":
    app.run(debug=True)