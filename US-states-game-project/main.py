from turtle import Screen, Turtle
import pandas

TOTALSTATESNUMBER = 50
FONT = ("Arial", 10, "normal")

screen = Screen()
screen.title("Name the States")
screen.setup(width=725, height=491)
screen.bgpic("blank_states_img.gif")

states_data = pandas.read_csv("50_states.csv")
score = 0
guessed_states = []
states_names = states_data["state"].to_list()

while score < 50:
    user_choice = screen.textinput(title=f"{score}/{TOTALSTATESNUMBER} States Correct",
                                       prompt="What's another state name?").title()
    if user_choice == "Exit":
        not_guessed_states = [state for state in states_names if state not in guessed_states]
        states_to_learn = pandas.DataFrame(not_guessed_states)
        states_to_learn.to_csv("states_to_learn.csv")
        break
    elif user_choice in states_names and user_choice not in guessed_states:
        guessed_states.append(user_choice)
        score += 1
        writer = Turtle()
        writer.penup()
        writer.hideturtle()
        state_row = states_data[states_data.state == user_choice]
        x_cor = int(state_row.x)
        y_cor = int(state_row.y)
        writer.goto(x=x_cor, y=y_cor)
        writer.write(arg=user_choice, font=FONT)




