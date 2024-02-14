# Program in Python to create a Snake Game

from tkinter import *
import customtkinter as ctk
import random


# Initialising Dimensions of Game
WIDTH = 500
HEIGHT = 500
SPEED = 200
SPACE_SIZE = 50
BODY_SIZE = 1
SNAKE = "#00FF00"
FOOD = "#FFFFFF"
BACKGROUND = "#000000"
global active
global g_food


    # Class to design the snake
class Snake:

    def __init__(self, canvas):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_SIZE):
            self.coordinates.append([250, 250])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE, tag="snake")
            self.squares.append(square)


# Class to design the food
class Food:

    def __init__(self, canvas):
        x = random.randint(0, int(WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y +
                        SPACE_SIZE, fill=FOOD, tag="food")


# Function to check the next move of snake
def next_turn(snake, food):
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

            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE,
                    y + SPACE_SIZE, fill=SNAKE)

            snake.squares.insert(0, square)

            if x == food.coordinates[0] and y == food.coordinates[1]:

                global score
                global g_food

                score += 1

                label.config(text="Points:{}".format(score))

                canvas.delete("food")

                g_food = Food()

            del snake.coordinates[-1]

            Canvas.delete(snake.squares[-1])

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


# function to check snake's collision and position
def check_collisions(coordinates):
    x, y = coordinates

    if x < 0 or x >= WIDTH-2:
        return True
    elif y < 0 or y >= HEIGHT-2:
        return True

    return False


    # Function to control everything
def game_over():
        global active

        active = False

        canvas.delete(ALL)
        canvas.create_text(canvas.winfo_width() / 2,
                        canvas.winfo_height() / 2,
                        font=('consolas', 70),
                        text="GAME OVER", fill="red",
                        tag="gameover")

def move(direction, snake, food):

        change_direction(direction)

        next_turn(snake, food)

    # Giving title to the gaming window
class GameFrame(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        ctk.CTkFrame.__init__(self, parent)
        frame1 = ctk.CTkFrame(parent)
        score=0
        direction='down'
        #frame1.pack()
        #canvas = Canvas(frame1, bg=BACKGROUND, height=HEIGHT, width=WIDTH)
        #canvas.pack()
        snake = Snake(canvas)
        g_food = Food(canvas)
        frame1.bind('<Left>',
            lambda event: move("left", snake, g_food))
        frame1.bind('<Right>',
            lambda event: move("right", snake, g_food))
        frame1.bind('<Up>',
            lambda event: move("up", snake, g_food))
        frame1.bind('<Down>',
            lambda event: move("down", snake, g_food))
        frame1.bind('<space>',
            lambda event: game_over())

active = True