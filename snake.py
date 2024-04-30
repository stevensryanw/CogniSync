from tkinter import *
import random
import customtkinter as ctk

'''Intialize variable for snake game objects'''
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

'''Main snake object'''
class Snake:
    def __init__(self, canvas):
        body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []
        # defines location of snake (define canavs as the canvas the main game will execute in)
        self.canvas = canvas
        # puts snake at the middle of the board at the start
        for i in range(0, BODY_SIZE):
            self.coordinates.append([100, 100])
        #draws snake as rectangle in canavas and store coordincates
        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE, tag="snake")
            self.squares.append(square)
'''Main food object'''
class Food:
    def __init__(self, canvas):
        #generates random location for food on initialization
        x = random.randint(0, int(WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        #stores food location information
        self.coordinates = [x, y]
        self.canvas = canvas
        #draws food as an oval in the game canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD, tag="food")

'''Determines if snake has run into the preset boundaries of the game'''
def check_collisions(coordinates):
    x, y = coordinates
    # checks if the snake has collided of the boarders of the canvas
    # otherwise, snake could move to infinity
    # checks horizontal boundary
    if x < 0 or x >= WIDTH-2:
        return True
     #checks vertical boundary
    elif y < 0 or y >= HEIGHT-2:
        return True
    return False
