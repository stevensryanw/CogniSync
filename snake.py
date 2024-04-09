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
FOOD = "#FF0000"
global score
global Snake
global Food
score = 0

class Snake:
    def __init__(self, canvas):
        body_size = BODY_SIZE
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
