import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import os
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
from functools import partial
from snake import *
import random
from pyOpenBCI import OpenBCICyton
from pylsl import StreamInfo, StreamOutlet
import threading
import multiprocessing
import time
from model_bci import *
from connect import *
import shutil
import plotly.express as px
import wheelchairController as wcc
import joblib

LARGEFONT =("Verdana", 35)
WIDTH = 500
HEIGHT = 500
SPEED = 200
SPACE_SIZE = 20
BODY_SIZE = 1
SNAKE = "#00FF00"
FOOD = "#FF0000"
BACKGROUND = "#000000"

#ensuring this is repo is here and is current cwd
if os.path.isdir("../CogniSync"):
    pathDir = os.path.abspath("../CogniSync")
    print(pathDir)
    while os.getcwd() != pathDir:
        print("Directory is wrong")
        os.chdir(pathDir)
        print("Directory changed to "+pathDir)
#once ensured then check if folder data exists
parentDir = pathDir+"/"
extraDir = "data"
dataPath = os.path.join(pathDir, extraDir)
modelPath = os.path.join(pathDir, "models")
print(dataPath)
#if it does then take list of files in there
if os.path.isdir("../CogniSync/data"):
    dataPath = os.path.abspath("../CogniSync/data")
    dataFiles = os.listdir(dataPath)
    if len(dataFiles)==0:
        dataFiles = ["No Current Files"]
#if not then create and give the string no files currently
else:
    os.mkdir(dataPath)
    dataFiles = ["No Current Files"]
#will do a similar thing to data later just making it the same as data for now
print(modelPath)
#if it does then take list of files in there
if os.path.isdir("../CogniSync/models"):
    modelPath = os.path.abspath("../CogniSync/models")
    modelFiles = os.listdir(modelPath)
    if len(modelFiles)==0:
        modelFiles = ["No Current Files"]
#if not then create and give the string no files currently
else:
    os.mkdir(dataPath)
    modelFiles = ["No Current Files"]

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
        for F in (Home, PlotEEG, UserRecording, Modeling, SnakeGame, USBOutput):
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
        label = ctk.CTkLabel(self, text ="CogniSync", font = LARGEFONT)
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 4, padx = 100, pady = 10) 
        button1 = ctk.CTkButton(self, text ="Live Feed",corner_radius=25, 
        command = lambda : controller.show_frame(PlotEEG))
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady= 20)
        ## button to show frame 2 with text layout2
        button2 = ctk.CTkButton(self, text ="Recording Data",corner_radius=25,
        command = lambda : controller.show_frame(UserRecording))
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 20)
        ## button to show model selection frame with
        button3 = ctk.CTkButton(self, text ="Modeling",corner_radius=25,
        command = lambda : controller.show_frame(Modeling))
        # putting the button in its place by
        # using grid
        button3.grid(row = 3, column = 1, padx = 10, pady = 20)
        #including snake game page for now
        button4 = ctk.CTkButton(self, text = "Snake Game", corner_radius=25, 
        command = lambda : controller.show_frame(SnakeGame))
        #places button to switch to snake game page
        button4.grid(row=4, column=1, padx=10, pady=20)
        #including USB output page for now
        button5 = ctk.CTkButton(self, text = "USB Output", corner_radius=25,
        command = lambda : controller.show_frame(USBOutput))
        #places button to switch to USB output page
        button5.grid(row=5, column=1, padx=10, pady=20)

class PlotEEG(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="Plot EEG Data", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 100, pady = 10)
        button1 = ctk.CTkButton(self, text ="Home",corner_radius=25,
                            command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 30)
        #labels for the data dropdown
        Data_label = ctk.CTkLabel(self, text="Data File")
        Data_label.grid(row=3, column=0, padx = 10, pady=10)

        #dropdown option for the data that we will plot in plotly
        self.Data_dropdown = ctk.CTkComboBox(self, values = dataFiles)
        self.Data_dropdown.grid(row=3, column = 1, padx=10, pady=10)

        #button to show the eeg data with labels
        button2 = ctk.CTkButton(self, text ="Show EEG Data",corner_radius=25, command=self.plot_eeg)
        button2.grid(row = 4, column = 1, padx = 10, pady = 30)

    def plot_eeg(self):
        dataSelected = self.Data_dropdown.get()
        dataPath = os.path.join(pathDir, "data", dataSelected)
        data = pd.read_csv(dataPath)
        data.dropna()
        interval_default = [0, 100000]
        interval1 = interval_default[0]
        interval2 = interval_default[1]
        data = data[interval1:interval2]
        data = data.drop(columns=data.columns[8:11])
        temp_save = ''
        fig = px.line(data, x=data.index, y=data.columns[0:8], title='EEG data with movement labels as vertical bars')
        fig.update_layout(legend_title_text='Channels')
        legend = {'0.0': 'Channel 1', '0.0.1': 'Channel 2', '0.0.2': 'Channel 3', '0.0.3': 'Channel 4', '0.0.4': 'Channel 5', '0.0.5': 'Channel 6', '0.0.6': 'Channel 7', '0.0.7': 'Channel 8'}
        fig.for_each_trace(lambda t: t.update(name=legend[t.name]))

        #lets add vertical colored bars for the first of each movement sample
        #legend2 = {'Move Left Arm': 'red', 'Move Right Arm': 'blue', 'Move Legs': 'green', 'Jaw Clench': 'purple'} 
        legend2 = {'left arm': 'red', ' right arm': 'blue', ' legs': 'green', ' jaw': 'purple'} 
        
        #lets add legend2 to the plot
        fig.update_layout(showlegend=True)

        for i in range(interval1, interval2):
            if data.iloc[i, 8] != 'norm' and data.iloc[i, 8] != temp_save:
                temp_save = data.iloc[i, 8]
                fig.add_vline(x=i, line_dash='dash', line_color=legend2[data.iloc[i, 8]])
                #print(move_colors[ryan_test.iloc[i, 8]])
        print(legend2)
        fig.show()

#third window frame page2
class UserRecording(ctk.CTkFrame): 
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
        self.movements = []
        self.n_movements = []
        self.shuffle_movements()
        self.current_movement_index = 0
        self.current_movement = None
        self.prompt_count = 0
        

        txt_label = ctk.CTkLabel(self, text="Movement Input")
        ## Here I use grid to place a grid like section of labels, I want the prompt label at index 0
        txt_label.grid(row=4, column=0, padx = 10, pady = 10)

        ## Creating our textbox so user can input file name

        txt_entry = ctk.CTkEntry(self, height=10, placeholder_text="ENTER MOVEMENTS SEPERATED BY COMMA",  width = 300)
        txt_entry.grid(row= 4, column =1, padx = 10, pady = 10)
        self.text_entry = txt_entry
        
        self.text_entry.bind("<KeyRelease>", self.update_movements)
        #self.length = len(self.movements)
        self.total_prompts = 4 * 40  # 4 movements, 40 times each
        
        output_label = ctk.CTkLabel(self, text="Output file")
        ## Here I use grid to place a grid like section of labels, I want the prompt label at index 0
        output_label.grid(row=5, column=0, padx = 10, pady = 10)

        ## Creating our textbox so user can input file name

        out_entry = ctk.CTkEntry(self, height=10, placeholder_text="FILE_NAME.csv",  width = 300)
        out_entry.grid(row= 5, column =1, padx = 10, pady = 10)
        self.file_out = out_entry

    



        self.start_button = ctk.CTkButton(self, text="Start Collecting", corner_radius=25, command=self.start_prompting)
        self.start_button.grid(row=2, column = 1, padx = 10, pady=30)
        self.home_button = ctk.CTkButton(self, text ="Home",corner_radius=25,
                            command = lambda : controller.show_frame(Home))
        self.home_button.grid(row = 1, column = 1, padx = 10, pady = 30)
        #data collection buttons
        #Begin collection (currently doing nothing)
        #Stop data collection
        self.stop_button = ctk.CTkButton(self, text="Stop Collecting", corner_radius=25, command=self.stop_prompting)
        self.stop_button.grid(row=3, column=1, padx=10, pady=30)
        self.is_prompting = False  # Flag to check if prompting is in progress
        self.step_start_time = 0
        self.record_thread = None


    def update_movements(self, event):
        # Get the text entered by the user
        movements_text = self.text_entry.get()
        # Update the movements array
        self.movements = movements_text.split(",")


    def start_prompting(self):
        self.start_button.configure(state=ctk.DISABLED)
        self.stop_button.configure(state=ctk.NORMAL)
        self.is_prompting = True
        self.prompt_next_movement()
        self.start_record()
        #Allow stream to start before prompting
        time.sleep(15)

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
            #open('tempVal.txt', 'w').close()
            
        self.stop_record()

    def end_prompting(self):
        self.is_prompting = False
        self.start_button.configure(state=ctk.NORMAL)
        self.stop_button.configure(state=ctk.DISABLED)
        self.instructions_label.configure(text="training completed!")
        my_outputFile = self.file_out.get()
        self.f = open(my_outputFile, "x")
        shutil.copyfile("newest_rename.csv", my_outputFile)
        self.current_movement_index = 0
        self.shuffle_movements()
        self.prepare_time = 5
        self.hold_time = 10
        self.rest_time = 10

        if self.canvas.find_all():
            self.instructions_label.configure(text="Training is completed!")
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
            self.instructions_label.configure(text="Training maybe completed!")
            self.end_prompting()
            open('tempVal.txt', 'w').close()

    def show_movement_instruction(self):
        if self.is_prompting:
            self.instructions_label.configure(text="Hold the movement for {} seconds".format(self.hold_time))
            self.current_movement = self.movements[self.current_movement_index]
            self.after(2000, self.start_writing_to_file)
            self.after(6000, self.stop_writing_to_file)
            self.canvas.create_text(100, 100, text=self.current_movement, font=("Helvetica", 30))
            self.canvas.after(1000 * self.hold_time, self.show_rest_period)
        else:
            open('tempVal.txt', 'w').close()
            self.instructions_label.configure(text="Training canceled!")
            self.canvas.delete("all")

    def start_writing_to_file(self):
        # Open the file for writing after 2 seconds
        open('tempVal.txt', 'w').close()
        f = open("tempVal.txt", "a")
        f.write(self.current_movement)
        f.close()
    
    def stop_writing_to_file(self):
        # Close the file when the middle 7 seconds end
        open('tempVal.txt', 'a').close()  # Make sure the file is closed

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
        if self.record_thread is None or not self.record_thread.is_alive():
            self.record_thread = threading.Thread(target=self.record_data)
            self.record_thread.start()

    def stop_record(self):
        if self.record_thread is not None and self.record_thread.is_alive():
            self.record_thread.join()

    def record_data(self):
        record(self)

#Page 3: Model Selection, Data Input, Training, and Testing, and Result Visualization
class Modeling(ctk.CTkFrame):
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

        #label for model dropdown
        modelLabel = ctk.CTkLabel(self, text="Model")
        modelLabel.grid(row=2, column=0, padx=10, pady=10)
        
        # dropdown option for the model label with options for models to run, function will run corresponding model
        self.model_dropdown = ctk.CTkComboBox(self, values = ["LDA", "SVC", "Random Forest Classifier", "Tensorflow", "Decision Tree Classifier", 
                                                              "Logistic Regression", "QDA", "Gradient Boosting Classifier", "KNN", 
                                                              "Gaussian NB", "MLP Classifier"])
        self.model_dropdown.grid(row=2, column = 1, padx=10, pady=10)

        #labels for the data dropdown
        Data_label = ctk.CTkLabel(self, text="Data File")
        Data_label.grid(row=3, column=0, padx = 10, pady=10)

        ## dropdown option for the data that we will run into the model. select from csvs, will be populated from directory 
        self.Data_dropdown = ctk.CTkComboBox(self, values = dataFiles)
        self.Data_dropdown.grid(row=3, column = 1, padx=10, pady=10)
        
        #dropdown to choose the labels
        dataFiles.insert(0, "No Label File")
        self.Labels_dropdown = ctk.CTkComboBox(self, values = dataFiles)
        self.Labels_dropdown.grid(row=4, column=1, padx=10, pady=10)
        dataFiles.pop(0)

        #frame label for label dropdown
        Label_label = ctk.CTkLabel(self, text = "Label File")
        Label_label.grid(row=4, column=0, padx=10, pady=10)

        ## Creating the file name label and setting it inside of our input frame
        txt_label = ctk.CTkLabel(self, text="Output File Name")
        ## Here I use grid to place a grid like section of labels, I want the prompt label at index 0
        txt_label.grid(row=5, column=0, padx = 10, pady = 10)

        ## Creating our textbox so user can input file name
        txt_entry = ctk.CTkEntry(self, height=10, placeholder_text="output.txt")
        txt_entry.grid(row= 5, column =1, padx = 10, pady = 10)
        self.text = txt_entry

        #update the datafile list
        update_button = ctk.CTkButton(self, text="Update File Lists", command = self.updateFiles)
        update_button.grid(row=6, column=0, columnspan=2, sticky="news", padx=10, pady=10)

        #will send the user back to the main menu
        run_button = ctk.CTkButton(self, text="Run", command=self.model_input)
        #put button on a grid
        run_button.grid(row=7, column=0, columnspan = 2, sticky = "news", padx=10, pady=10)

    def model_input(self):
        modelSelected = self.model_dropdown.get()
        dataSelected = self.Data_dropdown.get()
        labelsSelected = self.Labels_dropdown.get()
        outputFile = self.text.get()
        print(modelSelected)
        print(dataSelected)
        print(labelsSelected)
        print(outputFile)
        self.relPath = "../CogniSync/data/"
        if modelSelected == "LDA":
            phrase = ctk.CTkLabel(self, text="Time is a circle. You're your own grandpa.", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray = self.csvProcessing(dataSelected, labelsSelected)
            results = BCI_sklearn_LinearDiscriminantAnalysis(dataArray, labelsArray)

        elif modelSelected == "Gradient Boosting Classifier":
            phrase = ctk.CTkLabel(self, text="Booster rockets deployed", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray = self.csvProcessing(dataSelected, labelsSelected)
            print('going into modeling')
            results = BCI_sklearn_GradientBoostingClassifier(dataArray, labelsArray)

        elif modelSelected == "KNN":
            phrase = ctk.CTkLabel(self, text="Apartment complex", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray = self.csvProcessing(dataSelected, labelsSelected)
            print('going into modeling')
            results = BCI_sklearn_KNeighborsClassifier(dataArray, labelsArray)

        elif modelSelected == "Gaussian NB":
            phrase = ctk.CTkLabel(self, text="Math GOAT", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray = self.csvProcessing(dataSelected, labelsSelected)
            print('going into modeling')
            results = BCI_sklearn_GaussianNB(dataArray, labelsArray)

        elif modelSelected == "MLP Classifier":
            phrase = ctk.CTkLabel(self, text="Let's go dodgers, Let's go", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray = self.csvProcessing(dataSelected, labelsSelected)
            print('going into modeling')
            results = BCI_sklearn_MLPClassifier(dataArray, labelsArray)

        elif modelSelected == "SVC":
            phrase = ctk.CTkLabel(self, text="Get Vectored! *air horn noise*", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray = self.csvProcessing(dataSelected, labelsSelected)
            print('going into modeling')
            results = BCI_sklearn_SVC(dataArray, labelsArray)
            
        elif modelSelected == "Tensorflow":
            phrase = ctk.CTkLabel(self, text="Tensions between people flow to others.", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray = self.csvProcessing(dataSelected, labelsSelected)
            results = BCI_tensorflow_Net(dataArray, labelsArray)

        elif modelSelected == "Random Forest Classifier":
            phrase = ctk.CTkLabel(self, text="Trees are the breath of life", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray = self.csvProcessing(dataSelected, labelsSelected)
            results = BCI_sklearn_RandomForestClassifier(dataArray, labelsArray)

        elif modelSelected == "Decision Tree Classifier":
            phrase = ctk.CTkLabel(self, text="Decisions and Trees", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray = self.csvProcessing(dataSelected, labelsSelected)
            results = BCI_sklearn_DecisionTreeClassifier(dataArray, labelsArray)

        elif modelSelected == "Logistic Regression":
            phrase = ctk.CTkLabel(self, text="Logging onto the mainframe", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray = self.csvProcessing(dataSelected, labelsSelected)
            results = BCI_sklearn_LogisticRegression(dataArray, labelsArray)

        elif modelSelected == "QDA":
            phrase = ctk.CTkLabel(self, text="Quads for the win", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray = self.csvProcessing(dataSelected, labelsSelected)
            results = BCI_sklearn_QuadraticDiscriminantAnalysis(dataArray, labelsArray)

        if modelSelected == "Tensorflow":
            waitLabel.configure(text="Results")
            metrics = ctk.CTkLabel(self, text="Accuracy: {:.3f}".format(results[0]), font=("Verdana", 18))
            metrics.grid(row=4, column=3, padx=10, pady=10)
            nodes = ctk.CTkLabel(self, text=results[1], font=("Verdana", 18))
            nodes.grid(row=5, column=3, padx=10, pady=10)
            if outputFile == "" or outputFile == " ":
                dataName = dataSelected[:-4]
                outputFile = modelSelected+dataName+"Output.txt"
                f = open(self.relPath+outputFile, "a")
                f.write("Model Name: "+modelSelected+"\n")
                f.write("Score: "+str(results[0])+"\n")
                f.write("Parameters: "+str(results[1])+"\n")
                f.close()
                print("File Name: "+outputFile)
            else:
                f = open(self.relPath+outputFile, "a")
                f.write("Model Name: "+modelSelected+"\n")
                f.write("Score: "+str(results[0])+"\n")
                f.write("Parameters: "+str(results[1])+"\n")
                f.close()
        else:
            waitLabel.configure(text="Results")
            metrics = ctk.CTkLabel(self, text="Accuracy: {:.3f} F1 Score: {:.3f} Precision: {:.3f} Recall: {:.3f}".format(
                results[0], results[1], results[2], results[3]), font=("Verdana", 18))
            metrics.grid(row=4, column=3, padx=10, pady=10)
            if outputFile == "" or outputFile == " ":
                dataName = dataSelected[:-4]
                outputFile = modelSelected+dataName+"Fitted.pkl"
                joblib.dump(results[4], modelPath+"/"+outputFile)
                print("File Name: "+outputFile)
            else:
                joblib.dump(results[4], modelPath+"/"+outputFile)


    def updateFiles(self):
        dataFiles = os.listdir(dataPath)
        if len(dataFiles)==0:
            dataFiles = "No Current Files"
            self.Data_dropdown.configure(values=dataFiles)
            self.Labels_dropdown.configure(values=dataFiles)
        else:
            self.Data_dropdown.configure(values=dataFiles)
            dataFiles.insert(0, "No Label File")
            self.Labels_dropdown.configure(values=dataFiles)
            dataFiles.pop(0) 

    def csvProcessing(self, dataFile, labelFile):
        if labelFile == "No Label File":
            #do stuff like ryan.csv
            dataTemp = dataPath+"/"+dataFile
            df = pd.read_csv(dataTemp, 
                 names=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "labels"])
            df.dropna(inplace=True)
            names = df["labels"].unique()
            mapping = {}
            count = 0
            for x in names:
                mapping[x] = str(count)
                count += 1
            df2 = df["labels"]
            df.drop(columns=['labels'], inplace=True)
        #if they are different files
        else:
            dataTemp = dataPath+"/"+dataFile
            labelsTemp = dataPath+"/"+labelFile
            df = pd.read_csv(dataTemp)
            df2 = pd.read_csv(labelsTemp)
            columnNames = list(df2.columns)
            names = df2[columnNames[0]].unique()
            mapping = {}
            count = 0
            for x in names:
                mapping[x] = float(count)
                count += 1
        df2 = df2.replace(mapping)
        df2 = df2.astype('float64')
        dataArray = df.to_numpy()
        labelsArray = df2.to_numpy()
        return [dataArray, labelsArray]

class SnakeGame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
    
        button1 = ctk.CTkButton(self, text ="Home",corner_radius=25, 
                            command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 30)
        
        label = ctk.CTkLabel(self, text ="Snake Game", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 50, pady = 10)

        button2 = ctk.CTkButton(self, text = 'Snake Begin', corner_radius = 25, command = self.drawFrame)
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
        global active
    def drawFrame(self):
        global canvas
        global snake
        global g_food
        global active
        global pointCount
        active = True
        score = 0
        canvas = ctk.CTkCanvas(self, bg='black', height=260, width=260)
        canvas.grid(row=2, column=2, padx=10, pady=10)
        pointCount = ctk.CTkLabel(self, text="Points: {}".format(score), font=LARGEFONT)
        pointCount.grid(row=1, column=2, padx=10, pady=10)
        snake = Snake(canvas)
        g_food = Food(canvas)
        root = SnakeGame
        app.bind('<Left>', lambda event: self.move("left", snake, g_food, root, canvas))
        app.bind('<Right>', lambda event: self.move("right", snake, g_food, root, canvas))
        app.bind('<Up>', lambda event: self.move("up", snake, g_food, root, canvas))
        app.bind('<Down>', lambda event: self.move("down", snake, g_food, root, canvas))
        app.bind('<space>', lambda event: self.game_over())

#snake stuff copied over look over to make sure it creates everything
    def move(self, direction, snake, g_food, root, canvas):
        #print("move")
        global active
        if active:
            self.change_direction(direction)
            self.next_turn(snake, g_food, root, canvas) 

    def game_over(self):
        global active
        active = False
        canvas.delete(ALL)
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 30), 
                           text="GAME OVER", fill="red", tag="gameover")
        
    def change_direction(self, new_direction):
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

    def check_collisions(self, coordinates):
        x, y = coordinates

        if x < 0 or x >= WIDTH-2:
            return True
        elif y < 0 or y >= HEIGHT-2:
            return True
        return False

    def next_turn(self, snake, food, root, canvas):
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
                    pointCount.configure(text="Points: {}".format(score))
                    snake.canvas.delete("food")
                    g_food = Food(canvas)
                del snake.coordinates[-1]
                snake.canvas.delete(snake.squares[-1])
                del snake.squares[-1]

#second window frame page1 
class USBOutput(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="USB Output", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 100, pady = 10)
        button1 = ctk.CTkButton(self, text ="Home",corner_radius=25,
                            command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 30)
        buttonForeward = ctk.CTkButton(self, text ="Forward",
                            command = lambda : wcc.motorForward())
        buttonForeward.grid(row = 2, column = 4, pady = 12)
        buttonLeft = ctk.CTkButton(self, text ="Left",
                            command = lambda : wcc.turnLeft())
        buttonLeft.grid(row = 3, column = 3)
        buttonStop = ctk.CTkButton(self, text ="Stop",
                            command = lambda : wcc.motorStop())
        buttonStop.grid(row = 3, column = 4, pady = 12)
        buttonRight = ctk.CTkButton(self, text ="Right",
                            command = lambda : wcc.turnRight())
        buttonRight.grid(row = 3, column = 5)
        buttonBackward = ctk.CTkButton(self, text ="Backward",
                            command = lambda : wcc.motorBackward())
        buttonBackward.grid(row = 4, column = 4, pady = 12)

        #dropbox for models        
        self.modelDropdown = ctk.CTkComboBox(self, values = modelFiles)
        self.modelDropdown.grid(row=5, column = 1, padx=10, pady=10)
        #update the model list
        update_button = ctk.CTkButton(self, text="Update Model Lists", command = self.updateFiles)
        update_button.grid(row=6, column=1, columnspan=1, sticky="news", padx=10, pady=10)
        #button for model selection
        self.selectButton = ctk.CTkButton(self, text="Select Model", command = self.modelSelection)
        self.selectButton.grid(row=7, column=1, padx=10, pady=10)
        #button to start the prediction
        self.predictButton = ctk.CTkButton(self, text="Predict", command = self.predictStream)
        self.predictButton.grid(row=8, column=1, padx=10, pady=10)
        #button to stop the prediction
        self.stopButton = ctk.CTkButton(self, text="Stop Prediction", command = self.stop_predictions)
        self.stopButton.grid(row=9, column=1, padx=10, pady=10)

        self.model = False
        self.update()

        self.bind('<Left>', lambda event: wcc.turnLeft())
        self.bind('<Right>', lambda event: wcc.turnRight())
        self.bind('<Up>', lambda event: wcc.motorForward())
        self.bind('<Down>', lambda event: wcc.motorBackward())
        self.bind('<space>', lambda event: wcc.motorStop())
        self.record_thread = None
        self.stop_predict = True

    def start_record(self):
        if self.record_thread is None or not self.record_thread.is_alive():
            self.record_thread = threading.Thread(target=self.record_data)
            self.record_thread.start()

    def stop_record(self):
        if self.record_thread is not None and self.record_thread.is_alive():
            self.record_thread.join()

    def record_data(self):
        record(self)

    #update list of models
    def updateFiles(self):
        modelFiles = os.listdir(modelPath)
        if len(modelFiles)==0:
            modelFiles = "No Current Files"
            self.modelDropdown.configure(values=modelFiles)
        else:
            self.modelDropdown.configure(values=modelFiles)

    def modelSelection(self):
        modelSelected = self.modelDropdown.get()
        print(modelSelected[-3:])
        if modelSelected[-3:] == "pkl":
            self.model = joblib.load(modelPath+"/"+modelSelected)
        else:
            self.model = False

    def stop_predictions(self):
        self.stop_predict = False

    def predictStream(self):
        self.start_record()
        #Allow stream to start before prompting
        time.sleep(15)
        if self.stop_predict is True:
            stream = pd.read_csv('newest_rename.csv')
            stream = stream.iloc[:, 0:11]
            if stream.loc[len(stream)-1].isnull().values.any():
                stream = stream.dropna()
            stream_latest = stream.loc[len(stream)-1]
            #remove the header from stream_latest
            stream_latest = stream_latest.to_numpy()
            prediction = self.model.predict(stream_latest.reshape(1, -1))
            print(prediction)
            if prediction == 2:
                wcc.motorForward()
            elif prediction == 1:
                wcc.turnLeft()
            elif prediction == 4:
                wcc.turnRight()
            elif prediction == 0:
                wcc.motorBackward()
            elif prediction == 3:
                wcc.motorStop()
            else:
                wcc.motorStop()
        else:
            wcc.motorStop()
            self.stop_record()


score = 0
direction = 'down'

# Driver Code
app = App()
#setting window size by pixels "width x height"
app.geometry("800x700")
app.update()
#with new size labels should shift right by increasing columns
app.mainloop()