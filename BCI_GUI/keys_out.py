#Script for outputting key presses the system

#Import libraries
import pyautogui

def key_press(key):
    pyautogui.press(key)
    return

key_press('left')