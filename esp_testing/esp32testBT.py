import tkinter as tk
import serial

ser = serial.Serial('/dev/tty.ESP32_LED_Control', 9600)  # Replace 'COMX' with your ESP32's serial port

def send_command(cmd):
    ser.write(cmd.encode())

def turn_on():
    print("Turning on")
    send_command('led_on')

def turn_off():
    print("Turning off")
    send_command('led_off')

root = tk.Tk()
root.title("ESP32 LED Control")

on_button = tk.Button(root, text="Turn On", command=turn_on)
on_button.pack()

off_button = tk.Button(root, text="Turn Off", command=turn_off)
off_button.pack()

root.mainloop()