from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100  # Increased for better playability
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
BORDER_COLOR = "#FFFFFF"
FONT_STYLE = ('consolas', 40)
BUTTON_FONT_STYLE = ('consolas', 20)

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)


class Food:

    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")


def start_game():
    global snake, food, score, direction
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    Label.config(text="Score:{}".format(score))
    canvas.delete("start", "gameover")
    next_turn(snake, food)


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        Label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    opposites = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}

    if opposites.get(new_direction) != direction:
        direction = new_direction


def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 50,
                       font=FONT_STYLE, text="GAME OVER", fill="red", tags="gameover")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 50,
                       font=BUTTON_FONT_STYLE, text="Press Enter to Restart", fill="white", tags="gameover")
    window.bind('<Return>', lambda event: start_game())


window = Tk()
window.title("SNAKE GAME")
window.resizable(False, False)

score = 0
direction = 'down'

Label = Label(window, text="Score:{}".format(score), font=FONT_STYLE)
Label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Draw borders
canvas.create_line(0, 0, GAME_WIDTH, 0, fill=BORDER_COLOR)
canvas.create_line(0, 0, 0, GAME_HEIGHT, fill=BORDER_COLOR)
canvas.create_line(GAME_WIDTH, 0, GAME_WIDTH, GAME_HEIGHT, fill=BORDER_COLOR)
canvas.create_line(0, GAME_HEIGHT, GAME_WIDTH, GAME_HEIGHT, fill=BORDER_COLOR)

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Add start screen
canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 50,
                   font=FONT_STYLE, text="SNAKE GAME", fill="green", tags="start")
canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 50,
                   font=BUTTON_FONT_STYLE, text="Press Enter to Start", fill="white", tags="start")
window.bind('<Return>', lambda event: start_game())

window.mainloop()
