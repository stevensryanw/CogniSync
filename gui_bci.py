import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import os
from PIL import Image, ImageTk
from functools import partial
from snake import EmbeddedGameWindow
import random
import multiprocessing
from pyOpenBCI import OpenBCICyton
from pylsl import StreamInfo, StreamOutlet

LARGEFONT =("Verdana", 35)
WIDTH = 500
HEIGHT = 500
SPEED = 200
SPACE_SIZE = 50
BODY_SIZE = 1
SNAKE = "#00FF00"
FOOD = "#FF0000"
BACKGROUND = "#000000"

#make background gray
ctk.set_appearance_mode("dark")

class App(ctk.CTk):
        # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
        # __init__ function for class Tk
        ctk.CTk.__init__(self, *args, **kwargs)
        #self._set_appearance_mode("dark")
        # creating a container
        container = ctk.CTkFrame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        # initializing frames to an empty array
        self.frames = {}  
        # iterating through a tuple consisting
        # of the different page layouts
        #if a page is added it needs to be placed here
        for F in (Home, LiveFeed, Recorded, Model, snakeGame):
            frame = F(container, self)
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(Home)
        
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#first window frame startpage
class Home(ctk.CTkFrame):
    def __init__(self, parent, controller): 
        ctk.CTkFrame.__init__(self, parent)
        # label of frame Layout 2
        label = ctk.CTkLabel(self, text ="BCI Infinty", font = LARGEFONT)
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 4, padx = 100, pady = 10) 
        button1 = ctk.CTkButton(self, text ="Live Feed",corner_radius=25, 
        command = lambda : controller.show_frame(LiveFeed))
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 20)
        ## button to show frame 2 with text layout2
        button2 = ctk.CTkButton(self, text ="Recording Data",corner_radius=25,
        command = lambda : controller.show_frame(Recorded))
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 20)
        ## button to show model selection frame with
        button3 = ctk.CTkButton(self, text ="User Modeling",corner_radius=25,
        command = lambda : controller.show_frame(Model))
        # putting the button in its place by
        # using grid
        button3.grid(row = 3, column = 1, padx = 10, pady = 20)
        #including snake game page for now
        button4 = ctk.CTkButton(self, text = "Snake Game", corner_radius=25, 
        command = lambda : controller.show_frame(snakeGame))
        #places button to switch to snake game page
        button4.grid(row=4, column=1, padx=10, pady=20)

#second window frame page1 
class LiveFeed(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="Live Feed", font = LARGEFONT)
        #Later: Add a text input box for the user to enter the name of the file to be saved
        #Add a button to start live feed
        #Add a button to start recording
        #Add a button to stop recording
        label.grid(row = 0, column = 4, padx = 100, pady = 10)
        button1 = ctk.CTkButton(self, text ="Home",corner_radius=25,
                            command = lambda : controller.show_frame(Home))
        # putting the button in its place 
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 30)

#third window frame page2
class Recorded(ctk.CTkFrame): 
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.label = ctk.CTkLabel(self, text ="Recording Data", font = LARGEFONT)
        self.label.grid(row = 0, column = 4, padx = 100, pady = 10)

        self.instructions_label = ctk.CTkLabel(self, text="Follow the movement instructions below:")
        self.instructions_label.grid(row = 1, column = 4)

        self.canvas = ctk.CTkCanvas(self, width=400, height=400)
        self.canvas.grid(row = 2, column = 4, padx = 100, pady = 10)

        self.prepare_time = 5
        self.hold_time = 10
        self.rest_time = 10

        self.movements = ["Jaw Clench", "Move Right Arm", "Move Left Arm", "Move Legs"]
        self.shuffle_movements()

        self.current_movement_index = 0
        self.current_movement = None
        self.prompt_count = 0
        self.total_prompts = 4 * 40  # 4 movements, 40 times each

        self.start_button = ctk.CTkButton(self, text="Start Collecting", corner_radius=25, command=self.start_prompting)
        self.start_button.grid(row=2, column = 1, padx = 10, pady=30)

        self.home_button = ctk.CTkButton(self, text ="Home",corner_radius=25,
                            command = lambda : controller.show_frame(Home))
        
        self.home_button.grid(row = 1, column = 1, padx = 10, pady = 30)
        #data collection buttons
        #Begin collection (currently doing nothing)
        #Stop data collection
        self.stop_button = ctk.CTkButton(self, text="Stop Collecting", corner_radius=25, command=self.stop_prompting)
        self.stop_button.grid(row=3, column=1, sticky = "news", padx=10, pady=30)

        self.is_prompting = False  # Flag to check if prompting is in progress
        self.step_start_time = 0

    def start_prompting(self):
        self.start_button.configure(state=ctk.DISABLED)
        self.stop_button.configure(state=ctk.NORMAL)
        self.is_prompting = True
        self.prompt_next_movement()
        
    def stop_prompting(self):
        self.is_prompting = False
        self.start_button.configure(state=ctk.NORMAL)
        self.stop_button.configure(state=ctk.DISABLED)
        self.instructions_label.configure(text="Training canceled!")
        
        self.current_movement_index = 0
        self.shuffle_movements()
        self.prepare_time = 5
        self.hold_time = 10
        self.rest_time = 10
        if self.canvas.find_all():
            self.instructions_label.configure(text="Training canceled!")
            self.canvas.delete("all")
            open('tempVal.txt', 'w').close()
    
    def shuffle_movements(self):
        random.shuffle(self.movements)

    def prompt_next_movement(self):
        if self.prompt_count < self.total_prompts and self.is_prompting:
            self.instructions_label.configure(text="Prepare for the next movement...")
            self.canvas.delete("all")

            self.canvas.after(1000 * self.prepare_time, self.show_movement_instruction)
        else:
            self.instructions_label.configure(text="Training completed!")
            self.stop_prompting()
            open('tempVal.txt', 'w').close()

    def show_movement_instruction(self):
        if self.is_prompting:
            self.instructions_label.configure(text="Hold the movement for {} seconds".format(self.hold_time))
            self.current_movement = self.movements[self.current_movement_index]
            open('tempVal.txt', 'w').close()
            f = open("tempVal.txt", "a")
            f.write(self.current_movement)
            f.close()

            #makes 
            self.canvas.create_text(100, 100, text=self.current_movement)

            self.canvas.after(1000 * self.hold_time, self.show_rest_period)
        else:
            open('tempVal.txt', 'w').close()
            self.instructions_label.configure(text="Training canceled!")
            self.canvas.delete("all")
    
    def show_rest_period(self):
        if self.is_prompting:
            self.instructions_label.configure(text="Rest for {} seconds".format(self.rest_time))
            self.canvas.delete("all")
            open('tempVal.txt', 'w').close()

            self.prompt_count += 1
            self.current_movement_index = (self.current_movement_index + 1) % len(self.movements)
            if self.current_movement_index == 0:
                self.shuffle_movements()

            self.canvas.after(1000 * self.rest_time, self.prompt_next_movement)
            
    def start_record(self):
        SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count
        SCALE_FACTOR_AUX = 0.002 / (2**4)

        print("Creating LSL stream for EEG. \nName: OpenBCIEEG\nID: OpenBCItestEEG\n")

        info_eeg = StreamInfo('OpenBCIEEG', 'EEG', 8, 250, 'float32', 'OpenBCItestEEG')

        print("Creating LSL stream for AUX. \nName: OpenBCIAUX\nID: OpenBCItestEEG\n")

        info_aux = StreamInfo('OpenBCIAUX', 'AUX', 3, 250, 'float32', 'OpenBCItestAUX')

        outlet_eeg = StreamOutlet(info_eeg)
        outlet_aux = StreamOutlet(info_aux)

        file_out = open('newest_rename.csv', 'a')
        file_out.truncate(0)
        #tempVal = open('tempVal.txt', 'r')

        def lsl_streamers(sample):
            file_in = open('tempVal.txt', 'r')
            input = file_in.readline()
            lbl = ''
            #print(file_in.readline())
            if input != '':
                lbl = input
            else:
                lbl = 'norm'
            outlet_eeg.push_sample(np.array(sample.channels_data)*SCALE_FACTOR_EEG)
            outlet_aux.push_sample(np.array(sample.aux_data)*SCALE_FACTOR_AUX)
            #print(sample.channels_data*SCALE_FACTOR_EEG, sample.aux_data*SCALE_FACTOR_AUX, lbl)
            for datai in sample.channels_data:
                file_out.write(str(datai*SCALE_FACTOR_EEG) + ',')
            for dataj in sample.aux_data:
                file_out.write(str(dataj*SCALE_FACTOR_AUX) + ',')
            file_out.write(str(lbl) + '\n')
            file_in.close()

        board = OpenBCICyton()

        board.start_stream(lsl_streamers)
        file_out.close()

#Page 3: Model Selection, Data Input, Training, and Testing, and Result Visualization
class Model(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="User Modeling", font = LARGEFONT)
        label.grid(row = 0, column = 3, padx = 50, pady = 10)
        #Home button
        button1 = ctk.CTkButton(self, text ="Home",corner_radius=25, 
                            command = lambda : controller.show_frame(Home))
        # putting the button in its place 
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 30)
        
        ## dropdown option for the model label with options for models to run, function will run corresponding model
        model_dropdown = ctk.CTkComboBox(self, values = ["LDA", "SVM"])
        model_dropdown.grid(row=2, column = 1, padx=10, pady=10)

        #labels for the data dropdown
        Data_label = ctk.CTkLabel(self, text="Data")
        Data_label.grid(row=3, column=0, padx = 10, pady=10)

        ## dropdown option for the data that we will run into the model. select from csvs, will be populated from directory 
        Data_dropdown = ctk.CTkComboBox(self, values = ["Ryan.csv", "Gabe.csv"])
        Data_dropdown.grid(row=3, column = 1, padx=10, pady=10)

        ## Creating the file name label and setting it inside of our input frame
        txt_label = ctk.CTkLabel(self, text="File Name")
        ## Here I use grid to place a grid like section of labels, I want the prompt label at index 0
        txt_label.grid(row=4, column=0, padx = 10, pady = 10)

        ## Creating our textbox so user can input file name
        txt_entry = ctk.CTkTextbox(self, height=10)
        txt_entry.grid(row= 4, column =1, padx = 10, pady = 10)

        #will send the user back to the main menu
        run_button = ctk.CTkButton(self, text="Run")
        #put button on a grid
        run_button.grid(row=5, column=0, columnspan = 2, sticky = "news", padx=10, pady=10)

class snakeGame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
    
        button1 = ctk.CTkButton(self, text ="Home",corner_radius=25, 
                            command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 30)
        
        label = ctk.CTkLabel(self, text ="Snake Game", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 50, pady = 10)

        self.game_frame = EmbeddedGameWindow(self, 260, 260)
        self.game_frame.grid(row=1, column=2, padx=10, pady=10)
        #frame2.update()

class ThreadedConnection(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
    def run(self):
        SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count
        SCALE_FACTOR_AUX = 0.002 / (2**4)

        print("Creating LSL stream for EEG. \nName: OpenBCIEEG\nID: OpenBCItestEEG\n")

        info_eeg = StreamInfo('OpenBCIEEG', 'EEG', 8, 250, 'float32', 'OpenBCItestEEG')

        print("Creating LSL stream for AUX. \nName: OpenBCIAUX\nID: OpenBCItestEEG\n")

        info_aux = StreamInfo('OpenBCIAUX', 'AUX', 3, 250, 'float32', 'OpenBCItestAUX')

        outlet_eeg = StreamOutlet(info_eeg)
        outlet_aux = StreamOutlet(info_aux)

        file_out = open('newest_rename.csv', 'a')
        file_out.truncate(0)
        #tempVal = open('tempVal.txt', 'r')

        def lsl_streamers(sample):
            file_in = open('tempVal.txt', 'r')
            input = file_in.readline()
            lbl = ''
            #print(file_in.readline())
            if input != '':
                lbl = input
            else:
                lbl = 'norm'
            outlet_eeg.push_sample(np.array(sample.channels_data)*SCALE_FACTOR_EEG)
            outlet_aux.push_sample(np.array(sample.aux_data)*SCALE_FACTOR_AUX)
            #print(sample.channels_data*SCALE_FACTOR_EEG, sample.aux_data*SCALE_FACTOR_AUX, lbl)
            for datai in sample.channels_data:
                file_out.write(str(datai*SCALE_FACTOR_EEG) + ',')
            for dataj in sample.aux_data:
                file_out.write(str(dataj*SCALE_FACTOR_AUX) + ',')
            file_out.write(str(lbl) + '\n')
            file_in.close()

        board = OpenBCICyton()

        board.start_stream(lsl_streamers)
        file_out.close()

score = 0
direction = 'down'

# Driver Code
app = App()
#setting window size by pixels "widthxheight"
app.geometry("800x700")
app.update()
#with new size labels should shift right by increasing columns
app.mainloop()
