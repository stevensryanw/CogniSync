#------------------ Importing Libraries ----------------
'''Data Manipulation'''
import random
'''Tkinter'''
from tkinter import *
import customtkinter as ctk
#------------------ Importing Libraries ----------------

#------------------ Variable Initializations -----------
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
#------------------ Variable Initializations -----------

#------------------ Main Snake Object ------------------
class Snake:
    """
    Represents a snake in the game.

    Attributes:
        coordinates (list): A list of coordinate pairs representing the snake's body segments.
        squares (list): A list of canvas squares representing the snake's body segments.
        canvas (Canvas): The canvas on which the snake is drawn.
    """
    def __init__(self, canvas):
        """
        Initializes a new instance of the Snake class.

        Args:
            canvas (Canvas): The canvas on which the snake is drawn.
        """
        body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []
        #defines location of snake (define canvas as the canvas the main game will execute in)
        self.canvas = canvas
        #puts snake at the middle of the board at the start
        for i in range(0, BODY_SIZE):
            self.coordinates.append([100, 100])
        #draws snake as rectangle in canvas and store coordinates
        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE, tag="snake")
            self.squares.append(square)
#------------------ Main Snake Object ------------------

#------------------ Main Food Object -------------------
class Food:
    """
    Represents the food in the game.

    Attributes:
        coordinates (list): The x and y coordinates of the food.
        canvas (Canvas): The canvas on which the food is drawn.
    """
    def __init__(self, canvas):
        """
        Initializes a new instance of the Food class.

        Args:
            canvas (Canvas): The canvas on which the food is drawn.
        """
        x = random.randint(0, int(WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        self.canvas = canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD, tag="food")
#------------------ Main Food Object -------------------

#------------------ Boundary Detection -----------------
def check_collisions(coordinates):
    """
    Checks if the snake has collided with the borders of the canvas.

    Parameters:
    coordinates (tuple): The x and y coordinates of the snake.

    Returns:
    bool: True if the snake has collided with the borders, False otherwise.
    """
    x, y = coordinates
    #checks if the snake has collided with the borders of the canvas
    #otherwise, the snake could move to infinity
    #checks horizontal boundary
    if x < 0 or x >= WIDTH-2:
        return True
    #checks vertical boundary
    elif y < 0 or y >= HEIGHT-2:
        return True
    return False
#------------------ Boundary Detection -----------------