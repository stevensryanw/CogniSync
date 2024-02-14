from tkinter import *
import random
import customtkinter as ctk


BACKGROUND = 'black'
WIDTH = 260
HEIGHT = 260
SPEED = 200
SPACE_SIZE = 20
BODY_SIZE = 1
SNAKE = "#00FF00"
FOOD = "#FFFFFF"
global score
score = 0

class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []
        self.canvas = canvas

        for i in range(0, BODY_SIZE):
            self.coordinates.append([100, 100])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        x = random.randint(0, int(WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        self.canvas = canvas

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD, tag="food")

def check_collisions(coordinates):
    x, y = coordinates

    if x < 0 or x >= WIDTH-2:
        return True
    elif y < 0 or y >= HEIGHT-2:
        return True

    return False

def next_turn(snake, food, root, canvas):
    if active:
        global direction
        x, y = snake.coordinates[0]

        if direction == "up":
            y -= SPACE_SIZE
        elif direction == "down":
            y += SPACE_SIZE
        elif direction == "left":
            x -= SPACE_SIZE
        elif direction == "right":
            x += SPACE_SIZE

        if check_collisions((x,y)):
            direction = "collision"
        else:
            snake.coordinates.insert(0, (x, y))

            square = snake.canvas.create_rectangle(
                x, y, x + SPACE_SIZE,
                      y + SPACE_SIZE, fill=SNAKE)

            snake.squares.insert(0, square)

            if x == food.coordinates[0] and y == food.coordinates[1]:

                global score
                global g_food

                score += 1

                root.label = ctk.CTkLabel(root, text="Points:{}".format(score))

                snake.canvas.delete("food")

                g_food = Food(canvas)

            del snake.coordinates[-1]

            snake.canvas.delete(snake.squares[-1])

            del snake.squares[-1]


# Function to control direction of snake
def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        # if direction != 'right':
        direction = new_direction
    elif new_direction == 'right':
        # if direction != 'left':
        direction = new_direction
    elif new_direction == 'up':
        # if direction != 'down':
        direction = new_direction
    elif new_direction == 'down':
        # if direction != 'up':
        direction = new_direction

class EmbeddedGameWindow(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        ctk.CTkFrame.__init__(self, parent)
        self.label = ctk.CTkLabel(self, text="Points:{}".format(score))
        self.create_embedded_game(width, height)

    def create_embedded_game(self, width, height):
        # Create an instance of the Snake game
        self.snake_game = SnakeGame(width, height, self)

class SnakeGame:
    def __init__(self, width, height, parent_frame):
        global active
        global g_food

        active = True
        self.root = parent_frame
        self.window = ctk.CTkFrame(parent_frame)
        self.window.grid(row = 2, column = 1, padx = 10, pady = 30)
        self.canvas = Canvas(self.window, bg=BACKGROUND, height=height, width=width)
        self.canvas.pack()

        self.canvas.focus_set()

        self.snake = Snake(self.canvas)
        g_food = Food(self.canvas)

        # Initialize the rest of your game setup here

        self.window.update()

        # Key bindings
        self.canvas.bind('<Left>', lambda event: self.move("left"))
        self.canvas.bind('<Right>', lambda event: self.move("right"))
        self.canvas.bind('<Up>', lambda event: self.move("up"))
        self.canvas.bind('<Down>', lambda event: self.move("down"))
        self.canvas.bind('<space>', lambda event: self.game_over())
        print("setup done")

    def move(self, direction):
        print("move")
        global active
        if active:
            change_direction(direction)
            next_turn(self.snake, g_food, self.root, self.canvas)

    def game_over(self):
        global active
        active = False
        self.canvas.delete(ALL)
        self.canvas.create_text(self.canvas.winfo_width() / 2,
                                self.canvas.winfo_height() / 2,
                                font=('consolas', 70),
                                text="GAME OVER", fill="red",
                                tag="gameover")
