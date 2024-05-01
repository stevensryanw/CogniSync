#------------------ Importing Libraries -----------------
'''Tkinter'''
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from PIL import ImageTk
import PIL.Image
'''Data Manipulation'''
import numpy as np
import pandas as pd
import random
import time
'''Headset Connection'''
from pyOpenBCI import OpenBCICyton
from pylsl import StreamInfo, StreamOutlet
from connect import *
'''Plotting'''
import plotly.express as px
import plotly.graph_objects as go
'''Modeling'''
from model_bci import *
import joblib
from functools import partial
'''Snake Game'''
from snake import *
'''USB Output'''
import wheelchairController as wcc
'''Threading'''
import threading
import multiprocessing
'''File Management'''
import os
import shutil
#------------------ Importing Libraries -----------------

#------------------ Variable Initializations ------------
LARGEFONT =("Verdana", 35)
WIDTH = 500
HEIGHT = 500
SPEED = 200
SPACE_SIZE = 20
BODY_SIZE = 1
SNAKE = "#00FF00"
FOOD = "#FF0000"
BACKGROUND = "#000000"
#make background gray
ctk.set_appearance_mode("dark")
#------------------ Variable Initializations ------------

#------------------ File Management ---------------------
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
    dataFiles = [f for f in os.listdir(dataPath) if os.path.isfile(os.path.join(dataPath, f))]
    if '.DS_Store' in dataFiles:
        dataFiles.remove('.DS_Store')
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
    modelFiles = [f for f in os.listdir(modelPath) if os.path.isfile(os.path.join(modelPath, f))]
    if '.DS_Store' in modelFiles:
        modelFiles.remove('.DS_Store')
    if len(modelFiles)==0:
        modelFiles = ["No Current Files"]
#if not then create and give the string no files currently
else:
    os.mkdir(dataPath)
    modelFiles = ["No Current Files"]

#if it does then take list of files in there
if "MasterModelFile.csv" in modelFiles:
    masterFilePath = os.path.abspath("../CogniSync/models/MasterModelFile.csv")
#if not then create and give the string no files currently
else:
    csvDict = {'Model Name':['Example'], 'Accuracy':[0.0], 'F1 Score':[0.0], 'Precision':[0.0], 'Recall':[0.0], 
            'Label 1':[('example', 0)], 'Label 2':[('example', 0)], 'Label 3':[('example', 0)], 'Label 4':[('example', 0)],
            'Label 5':[('example', 0)]}
    empty = pd.DataFrame(csvDict)
    masterFilePath = modelPath+"/MasterModelFile.csv"
    empty.to_csv(masterFilePath, index=False)
#------------------ File Management ---------------------

#------------------ Main Application --------------------
class App(ctk.CTk):
    """
    This class is the main application class that will be used to run the entire application.
    """
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs):
        """
        This function initializes the main application class and creates the container for the different pages.
        """ 
        # __init__ function for class Tk
        ctk.CTk.__init__(self, *args, **kwargs)
        #creating a container
        container = ctk.CTkFrame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        #initializing frames to an empty array
        self.frames = {}  
        #iterating through a tuple consisting of the different page classes
        for F in (Home, PlotEEG, UserRecording, Modeling, SnakeGame, USBOutput):
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(Home)
    #to display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
#------------------ Main Application --------------------


#------------------ Home Page ---------------------------
class Home(ctk.CTkFrame):
    """
    This class is the home page class that will be used to display the home page of the application.
    """
    def __init__(self, parent, controller): 
        """
        This function initializes the home page class and creates the home page.
        """
        ctk.CTkFrame.__init__(self, parent)
        #Adding our logo to the home page
        my_image = ctk.CTkImage(light_image=PIL.Image.open("resources/CogniSyncLogo.png"),
                                  dark_image=PIL.Image.open("resources/CogniSyncLogo.png"),
                                  size=(450, 450))
        my_label = ctk.CTkLabel(self, text = '', image=my_image)
        my_label.grid(row=1, column=2, padx=0, pady=0)
        #button to plot the EEG data
        button1 = ctk.CTkButton(self, text ="Plot EEG Data",corner_radius=25, 
        command = lambda : controller.show_frame(PlotEEG))
        button1.grid(row = 2, column = 1, padx = 10, pady = 10)
        #button to record the user data with prompting
        button2 = ctk.CTkButton(self, text ="Recording Data",corner_radius=25,
        command = lambda : controller.show_frame(UserRecording))
        button2.grid(row = 2, column = 2, padx = 10, pady = 20)
        #button to go to the modeling page
        button3 = ctk.CTkButton(self, text ="Modeling",corner_radius=25,
        command = lambda : controller.show_frame(Modeling))
        button3.grid(row = 2, column = 3, padx = 10, pady = 20)
        #button to go to the snake game
        button4 = ctk.CTkButton(self, text = "Snake Game", corner_radius=25, 
        command = lambda : controller.show_frame(SnakeGame))
        button4.grid(row=3, column=1, padx=10, pady=20)
        #button to go to the USB output page
        button5 = ctk.CTkButton(self, text = "USB Output", corner_radius=25,
        command = lambda : controller.show_frame(USBOutput))
        button5.grid(row=3, column=2, padx=10, pady=20)
#------------------ Home Page ---------------------------


#------------------ Plot EEG Data Page ------------------
class PlotEEG(ctk.CTkFrame):
    """
    This class is the plot EEG data page class that will be used to display the plot EEG data page of the application.
    """
    def __init__(self, parent, controller):
        """
        This function initializes the plot EEG data page class and creates the plot EEG data page.

        Parameters:
            parent: The parent class of the current class.
            controller: The controller class that controls the current class.

        Returns:
            None
        """
        ctk.CTkFrame.__init__(self, parent)
        #Label for the page
        label = ctk.CTkLabel(self, text ="Plotting EEG Data", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 100, pady = 10)
        #Button to go to the home page
        button1 = ctk.CTkButton(self, text ="Home",corner_radius=25,
                            command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 30)
        #Label for the data file dropdown menu
        Data_label = ctk.CTkLabel(self, text="Data File", font=("Verdana", 15))
        Data_label.grid(row=3, column=0, padx = 10, pady=10)
        #Dropdown menu for the data files
        self.Data_dropdown = ctk.CTkComboBox(self, values = dataFiles)
        self.Data_dropdown.grid(row=3, column = 1, padx=10, pady=10)
        #Button to update the data file list
        self.updateButton = ctk.CTkButton(self, text='Update File List', corner_radius=25, command=self.updateList)
        self.updateButton.grid(row=4, column=1, padx=10, pady=10)
        #Button to plot the EEG data
        button2 = ctk.CTkButton(self, text ="Show EEG Data",corner_radius=25, command=self.plot_eeg)
        button2.grid(row = 9, column = 1, padx = 10, pady = 30)
        #Slider for the starting point of the data
        self.slider1 = ctk.CTkSlider(self, from_=0, to=999990, command=self.slide1)
        self.slider1.grid(row=5, column=1, padx=10, pady=10)
        self.slideLabel1 = ctk.CTkLabel(self, text='Starting Point', font=("Verdana", 15))
        self.slideLabel1.grid(row=5, column=0, padx=10, pady=10)
        self.sliderLabel1 = ctk.CTkLabel(self, text=str(int(self.slider1.get())), font=("Verdana", 15))
        self.sliderLabel1.grid(row=5, column=2, padx=10, pady=10)
        #Slider for the ending point of the data
        self.slider2 = ctk.CTkSlider(self, from_=2, to=1000000, command=self.slide2)
        self.slider2.grid(row=6, column=1, padx=10, pady=10)
        self.slideLabel1 = ctk.CTkLabel(self, text='Ending Point', font=("Verdana", 15))
        self.slideLabel1.grid(row=6, column=0, padx=10, pady=10)
        self.sliderLabel2 = ctk.CTkLabel(self, text=str(int(self.slider2.get())), font=("Verdana", 15))
        self.sliderLabel2.grid(row=6, column=2, padx=10, pady=10)
        #checkbox to select electrode data for graph
        self.check1Var = ctk.IntVar(value=0)
        self.check1 = ctk.CTkCheckBox(self, text = "Electrode Readings", onvalue=1, offvalue=0, corner_radius=5, variable=self.check1Var, font=("Verdana", 15))
        self.check1.grid(row=7, column=1, padx=10, pady=10)
        #checkbox to select alpha values for graph
        self.check2Var = ctk.IntVar(value=0)
        self.check2 = ctk.CTkCheckBox(self, text = "Alpha Values", onvalue=1, offvalue=0, corner_radius=5, variable=self.check2Var, font=("Verdana", 15))
        self.check2.grid(row=7, column=0, padx=10, pady=10)
    
    '''Updates the file list for the dropdown menu'''
    def updateList(self):
        """
        Updates the data file list in the GUI dropdown menu.

        This method searches the given directory and checks if each item is a file.
        If it is a file, it is added to the data file list. The method also removes
        a folder that is typically hidden for Mac users. If no files exist, it sets
        the data file list to "No Current Files". Finally, it updates the data file
        list in the GUI dropdown menu.

        Args:
            None

        Returns:
            None
        """
        dataFiles = [f for f in os.listdir(dataPath) if os.path.isfile(os.path.join(dataPath, f))]
        if '.DS_Store' in dataFiles:
            dataFiles.remove('.DS_Store')
        if len(dataFiles) == 0:
            dataFiles = "No Current Files"
            self.Data_dropdown.configure(values=dataFiles)
        else:
            self.Data_dropdown.configure(values=dataFiles)

    '''Controls the slider values'''
    def slide1(self, value):
        """
        This method is used to handle the changes in the first slider's value.

        Parameters:
            value: The new value of the first slider.

        Returns:
            None
        """
        if value >= self.slider2.get():
            self.slider1.configure(to=self.slider2.get()-1)
        if self.slider1.cget('to')<self.slider2.get()-2:
            self.slider1.configure(to=self.slider2.get()-2)
        self.sliderLabel1.configure(text=str(int(self.slider1.get())))
        self.sliderLabel2.configure(text=str(int(self.slider2.get())))
    def slide2(self, value):
        """
        This method is used to handle the changes in the second slider's value.

        Parameters:
            value: The new value of the second slider.

        Returns:
            None
        """
        #This changes the slider value to be more than the lower interval slider value
        if value <= self.slider1.get():
            #The value is set to be one more than the first slider value 
            self.slider2.configure(from_=self.slider1.get()+1)
        #This changes the minimum of the slider value if it is greater than 2 more than the first slider value
        if self.slider2.cget('from_')>self.slider1.get()+2:
            self.slider2.configure(from_=self.slider1.get()+2)
        #This updates the labels for the values of both sliders
        self.sliderLabel2.configure(text=str(int(self.slider2.get())))
        self.sliderLabel1.configure(text=str(int(self.slider1.get())))
    
    '''Plots the requested value categories for the interval inputed'''
    def plot_eeg(self):
        """
        Plots the EEG data based on the selected file and plot options.

        Returns:
            None
        """
        #This retrieves the data file name requested
        dataSelected = self.Data_dropdown.get()
        #the path for the file is created
        dataPath = os.path.join(pathDir, "data/", dataSelected)
        #the file is converted to a pandas dataframe
        data = pd.read_csv(dataPath)
        #all the rows with a NA value are removed
        data.dropna(inplace=True)
        #this grabs all the unique labels from the file
        labelNames = data['label'].unique()
        #the labels are placed into their own dataframe and removed from the original
        labels = data['label']
        data.drop(columns='label', inplace=True)
        temp_save = ''
        columnNames = []
        legend = {}
        #colors are assigned to the columns of the data
        k=0
        for col in data.columns:
            columnNames.append(col)
            legend[col] = px.colors.qualitative.Alphabet[k]
            k+=1
        k=0
        #a standard interval for plotting the data is created
        #if the slider values differ from the default ones the slider values are used
        interval_default = [0, len(data)]
        fig = go.Figure()
        if self.slider1.get()>interval_default[0]:
            interval1 = int(self.slider1.get())
        else:
            interval1 = interval_default[0]
        if self.slider2.get()<interval_default[1]:
            interval2 = int(self.slider2.get())
        else:
            interval2 = interval_default[1]
        data = data[interval1:interval2]
        #the min and max of the data are taken to create vertical lines in the data set
        min = data[['ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','aux1','aux2','aux3']].values.min()
        max = data[['ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','aux1','aux2','aux3']].values.max()
        legend2={}
        #colors are assigned to the unique labels from the data set
        k=0
        for j in labelNames:
            legend2[j]=px.colors.qualitative.Light24[k]
            k+=1
        #this creates the line plots if only the electrode values are requested
        if self.check1Var.get()==1 and self.check2Var.get()==0:
            data = data.drop(columns=data.columns[8:11])
            fig.add_trace(go.Scatter(x=data.index, y=data['ch1'], mode='lines', line=dict(color=legend.get('ch1')), name='ch1'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch2'], mode='lines', line=dict(color=legend.get('ch2')), name='ch2'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch3'], mode='lines', line=dict(color=legend.get('ch3')), name='ch3'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch4'], mode='lines', line=dict(color=legend.get('ch4')), name='ch4'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch5'], mode='lines', line=dict(color=legend.get('ch5')), name='ch5'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch6'], mode='lines', line=dict(color=legend.get('ch6')), name='ch6'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch7'], mode='lines', line=dict(color=legend.get('ch7')), name='ch7'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch8'], mode='lines', line=dict(color=legend.get('ch8')), name='ch8'))
            #this adds a line for each movement only once so that the label names are present in the legend with the associated color
            previous=[]
            for i in range(interval1, interval2):
                #this checks that the movement is not norm or already added and plots the line
                if labels.iloc[i] != 'norm' and labels.iloc[i] != temp_save and not(labels.iloc[i] in previous):
                    temp_save = labels.iloc[i]
                    #this adds the label to a list that is used to check if the label was already used
                    previous.append(labels.iloc[i])
                    fig.add_trace(go.Scatter(x=[labels.iloc[i], labels.iloc[i]], y=[min, max], mode='lines', 
                                  line=dict(color=legend2[labels.iloc[i]], dash='dash'), name=labels.iloc[i]))
            #the graph is given a title from the data file name and what was selected to plot
            graphTitle = dataSelected[:-4]+" Electrode Values"
        #this plots the alpha values from the data file
        elif self.check1Var.get()==0 and self.check2Var.get()==1:
            data = data.drop(columns=data.columns[0:8])
            #the min and max are retaken so that it will not increase the y axis too much compared to the alpha values
            min = data[['aux1','aux2','aux3']].values.min()
            max = data[['aux1','aux2','aux3']].values.max()
            #all rows with an alpha value of zero are removed to remove times when the alpha was not calculated
            data.drop(data[data.aux1==0.0].index, inplace=True)
            data.drop(data[data.aux2==0.0].index, inplace=True)
            data.drop(data[data.aux3==0.0].index, inplace=True)
            #the alpha values are plotted with the colors given to them
            fig.add_trace(go.Scatter(x=data.index, y=data['aux1'], mode='lines', line=dict(color=legend.get('aux1')), name='aux1'))
            fig.add_trace(go.Scatter(x=data.index, y=data['aux2'], mode='lines', line=dict(color=legend.get('aux2')), name='aux2'))
            fig.add_trace(go.Scatter(x=data.index, y=data['aux3'], mode='lines', line=dict(color=legend.get('aux3')), name='aux3'))
            previous=[]
            for i in range(interval1, interval2):
                #this checks that the movement is not norm or already added and plots the line
                if labels.iloc[i] != 'norm' and labels.iloc[i] != temp_save and not(labels.iloc[i] in previous):
                    temp_save = labels.iloc[i]
                    #this adds the label to a list that is used to check if the label was already used
                    previous.append(labels.iloc[i])
                    fig.add_trace(go.Scatter(x=[labels.iloc[i], labels.iloc[i]], y=[min, max], mode='lines', 
                                  line=dict(color=legend2[labels.iloc[i]], dash='dash'), name=labels.iloc[i]))
            #the graph is given a title from the data file name and what was selected to plot
            graphTitle = dataSelected[:-4]+" Alpha Values"
        #all values are plotted when both or neither checkbox is checked
        else:
            #the graph is given a title from the data file name and what was selected to plot
            graphTitle = dataSelected[:-4]+" Electrode and Alpha Values"
            fig.add_trace(go.Scatter(x=data.index, y=data['ch1'], mode='lines', line=dict(color=legend.get('ch1')), name='ch1'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch2'], mode='lines', line=dict(color=legend.get('ch2')), name='ch2'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch3'], mode='lines', line=dict(color=legend.get('ch3')), name='ch3'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch4'], mode='lines', line=dict(color=legend.get('ch4')), name='ch4'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch5'], mode='lines', line=dict(color=legend.get('ch5')), name='ch5'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch6'], mode='lines', line=dict(color=legend.get('ch6')), name='ch6'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch7'], mode='lines', line=dict(color=legend.get('ch7')), name='ch7'))
            fig.add_trace(go.Scatter(x=data.index, y=data['ch8'], mode='lines', line=dict(color=legend.get('ch8')), name='ch8'))
            fig.add_trace(go.Scatter(x=data.index, y=data['aux1'], mode='lines', line=dict(color=legend.get('aux1')), name='aux1'))
            fig.add_trace(go.Scatter(x=data.index, y=data['aux2'], mode='lines', line=dict(color=legend.get('aux2')), name='aux2'))
            fig.add_trace(go.Scatter(x=data.index, y=data['aux3'], mode='lines', line=dict(color=legend.get('aux3')), name='aux3'))
            previous=[]
            for i in range(interval1, interval2):
                #this checks that the movement is not norm or already added and plots the line
                if labels.iloc[i] != 'norm' and labels.iloc[i] != temp_save and not(labels.iloc[i] in previous):
                    temp_save = labels.iloc[i]
                    #this adds the label to a list that is used to check if the label was already used
                    previous.append(labels.iloc[i])
                    fig.add_trace(go.Scatter(x=[labels.iloc[i], labels.iloc[i]], y=[min, max], mode='lines', 
                                  line=dict(color=legend2[labels.iloc[i]], dash='dash'), name=labels.iloc[i]))
        data.reset_index(inplace=True)
        #the legend is given a title and updated to be shown on the graph
        fig.update_layout(legend_title_text='Legend')
        fig.update_layout(showlegend=True)
        fig.update_layout(font_size=35)
        fig.update_layout(title_text=graphTitle)
        #the rest of the labels are plotted without adding to the legend
        for i in range(interval1, interval2):
            #if a label is not norm and is not the same as the previously plotted movement then it is added
            if labels.iloc[i] != 'norm' and labels.iloc[i] != temp_save:
                temp_save = labels.iloc[i]
                #a dashed vertical line is added to the graph with this function to not add it to the legend
                fig.add_vline(x=i, line_dash='dash', line_color=legend2[labels.iloc[i]])
        #the plot is shown in the browser of the user
        fig.show()
#------------------ Plot EEG Data Page ------------------


#------------------ User Recording Page -----------------
class UserRecording(ctk.CTkFrame): 
    """
    This class is the user recording page class that will be used to display the user recording page of the application.
    """
    def __init__(self, parent, controller):
        """
        This function initializes the user recording page class and creates the user recording page.

        Parameters:
            parent: The parent class of the current class.
            controller: The controller class that controls the current class.

        Returns:
            None
        """
        ctk.CTkFrame.__init__(self, parent)
        #Page name label
        self.label = ctk.CTkLabel(self, text ="Recording Data", font = LARGEFONT)
        self.label.grid(row = 0, column = 1, padx = 100, pady = 10)
        #Text label for prompting instructions
        self.instructions_label = ctk.CTkLabel(self, text="Follow the movement instructions below:")
        self.instructions_label.grid(row = 1, column = 1)
        #creates canvas for movement prompting
        self.canvas = ctk.CTkCanvas(self, width=400, height=400)
        self.canvas.grid(row = 2, column = 1, padx = 100, pady = 10)
        #set the prompting time frames
        self.prepare_time = 5
        self.hold_time = 10
        self.rest_time = 10
        #init empty movement list
        self.movements = []
        #set some default movements
        self.default_movements = ["arms","legs","jaw","eyes"]
        self.n_movements = []
        #shuffle movements
        self.shuffle_movements()
        #sets some values for future use
        self.current_movement_index = 0
        self.current_movement = None
        self.prompt_count = 0
        self.movement_activated = 0
        #Label for the input movement entry box
        txt_label = ctk.CTkLabel(self, text="Movement Input")
        txt_label.grid(row=6, column=0, padx = 10, pady = 5)
        #textbox for entry of movements separated by commas EX. jaw,leg,arm
        txt_entry = ctk.CTkEntry(self, height=10, placeholder_text="ENTER MOVEMENTS SEPERATED BY COMMA",  width = 300)
        txt_entry.grid(row= 6, column =1, padx = 10, pady = 5)
        self.text_entry = txt_entry
        #Label for the movement count input
        mvmt_count_label = ctk.CTkLabel(self, text="Number of movements")
        mvmt_count_label.grid(row=7, column=0, padx = 10, pady = 5)
        #Textbox for the entry of an int representing the number of movements for prompting
        mvmt_count = ctk.CTkEntry(self, height=10, placeholder_text="ENTER NUMBER OF MOVEMENTS AS INTEGER",  width = 300)
        mvmt_count.grid(row= 7, column =1, padx = 10, pady = 5)
        self.mvmt_count = mvmt_count
        #Label for number of iterations text box
        iter_count_label = ctk.CTkLabel(self, text="Number of Iterations")
        iter_count_label.grid(row=9, column=0, padx = 10, pady = 5)
        #text box for user to enter the number of iterations
        iter_count = ctk.CTkEntry(self, height=10, placeholder_text="NUMBER OF ITERATIONS PER MOVE",  width = 300)
        iter_count.grid(row= 9, column =1, padx = 10, pady = 5)
        #variable to hold iterations
        self.iter_count = iter_count
        #key releases that call the update_movements function when input is provided to the text boxes
        self.iter_count.bind("<KeyRelease>", self.update_movements)
        self.mvmt_count.bind("<KeyRelease>", self.update_movements)
        self.text_entry.bind("<KeyRelease>", self.update_movements)
        # 4 movements, 40 times each
        self.total_prompts = 4 * 40
        #label for the output file textbox
        output_label = ctk.CTkLabel(self, text="Output file")
        output_label.grid(row=8, column=0, padx = 10, pady = 5)
        #Creating our textbox so user can input file name
        out_entry = ctk.CTkEntry(self, height=10, placeholder_text="FILE_NAME.csv",  width = 300)
        out_entry.grid(row= 8, column =1, padx = 10, pady = 5)
        #variable to hold output
        self.file_out = out_entry
        #Button to start prompting
        self.start_button = ctk.CTkButton(self, text="Start Collecting", corner_radius=10, command=self.start_prompting)
        self.start_button.grid(row=4, column = 1, padx = 10, pady=5)
        #button to go to home page
        self.home_button = ctk.CTkButton(self, text ="Home",corner_radius=10,
                            command = lambda : controller.show_frame(Home))
        self.home_button.grid(row = 1, column = 0, padx = 10, pady = 5)
        #Stop data collection
        self.stop_button = ctk.CTkButton(self, text="Stop Collecting", corner_radius=10, command=self.stop_prompting)
        self.stop_button.grid(row=5, column=1, padx=10, pady=5)
        self.is_prompting = False  # Flag to check if prompting is in progress
        self.step_start_time = 0

        '''Variables for threading'''
        self.record_thread = None

    '''Function used to update the user movements if they have been entered into a textbox'''
    def update_movements(self, event):
        """
        Update the movements based on the text entered by the user.

        Parameters:
            event: The event that triggered the update.

        Returns:
            None
        """
        self.movement_activated = 1
        # Get the text entered by the user
        movements_text = self.text_entry.get()
        # if the movement box is full of whitespace set to default movement
        if not movements_text.strip():
            self.movements = self.default_movements
        # split the entered movements by ,
        else:
            self.movements = movements_text.split(",")


    '''Function that begins the prompting process and intis some prompting parameters'''
    def start_prompting(self):
        """
        Starts the prompting process.

        This method disables the start button, enables the stop button, sets the `is_prompting` flag to True,
        calls the `prompt_next_movement` function, starts the recording session, sets the `total_prompts` variable
        based on the specified movement iterations and counts, and allows the stream to start before prompting.

        Note: The `total_prompts` variable is set to a default value of 4*40 if neither movement iterations nor counts
        are specified.

        Args:
            None

        Returns:
            None
        """
        #disable the start button
        self.start_button.configure(state=ctk.DISABLED)
        #enable the stop button
        self.stop_button.configure(state=ctk.NORMAL)
        #set prompting to true
        self.is_prompting = True
        #call prompt next movement function
        self.prompt_next_movement()
        #start the recording session
        self.start_record()
        #set total prompts to movements * iterations
        self.total_prompts = int(self.iter_count.get()) * int(self.mvmt_count.get())
        #if user has specified neither movement iterations or counts set to a default 4*40
        if not self.total_prompts:
            self.total_prompts = 4*40
        #Allow stream to start before prompting
        time.sleep(15)


    '''Function used to stop the prompting processes when the stop button is called used to reset the frame and wipe it of information'''
    def stop_prompting(self):
        """
        Stops the prompting process.

        This method sets the `is_prompting` flag to False, disables the start button, enables the stop button, throws a
        "Training canceled!" message, resets the movement index, reshuffles the movements, resets the prompting time frames,
        wipes the canvas if it is populated, and stops the recording session.

        Args:
            None

        Returns:
            None
        """
        #set is prompting to false
        self.is_prompting = False
        #enable start button use
        self.start_button.configure(state=ctk.NORMAL)
        #disable stop button use
        self.stop_button.configure(state=ctk.DISABLED)
        #throw message "training canceled"
        self.instructions_label.configure(text="Training canceled!")
        #reset movement index
        self.current_movement_index = 0
        #reshuffle movements
        self.shuffle_movements()
        #reset prompting time frames
        self.prepare_time = 5
        self.hold_time = 10
        self.rest_time = 10
        #if the canvas is populated then wipe it
        if self.canvas.find_all():
            self.instructions_label.configure(text="Training canceled!")
            self.canvas.delete("all")
        #stop the recording  
        self.stop_record()

    '''This function is called when the prompting has reached its conclusion.
        It resets the frame and ends the data stream and sends the recorded data to an output file.'''
    def end_prompting(self):
        """
        Ends the prompting process.

        This method sets the `is_prompting` flag to False, enables the start button, disables the stop button, throws a
        "Training completed!" message, gets the user file name input, sets the file name to "YOUR_DATA.csv" if the user
        input is empty or whitespace, opens the output file and copies the recorded results, resets the movement index and
        reshuffles the movements, resets the prompting time frames, and wipes the canvas if it is populated.

        Args:
            None

        Returns:
            None
        """
        #set prompting to false
        self.is_prompting = False
        #Enables start button
        self.start_button.configure(state=ctk.NORMAL)
        #Disables stop button
        self.stop_button.configure(state=ctk.DISABLED)
        #Throws "training completed" message
        self.instructions_label.configure(text="training completed!")
        #Gets the user File name input
        my_outputFile = self.file_out.get()
        #if the users input was empty or whitespace default name to "YOUR_DATA.csv"
        if not my_outputFile:
            my_outputFile = "YOUR_DATA.csv"
        elif not my_outputFile.strip():
            my_outputFile = "YOUR_DATA.csv"
        #open output file and copy in recorded results
        self.f = open(my_outputFile, "x")
        shutil.copyfile("newest_rename.csv", my_outputFile)
        #reset movement idx and reshuffle movements
        self.current_movement_index = 0
        self.shuffle_movements()
        #reset prompting time frames
        self.prepare_time = 5
        self.hold_time = 10
        self.rest_time = 10
        #if the canvas is populated then wipe it
        if self.canvas.find_all():
            self.instructions_label.configure(text="Training is completed!")
            self.canvas.delete("all")
            open('tempVal.txt', 'w').close()

    '''function used to shuffle movements'''
    def shuffle_movements(self):
        """
        This method shuffles the movements list.

        Args:
            None

        Returns:
            None
        """
        random.shuffle(self.movements)

    '''Function used to prompt the next movement in the list of movements'''
    def prompt_next_movement(self):
        """
        Prompts the next movement in the list of movements.

        This method checks if the `prompt_count` is less than the `total_prompts` and the `is_prompting` flag is True.
        If both conditions are met, the method throws a "Prepare for the next movement..." message, deletes the movement
        in the canvas, and calls the `show_movement_instruction` function after 5 seconds. If the conditions are not met,
        the method calls the `end_prompting` function.

        Args:
            None

        Returns:
            None
        """
        #if the prompt_count is less than the total amount of prompts and is prompting is true
        if self.prompt_count < self.total_prompts and self.is_prompting:
            #throw text "prepare for next movement"
            self.instructions_label.configure(text="Prepare for the next movement...")
            #delete the movement in the canvas
            self.canvas.delete("all")
            #after 5 seconds show the next movement using the show_movement_instruction function
            self.canvas.after(1000 * self.prepare_time, self.show_movement_instruction)
        #else, end prompting
        else:
            self.end_prompting()
            open('tempVal.txt', 'w').close()

    '''Function used to show the instructions for the next movement'''
    def show_movement_instruction(self):
        """
        Shows the instructions for the next movement.

        This method checks if the `is_prompting` flag is True. If the condition is met, the method throws a "Hold the
        movement for {specified time} seconds" message, sets the `current_movement` to the movement at the current
        movement index, calls the `start_writing_to_file` function after 2 seconds, calls the `stop_writing_to_file`
        function after 6 seconds, shows the current movement in the prompting canvas, and calls the `show_rest_period`
        function after the specified hold movement time (10 seconds). If the condition is not met, the method closes the
        "tempVal.txt" file and deletes the canvas.

        Args:
            None

        Returns:
            None
        """
        #if is prompting is true throw text "Hold the movement for {specified time} seconds"
        if self.is_prompting:
            self.instructions_label.configure(text="Hold the movement for {} seconds".format(self.hold_time))
            #if the user did not input movements into the entry box set to default movements
            if self.movement_activated == 0:
                self.movements = self.default_movements
            #the current movement is set to the idx of the current movement idx
            self.current_movement = self.movements[self.current_movement_index]
            #after 2 seconds being writing labels to the temp val file to append to data
            self.after(2000, self.start_writing_to_file)
            #after 6 secconds stop writing the data to the temp val
            self.after(6000, self.stop_writing_to_file)
            #Show the current movement in the prompting canvas
            self.canvas.create_text(100, 100, text=self.current_movement, font=("Helvetica", 30))
            #after the specified hold movement time (10 seconds) show the rest period
            self.canvas.after(1000 * self.hold_time, self.show_rest_period)
        #if we aren't prompting close temp val and close canvas
        else:
            open('tempVal.txt', 'w').close()
            self.instructions_label.configure(text="Training canceled!")
            self.canvas.delete("all")

    '''Function used to start writing to the tempVal file, used to append labels to data'''
    def start_writing_to_file(self):
        """
        Starts writing the current movement to the "tempVal.txt" file.

        This method opens the "tempVal.txt" file and writes the current movement to the file.

        Args:
            None

        Returns:
            None
        """
        # close the file if open then reopen and write the current movement
        open('tempVal.txt', 'w').close()
        f = open("tempVal.txt", "a")
        f.write(self.current_movement)
        f.close()
    
    '''Function used to ensure that the tempVal file is closed'''
    def stop_writing_to_file(self):
        """
        Stops writing to the "tempVal.txt" file.

        This method closes the "tempVal.txt" file.

        Args:
            None

        Returns:
            None
        """
        # Close the file when the middle 7 seconds end
        open('tempVal.txt', 'a').close()  # Make sure the file is closed

    '''Function used to show the rest period in between movements'''
    def show_rest_period(self):
        """
        Shows the rest period in between movements.

        This method checks if the `is_prompting` flag is True. If the condition is met, the method throws a "Rest for
        {specified time} seconds" message, deletes the movement in the canvas, ensures the "tempVal.txt" file is closed,
        increments the `prompt_count` by 1, increments the `current_movement_index` by 1 (wrapping around to the beginning
        if the end of the list is reached), shuffles the movements if the current movement index is 0, and calls the
        `prompt_next_movement` function after 5 seconds.

        Args:
            None

        Returns:
            None
        """
        #if is prompting is true
        if self.is_prompting:
            #give message "Rest for {10} seconds"
            self.instructions_label.configure(text="Rest for {} seconds".format(self.rest_time))
            #delete the movement in the canvas
            self.canvas.delete("all")
            #ensure tempVal file is closed
            open('tempVal.txt', 'w').close()
            #increment the prompt count
            self.prompt_count += 1
            #moves the current movement index by one and wraps around to the beginning if the end of list is reached
            self.current_movement_index = (self.current_movement_index + 1) % len(self.movements)
            #if current movement idx is zero shuffle the movements
            if self.current_movement_index == 0:
                self.shuffle_movements()
            #after 5 seconds prompt the next movement using the prompt next movement function
            self.canvas.after(1000 * self.rest_time, self.prompt_next_movement)
    
    '''Thread for recording EEG data'''
    def start_record(self):
        """
        Starts the recording of EEG data.

        This method starts the recording of EEG data by creating a new thread and calling the `record_data` function.

        Args:
            None

        Returns:
            None
        """
        if self.record_thread is None or not self.record_thread.is_alive():
            self.record_thread = threading.Thread(target=self.record_data)
            self.record_thread.start()
    def stop_record(self):
        """
        Stops the recording of EEG data.

        This method stops the recording of EEG data by joining the record thread if it is alive.

        Args:
            None

        Returns:
            None
        """
        if self.record_thread is not None and self.record_thread.is_alive():
            self.record_thread.join()
    def record_data(self):
        """
        Records the EEG data.

        This method records the EEG data by calling the `record` function from the connect.py.

        Args:
            None

        Returns:
            None
        """
        record(self)
#------------------ User Recording Page -----------------


#------------------ Modeling Page -----------------------
class Modeling(ctk.CTkFrame):
    """
    This class is the modeling page class that will be used to display the modeling page of the application.
    """
    def __init__(self, parent, controller):
        """
        This function initializes the modeling page class and creates the modeling page.

        Parameters:
            parent: The parent class of the current class.
            controller: The controller class that controls the current class.

        Returns:
            None
        """
        ctk.CTkFrame.__init__(self, parent)
        #label for the page
        label = ctk.CTkLabel(self, text ="User Modeling", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 50, pady = 10)
        #Home button
        button1 = ctk.CTkButton(self, text ="Home",corner_radius=25, 
                            command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 30)
        #label for model dropdown
        modelLabel = ctk.CTkLabel(self, text="Model")
        modelLabel.grid(row=2, column=0, padx=10, pady=10)
        #dropdown option for the model label with options for models to run, function will run corresponding model
        self.model_dropdown = ctk.CTkOptionMenu(self, values = ["LDA", "SVC", "Random Forest Classifier", "Tensorflow", "Decision Tree Classifier", 
                                                              "Logistic Regression", "QDA", "Gradient Boosting Classifier", "KNN", 
                                                              "Gaussian NB", "MLP Classifier", "PyTorch"])
        self.model_dropdown.grid(row=2, column = 1, padx=10, pady=10)
        #labels for the data dropdown
        Data_label = ctk.CTkLabel(self, text="Data File")
        Data_label.grid(row=3, column=0, padx = 10, pady=10)
        #dropdown option for the data that we will run into the model. select from csvs, will be populated from directory 
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
        #Creating the file name label
        txt_label = ctk.CTkLabel(self, text="Output File Name")
        txt_label.grid(row=5, column=0, padx = 10, pady = 10)
        #Creating our textbox so user can input file name
        txt_entry = ctk.CTkEntry(self, height=10, placeholder_text="output.pkl")
        txt_entry.grid(row= 5, column =1, padx = 10, pady = 10)
        self.text = txt_entry
        #checkbox to select electrode data
        self.check1Var = ctk.IntVar(value=1)
        self.check1 = ctk.CTkCheckBox(self, text = "Electrode Readings", onvalue=1, offvalue=0, corner_radius=5, variable=self.check1Var)
        self.check1.grid(row=6, column=1, padx=20, pady=10)
        #checkbox to select alpha values
        self.check2Var = ctk.IntVar(value=1)
        self.check2 = ctk.CTkCheckBox(self, text = "Alpha Values", onvalue=1, offvalue=0, corner_radius=5, variable=self.check2Var)
        self.check2.grid(row=6, column=0, padx=10, pady=10)
        #update the datafile list
        update_button = ctk.CTkButton(self, text="Update File Lists", command = self.updateFiles)
        update_button.grid(row=7, column=0, columnspan=2, sticky="news", padx=10, pady=10)
        #will create the model with the selections by the user
        run_button = ctk.CTkButton(self, text="Run", command=self.model_input)
        run_button.grid(row=8, column=0, columnspan = 2, sticky = "news", padx=10, pady=10)

    '''creates the model from the data file selected by the user'''
    def model_input(self):
        """
        Creates the model from the data file selected by the user.

        This method gets the model, data, labels, and output file name selected by the user, and calls the corresponding
        function to create the model. Then saves the model results to a file and outputs the results to the GUI.

        Args:
            None

        Returns:
            None
        """
        #values the user inputed are placed in variables
        modelSelected = self.model_dropdown.get()
        dataSelected = self.Data_dropdown.get()
        labelsSelected = self.Labels_dropdown.get()
        outputFile = self.text.get()
        print(modelSelected)
        print(dataSelected)
        print(labelsSelected)
        print(outputFile)
        self.relPath = "../CogniSync/data/"
        #all these send the data files selected to csv processing and then send the files to model_bci 
        #these are separated by which type of model is being created
        if modelSelected == "LDA":
            phrase = ctk.CTkLabel(self, text="Time is a circle. You're your own grandpa.", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray, legend = self.csvProcessing(dataSelected, labelsSelected)
            results = BCI_sklearn_LinearDiscriminantAnalysis(dataArray, labelsArray)
        elif modelSelected == "Gradient Boosting Classifier":
            phrase = ctk.CTkLabel(self, text="Booster rockets deployed", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray, legend = self.csvProcessing(dataSelected, labelsSelected)
            print('going into modeling')
            results = BCI_sklearn_GradientBoostingClassifier(dataArray, labelsArray)
        elif modelSelected == "KNN":
            phrase = ctk.CTkLabel(self, text="Apartment complex", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray, legend = self.csvProcessing(dataSelected, labelsSelected)
            print('going into modeling')
            results = BCI_sklearn_KNeighborsClassifier(dataArray, labelsArray)
        elif modelSelected == "Gaussian NB":
            phrase = ctk.CTkLabel(self, text="Math GOAT", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray, legend = self.csvProcessing(dataSelected, labelsSelected)
            print('going into modeling')
            results = BCI_sklearn_GaussianNB(dataArray, labelsArray)
        elif modelSelected == "MLP Classifier":
            phrase = ctk.CTkLabel(self, text="Let's go dodgers, Let's go", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray, legend = self.csvProcessing(dataSelected, labelsSelected)
            print('going into modeling')
            results = BCI_sklearn_MLPClassifier(dataArray, labelsArray)
        elif modelSelected == "SVC":
            phrase = ctk.CTkLabel(self, text="Get Vectored! *air horn noise*", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray, legend = self.csvProcessing(dataSelected, labelsSelected)
            print('going into modeling')
            results = BCI_sklearn_SVC(dataArray, labelsArray)
        elif modelSelected == "Tensorflow":
            phrase = ctk.CTkLabel(self, text="Tensions between people flow to others.", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray, legend = self.csvProcessing(dataSelected, labelsSelected)
           # results = BCI_tensorflow_Net(dataArray, labelsArray)
        elif modelSelected == "Random Forest Classifier":
            phrase = ctk.CTkLabel(self, text="Trees are the breath of life", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray, legend = self.csvProcessing(dataSelected, labelsSelected)
            results = BCI_sklearn_RandomForestClassifier(dataArray, labelsArray)
        elif modelSelected == "Decision Tree Classifier":
            phrase = ctk.CTkLabel(self, text="Decisions and Trees", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray, legend = self.csvProcessing(dataSelected, labelsSelected)
            results = BCI_sklearn_DecisionTreeClassifier(dataArray, labelsArray)
        elif modelSelected == "Logistic Regression":
            phrase = ctk.CTkLabel(self, text="Logging onto the mainframe", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray, legend = self.csvProcessing(dataSelected, labelsSelected)
            results = BCI_sklearn_LogisticRegression(dataArray, labelsArray)
        elif modelSelected == "QDA":
            phrase = ctk.CTkLabel(self, text="Quads for the win", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray, legend = self.csvProcessing(dataSelected, labelsSelected)
            results = BCI_sklearn_QuadraticDiscriminantAnalysis(dataArray, labelsArray)
        elif modelSelected == "PyTorch":
            phrase = ctk.CTkLabel(self, text="Torching the competition", font=("Verdana", 18))
            phrase.grid(row=2, column=3, padx=10, pady=10)
            waitLabel = ctk.CTkLabel(self, text="Modeling data right now. Please be patient.", font=("Verdana", 18))
            waitLabel.grid(row=3, column=3, padx=10, pady=10)
            dataArray, labelsArray, legend = self.csvProcessing(dataSelected, labelsSelected)
            results, model = BCI_pytorch_Net(dataArray, labelsArray)
        #time is taken to create a unique id for the model
        t = time.time()
        #tensorflow results are saved in a text file
        if modelSelected == "Tensorflow":
            waitLabel.configure(text="Results")
            #the accuracy and nodes used are printed to the gui
            metrics = ctk.CTkLabel(self, text="Accuracy: {:.3f}".format(results[0]), font=("Verdana", 18))
            metrics.grid(row=4, column=3, padx=10, pady=10)
            nodes = ctk.CTkLabel(self, text=results[1], font=("Verdana", 18))
            nodes.grid(row=5, column=3, padx=10, pady=10)
            #if no output file name is given one is created
            if outputFile == "" or outputFile == " ":
                dataName = dataSelected[:-4]
                outputFile = modelSelected+dataName+str(t)+"Output.txt"
                #output file has the model name, score, and nodes written into it
                f = open(self.relPath+outputFile, "a")
                f.write("Model Name: "+modelSelected+'_'+dataName+'_'+str(t)+"\n")
                f.write("Score: "+str(results[0])+"\n")
                f.write("Parameters: "+str(results[1])+"\n")
                f.close()
                print("File Name: "+outputFile)
            #the results and nodes are written to the file name given by the user
            else:
                f = open(self.relPath+outputFile, "a")
                f.write("Model Name: "+modelSelected+'_'+dataName+'_'+str(t)+"\n")
                f.write("Score: "+str(results[0])+"\n")
                f.write("Parameters: "+str(results[1])+"\n")
                f.close()
        #pytorch models are saved as a .pt file
        elif modelSelected == "PyTorch":
            #metrics for the model are written to the gui
            waitLabel.configure(text="Results")
            metrics = ctk.CTkLabel(self, text="Accuracy: {:.3f} F1 Score: {:.3f} Precision: {:.3f} Recall: {:.3f}".format(
                results[0], results[1], results[2], results[3]), font=("Verdana", 18))
            metrics.grid(row=4, column=3, padx=10, pady=10)
            dataName = dataSelected[:-4]
            #if no file name is given one is made
            #a .pt file of the fitted model is saved to the models folder
            if outputFile == "" or outputFile == " ":
                torch.save(model, modelPath+'/'+modelSelected+'_'+dataName+'_'+str(t)+".pt")
            else:
                torch.save(model, modelPath+'/'+outputFile)
        #all sklearn models are saved as .pkl files
        else:
            #metrics for the modle are written to the gui
            waitLabel.configure(text="Results")
            metrics = ctk.CTkLabel(self, text="Accuracy: {:.3f} F1 Score: {:.3f} Precision: {:.3f} Recall: {:.3f}".format(
                results[0], results[1], results[2], results[3]), font=("Verdana", 18))
            metrics.grid(row=4, column=3, padx=10, pady=10)
            #if no file name is given one is made
            #a .pkl file of the fitted model is saved to the models folder
            if outputFile == "" or outputFile == " ":
                dataName = dataSelected[:-4]
                outputFile = modelSelected+'_'+dataName+'_'+str(t)+".pkl"
                joblib.dump(results[4], modelPath+"/"+outputFile)
                print("File Name: "+outputFile)
            else:
                joblib.dump(results[4], modelPath+"/"+outputFile)
        #the csv containing all model names is read in
        df=pd.read_csv(masterFilePath)
        modelID = modelSelected+'_'+dataName+'_'+str(t)
        #if five movements are recorded in the file the model name, results, 
        #and label names are written into the model name csv
        if len(legend)==5:
            keyList = list(legend.keys())
            valList = list(legend.values())
            items = []
            #makes the legend indexable to allow generalized addition of the label names
            i=0
            for i in range(len(legend)):
                #the index of label names are found using the value list and added to items
                items.append(keyList[valList.index(str(i))])
                i+=1
            df.loc[len(df.index)] = [modelID, results[0], results[1], results[2], results[3], items[0], items[1], items[2], items[3], items[4]]
            df.to_csv(masterFilePath, index=False)

    '''Updates the file list for the dropdown menus'''
    def updateFiles(self):
        """
        Updates the file list for the dropdown menus.

        This method updates the file list for the dropdown menus by getting the files in the data path and updating the
        dropdown menus with the files.

        Args:
            None

        Returns:
            None
        """
        #this searches the given directory and checks if it is a file
        #if it is a file then it is added to the data file list
        dataFiles = [f for f in os.listdir(dataPath) if os.path.isfile(os.path.join(dataPath, f))]
        #this removes a folder that is typically hidden for mac users
        if '.DS_Store' in dataFiles:
            dataFiles.remove('.DS_Store')
        #This ensures that some value is given if no files exist
        #It then updates the data file list
        if len(dataFiles)==0:
            dataFiles = "No Current Files"
            self.Data_dropdown.configure(values=dataFiles)
            self.Labels_dropdown.configure(values=dataFiles)
        #creates an entry to allow the user to  choose no label file
        else:
            self.Data_dropdown.configure(values=dataFiles)
            dataFiles.insert(0, "No Label File")
            self.Labels_dropdown.configure(values=dataFiles)
            dataFiles.pop(0) 

    '''processes a csv and changes it into a numpy array'''
    def csvProcessing(self, dataFile, labelFile):
        """
        Processes a CSV file and changes it into a NumPy array.

        This method processes a CSV file and changes it into a NumPy array by reading the CSV file, dropping any NaN
        values, getting the unique movement labels, sorting the movement labels in alphabetical order, creating a mapping
        dictionary for the movement labels, creating a DataFrame for the movement labels, dropping the movement labels from
        the DataFrame, replacing the movement labels with the associated number, converting the DataFrame to a NumPy array,
        converting the DataFrame of movement labels to a NumPy array, and returning the NumPy arrays of the data and labels
        and the mapping dictionary.

        Args:
            dataFile: The data file to process.
            labelFile: The label file to process.

        Returns:
            [dataArray, labelsArray, mapping]: The NumPy arrays of the data and labels and the mapping dictionary.
        """
        #if the labels are in the same file
        if labelFile == "No Label File":
            dataTemp = dataPath+"/"+dataFile
            #datafile placed in pandas dataframe
            df = pd.read_csv(dataTemp)
            df.dropna(inplace=True)
            #movement labels are taken from label column
            names = df["label"].unique()
            #labels are sorted in alphabetical order
            names = sorted(names, key=str.lower)
            mapping = {}
            count = 0
            #dictionary for label and number to associate it with to allow for models to be created
            for x in names:
                mapping[x] = str(count)
                count += 1
            df2 = df["label"]
            df.drop(columns=['label'], inplace=True)
        #if they are different files
        else:
            dataTemp = dataPath+"/"+dataFile
            labelsTemp = dataPath+"/"+labelFile
            df = pd.read_csv(dataTemp)
            df2 = pd.read_csv(labelsTemp)
            columnNames = list(df2.columns)
            #movement labels are taken from label file
            names = df2[columnNames[0]].unique()
            #labels are sorted in alphabetical order
            names = sorted(names, key=str.lower)
            mapping = {}
            count = 0
            #dictionary for label and number to associate it with to allow for models to be created
            for x in names:
                mapping[x] = float(count)
                count += 1
        #labels are replaced with associated number
        df2 = df2.replace(mapping)
        df2 = df2.astype('float64')
        #drops alpha values if user specified electrode values only
        if self.check1Var.get()==1 and self.check2Var.get()==0:
            df = df.drop(columns=df.columns[8:11])
        #drops electrode values if user specified alpha values only
        elif self.check1Var.get()==0 and self.check2Var.get()==1:
            df = df.drop(columns=df.columns[0:8])
        dataArray = df.to_numpy()
        labelsArray = df2.to_numpy()
        return [dataArray, labelsArray, mapping]
#------------------ Modeling Page -----------------------


#------------------ Snake Game Page ---------------------
class SnakeGame(ctk.CTkFrame):
    """
    This class is the snake game page class that will be used to display the snake game page of the application.
    """
    def __init__(self, parent, controller):
        """
        This function initializes the snake game page class and creates the snake game page.

        Parameters:
            parent: The parent class of the current class.
            controller: The controller class that controls the current class.

        Returns:
            None
        """
        ctk.CTkFrame.__init__(self, parent)
        #Home button
        button1 = ctk.CTkButton(self, text ="Home",corner_radius=25, 
                            command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 20)
        #label for the page
        label = ctk.CTkLabel(self, text ="Snake Game", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 50, pady = 20)
        #button to start the snake game
        button2 = ctk.CTkButton(self, text = 'Snake Begin', corner_radius = 25, command = self.drawFrame)
        button2.grid(row = 2, column = 1, padx = 10, pady = 20)
        global active
        #dropbox for models        
        self.modelDropdown = ctk.CTkComboBox(self, values = modelFiles)
        self.modelDropdown.grid(row=3, column = 1, padx=10, pady=20)
        #update the model list
        update_button = ctk.CTkButton(self, text="Update Model Lists", corner_radius=25, command = self.updateFiles)
        update_button.grid(row=4, column=1, padx=10, pady=20)
        #button to select the model
        select_button = ctk.CTkButton(self, text="Select Model", corner_radius=25, command = self.modelSelection)
        select_button.grid(row=7, column=1, padx=10, pady=20)
        #button to start playing with predictions
        play_button = ctk.CTkButton(self, text="Play with Predictions", corner_radius=25, command = self.start_stream_thread)
        play_button.grid(row=8, column=1, padx=10, pady=20)
        #button to stop playing with predictions
        stop_button = ctk.CTkButton(self, text="Stop Predictions", corner_radius=25, command = self.stop_stream)
        stop_button.grid(row=9, column=1, padx=10, pady=20)
        #checkbox to select electrode data for graph
        self.check1Var = ctk.IntVar(value=1)
        self.check1 = ctk.CTkCheckBox(self, text = "Electrode Readings", onvalue=1, offvalue=0, corner_radius=5, variable=self.check1Var)
        self.check1.grid(row=5, column=1, padx=20, pady=10)
        #checkboc to select alpha values for graph
        self.check2Var = ctk.IntVar(value=1)
        self.check2 = ctk.CTkCheckBox(self, text = "Alpha Values", onvalue=1, offvalue=0, corner_radius=5, variable=self.check2Var)
        self.check2.grid(row=6, column=1, padx=10, pady=10)

        '''Variables for threading'''
        self.record_thread = None
        self.predict_thread = None
        self.stream_thread = None
        self.stop_predict = True

    '''Update list of models'''
    def updateFiles(self):
        """
        Updates the list of models.

        This method updates the list of models by getting the files in the model path and updating the model dropdown menu
        with the files.

        Args:
            None

        Returns:
            None
        """
        #this searches the given directory and checks if it is a file
        #if it is a file then it is added to the data file list
        modelFiles = [f for f in os.listdir(modelPath) if os.path.isfile(os.path.join(modelPath, f))]
        #this removes a folder that is typically hidden for mac users
        if '.DS_Store' in modelFiles:
            modelFiles.remove('.DS_Store')
        #This ensures that some value is given if no files exist
        #It then updates the data file list
        if len(modelFiles)==0:
            modelFiles = "No Current Files"
            self.modelDropdown.configure(values=modelFiles)
        else:
            self.modelDropdown.configure(values=modelFiles)

    '''Unpackages the model selected'''       
    def modelSelection(self):
        """
        Unpackages the model selected.

        This method unpackages the model selected by getting the model selected from the model dropdown menu and unpackages
        the model based on the model type.

        Args:
            None

        Returns:
            None
        """
        modelSelected = self.modelDropdown.get()
        print(modelSelected[-3:])
        #unpackages based on model type
        if modelSelected[-3:] == "pkl":
            self.model = joblib.load(modelPath+"/"+modelSelected)
        elif modelSelected[-2:] == ".pt":
            self.model = torch.load(modelPath+"/"+modelSelected)
        else:
            self.model = False

    '''Thread for recording EEG data'''
    def start_record(self):
        """
        Starts the recording of EEG data.
        
        This method starts the recording of EEG data by creating a new thread and calling the `record_data` function.
        
        Args:
            None
            
        Returns:
            None
        """
        #if the thread is not running, start it
        if self.record_thread is None or not self.record_thread.is_alive():
            self.record_thread = threading.Thread(target=self.record_data)
            self.record_thread.start()
    def stop_record(self):
        """
        Stops the recording of EEG data.

        This method stops the recording of EEG data by joining the record thread if it is alive.

        Args:
            None

        Returns:
            None
        """
        #if the thread is running, stop it
        if self.record_thread is not None and self.record_thread.is_alive():
            self.record_thread.join()
    def record_data(self):
        """
        Records the EEG data.

        This method records the EEG data by calling the `record` function from the connect.py.

        Args:
            None

        Returns:
            None
        """
        record(self)

    '''Thread for making predictions with the model selected and outputting to a temp file'''
    def start_predictions(self):
        """
        Starts making predictions with the model selected and outputting to a temp file.

        This method starts making predictions with the model selected and outputting to a temp file by reading the newest

        Args:
            None

        Returns:
            None
        """
        modelSelected = self.modelDropdown.get()
        while self.stop_predict is True:
            stream = pd.read_csv('newest_rename.csv')
            if self.check1Var.get()==1 and self.check2Var.get()==0:
                stream = stream.iloc[:, 8:11]
            elif self.check1Var.get()==0 and self.check2Var.get()==1:
                stream = stream.iloc[:, 0:8]
            else:
                stream = stream.iloc[:, 0:11]
            if stream.loc[len(stream)-1].isnull().values.any():
                stream = stream.dropna()
            stream_latest = stream.loc[len(stream)-1]
            #remove the header from stream_latest
            stream_latest = stream_latest.to_numpy()
            if modelSelected[-3:] == "pkl":
                prediction = self.model.predict(stream_latest.reshape(1, -1))
            elif modelSelected[-2:] == ".pt":
                prediction = self.model.eval(stream_latest)
            else:
                print("No model selected")
            #opening tempPred file as empty to write the new prediction
            file = open("tempPred.txt", "w")
            #writing the prediction to the file
            file.write(str(int(prediction[0])))
            file.close()
    def start_prediction_thread(self):
        """
        Starts the prediction thread.
        
        This method starts the prediction thread by creating a new thread and calling the `start_predictions` function.
        
        Args:
            None
            
        Returns:
            None
        """
        if self.predict_thread is None or not self.predict_thread.is_alive():
            self.predict_thread = threading.Thread(target=self.start_predictions)
            self.predict_thread.start()
    def stop_predictions(self):
        """
        Stops the predictions.

        This method stops the predictions by setting the stop predict variable to false and joining the prediction thread
        if it is alive.

        Args:
            None

        Returns:
            None
        """
        self.stop_predict = False
        if self.predict_thread is not None and self.predict_thread.is_alive():
            self.predict_thread.join()

    '''Thread for sending predictions to the snake game as keypresses'''
    def predictStream(self):
        """
        Sends predictions to the snake game as keypresses.

        This method sends predictions to the snake game as keypresses by reading the prediction from the temp file and
        sending the corresponding keypress to the snake game.

        Args:
            None

        Returns:
            None
        """
        self.drawFrame()
        self.start_record()
        #Allow stream to start before prompting
        time.sleep(15)
        self.start_prediction_thread()
        while self.stop_predict is True:
            pred_file = open("tempPred.txt", "r")
            #Continue if the file is empty
            if pred_file.read() == ' ':
                prediction = 3
            else:
                prediction = pred_file.seek(0)
            #Read the prediction from the file as an integer
            prediction = pred_file.read()
            print(prediction)
            if prediction == 0:
                app.event_generate('<Up>')
            elif prediction == 1:
                app.event_generate('<Left')
            elif prediction == 2:
                app.event_generate('<Down>')
            elif prediction == 3:
                app.event_generate('<Right>')
            elif prediction == 4:
                continue
            else:
                print("Error in prediction")
                self.stop_record()
    def start_stream_thread(self):
        """
        Starts the stream thread.

        This method starts the stream thread by creating a new thread and calling the `predictStream` function.
        
        Args:
            None
        Returns:
            None
        """
        if self.stream_thread is None or not self.stream_thread.is_alive():
            self.stream_thread = threading.Thread(target=self.predictStream)
            self.stream_thread.start()
    def stop_stream(self):
        """
        Stops the stream.

        This method stops the stream by setting the stop predict variable to false and joining the stream thread if it is
        alive.

        Args:
            None

        Returns:
            None
        """
        self.stop_predict = False
        if self.stream_thread is not None and self.stream_thread.is_alive():
            self.stream_thread.join()
        self.stop_predictions()
        self.stop_record()

    '''Snake Game Functions'''
    def drawFrame(self):
        """
        Initializes the snake game function variables.
        
        This method initializes the snake game function variables by creating the canvas object that holds the snake game,
        initializing the snake, initializing the first food pellet, and starting the game.
        
        Args:
            None
            
        Returns:
            None
        """
        global canvas
        global snake
        global g_food
        global active
        global pointCount
        active = True
        score = 0
        #canvas object that holds the snake game
        canvas = ctk.CTkCanvas(self, bg='black', height=260, width=260)
        canvas.grid(row=2, rowspan=5, column=2, padx=10, pady=10)
        #intialize the label that will hold the score board for the game
        pointCount = ctk.CTkLabel(self, text="Points: {}".format(score), font=LARGEFONT)
        pointCount.grid(row=1, column=2, padx=10, pady=10)
        #intialize the snake
        snake = Snake(canvas)
        #intialize the first food pellet
        g_food = Food(canvas)
        #start the game
        root = SnakeGame
        #binds arrow keys to movement types in the game
        app.bind('<Left>', lambda event: self.move("left", snake, g_food, root, canvas))
        app.bind('<Right>', lambda event: self.move("right", snake, g_food, root, canvas))
        app.bind('<Up>', lambda event: self.move("up", snake, g_food, root, canvas))
        app.bind('<Down>', lambda event: self.move("down", snake, g_food, root, canvas))
        app.bind('<space>', lambda event: self.game_over())
    '''Handles snake movement fucntions'''
    def move(self, direction, snake, g_food, root, canvas):
        """
        Handles the snake movement.

        This method handles the snake movement by changing the direction of the snake, moving the snake to the next square,
        and checking for food consumption.

        Args:
            direction: The direction to move the snake.
            snake: The snake object to move.
            g_food: The food object to check for food consumption.
            root: The root object to move the snake.
            canvas: The canvas object to move the snake.

        Returns:
            None
        """
        global active
        #reads in movement types from the controller (likely computer or model)
        if active:
            #changes stored 'oreintion of the snake'
            self.change_direction(direction)
            #moves the snake to the next square (handles movement and checks for food consumtion)
            self.next_turn(snake, g_food, root, canvas) 
    '''Executes the game over protocol and cleanup'''
    def game_over(self):
        """
        Executes the game over protocol and cleanup.

        This method executes the game over protocol and cleanup by setting the active variable to false, destroying the game
        objects and canvas, and displaying the game over text.

        Args:
            None

        Returns:
            None
        """
        global active
        #destroys game objects and canvas if the user opts to quit the game
        active = False
        canvas.delete(ALL)
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 30), 
                           text="GAME OVER", fill="red", tag="gameover") 
    '''Handles orienting the snake in the correct direction'''
    def change_direction(self, new_direction):
        """
        Changes the direction of the snake.

        This method changes the direction of the snake by changing the orientation of the snake according to the most recent
        input from the controller.

        Args:
            new_direction: The new direction to change the snake to.

        Returns:
            None
        """
        global direction
        #changes the 'orienation' of the snake according to the most recent input from the controller
        if new_direction == 'left':
            direction = new_direction
        elif new_direction == 'right':
            direction = new_direction
        elif new_direction == 'up':
            direction = new_direction
        elif new_direction == 'down':
            direction = new_direction
    '''Determines if snake has run into the preset boundaries of the game'''
    def check_collisions(self, coordinates):
        """
        Checks if the snake has collided with the boundaries of the game.

        This method checks if the snake has collided with the boundaries of the game by checking if the snake has collided
        with the boarders of the canvas.

        Args:
            coordinates: The coordinates of the snake.

        Returns:
            True: If the snake has collided with the boundaries of the game.
            False: If the snake has not collided with the boundaries of the game.
        """
        #checks if the snake has collided of the boarders of the canvas
        #otherwise, snake could move to infinity
        x, y = coordinates
        #checks horizontal boundary
        if x < 0 or x >= WIDTH-2:
            return True
        #checks vertical boundary
        elif y < 0 or y >= HEIGHT-2:
            return True
        return False
    '''Handles snake movement'''
    def next_turn(self, snake, food, root, canvas):
        """
        Handles the next turn of the snake.

        This method handles the next turn of the snake by moving the snake to the next square, checking for food consumption,
        and checking for collisions.

        Args:
            snake: The snake object to move.

        Returns:
            None
        """
        if active:
            global direction
            #defines snakes current location
            x, y = snake.coordinates[0]
            #updates snake's coordinates according to into orientation
            if direction == "up":
                y -= SPACE_SIZE
            elif direction == "down":
                y += SPACE_SIZE
            elif direction == "left":
                x -= SPACE_SIZE
            elif direction == "right":
                x += SPACE_SIZE
            #determines if the snake is running into a boundary or at a boundary
            if check_collisions((x,y)):
                #if at a boundary, the snake can no longer move until it given a direction that brings it away from the boundary
                direction = "collision"
            else:
                #once verified that there is no collision, the snake's new cooordinates are offically stored here
                snake.coordinates.insert(0, (x, y))
                #creates the rectangle for the snake at its new location
                square = snake.canvas.create_rectangle(
                    x, y, x + SPACE_SIZE,
                            y + SPACE_SIZE, fill=SNAKE)
                snake.squares.insert(0, square)
                #checks if the snake has collided with the generated food pellet
                if x == food.coordinates[0] and y == food.coordinates[1]:
                    #if so, ..
                    global score
                    global g_food
                    #score updates
                    score += 1
                    #update score label with new information
                    pointCount.configure(text="Points: {}".format(score))
                    #deletes food pellet and randomly generates a new one
                    snake.canvas.delete("food")
                    g_food = Food(canvas)
                # deletes the snakes trail the ensure the snake remains of length 1
                del snake.coordinates[-1]
                snake.canvas.delete(snake.squares[-1])
                del snake.squares[-1]
#------------------ Snake Game Page ---------------------


'''Robotic Wheel Chair Control Page'''
#------------------ USB Output Page ---------------------
class USBOutput(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="USB Output", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 100, pady = 10)
        #button to return to home page
        button1 = ctk.CTkButton(self, text ="Home",corner_radius=25,
                            command = lambda : controller.show_frame(Home))
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 30)
        
        # button sends "foreward" request directly to ESP via IP
        buttonForeward = ctk.CTkButton(self, text ="Forward",
                            command = lambda : wcc.motorForward())
        buttonForeward.grid(row = 2, column = 4, pady = 12)
        
        # button sends "left" request directly to ESP via IP
        buttonLeft = ctk.CTkButton(self, text ="Left",
                            command = lambda : wcc.turnLeft())
        buttonLeft.grid(row = 3, column = 3)

        # button sends "stop" request directly to ESP via IP
        buttonStop = ctk.CTkButton(self, text ="Stop",
                            command = lambda : wcc.motorStop())
        buttonStop.grid(row = 3, column = 4, pady = 12)

        # button sends "right" request directly to ESP via IP
        buttonRight = ctk.CTkButton(self, text ="Right",
                            command = lambda : wcc.turnRight())
        buttonRight.grid(row = 3, column = 5)

        # button sends "backward" request directly to ESP via IP
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

        self.model = False
        self.update()
        '''Bind keys to functions that send requests to ESP'''
        self.bind('<Left>', lambda event: wcc.turnLeft())
        self.bind('<Right>', lambda event: wcc.turnRight())
        self.bind('<Up>', lambda event: wcc.motorForward())
        self.bind('<Down>', lambda event: wcc.motorBackward())
        self.bind('<space>', lambda event: wcc.motorStop())
        #button to select the model
        select_button = ctk.CTkButton(self, text="Select Model", corner_radius=25, command = self.modelSelection)
        select_button.grid(row=9, column=1, padx=10, pady=20)

        #button to start playing with predictions
        play_button = ctk.CTkButton(self, text="Play with Predictions", corner_radius=25, command = self.start_stream_thread)
        play_button.grid(row=10, column=1, padx=10, pady=20)

        #button to stop playing with predictions
        stop_button = ctk.CTkButton(self, text="Stop Predictions", corner_radius=25, command = self.stop_stream)
        stop_button.grid(row=11, column=1, padx=10, pady=20)

        #checkbox to select electrode data for graph
        self.check1Var = ctk.IntVar(value=1)
        self.check1 = ctk.CTkCheckBox(self, text = "Electrode Readings", onvalue=1, offvalue=0, corner_radius=5, variable=self.check1Var)
        self.check1.grid(row=7, column=1, padx=20, pady=10)

        #checkboc to select alpha values for graph
        self.check2Var = ctk.IntVar(value=1)
        self.check2 = ctk.CTkCheckBox(self, text = "Alpha Values", onvalue=1, offvalue=0, corner_radius=5, variable=self.check2Var)
        self.check2.grid(row=8, column=1, padx=10, pady=10)

        '''Variables for threading'''
        self.record_thread = None
        self.predict_thread = None
        self.stream_thread = None
        self.stop_predict = True

    '''Update list of models'''
    def updateFiles(self):
        #this searches the given directory and checks if it is a file
        #if it is a file then it is added to the data file list
        modelFiles = [f for f in os.listdir(modelPath) if os.path.isfile(os.path.join(modelPath, f))]
        #this removes a folder that is typically hidden for mac users
        if '.DS_Store' in modelFiles:
            modelFiles.remove('.DS_Store')
        #This ensures that some value is given if no files exist
        #It then updates the data file list
        if len(modelFiles)==0:
            modelFiles = "No Current Files"
            self.modelDropdown.configure(values=modelFiles)
        else:
            self.modelDropdown.configure(values=modelFiles)

    '''Unpackages model selected by user'''        
    def modelSelection(self):
        modelSelected = self.modelDropdown.get()
        print(modelSelected[-3:])
        #unpackages model based on model type
        if modelSelected[-3:] == "pkl":
            self.model = joblib.load(modelPath+"/"+modelSelected)
        elif modelSelected[-2:] == ".pt":
            self.model = torch.load(modelPath+"/"+modelSelected)
        else:
            self.model = False

    '''Thread for recording EEG data'''
    def start_record(self):
        if self.record_thread is None or not self.record_thread.is_alive():
            self.record_thread = threading.Thread(target=self.record_data)
            self.record_thread.start()
    def stop_record(self):
        if self.record_thread is not None and self.record_thread.is_alive():
            self.record_thread.join()
    def record_data(self):
        record(self)

    '''Thread for making predictions with the model selected and outputting to a temp file'''
    def start_predictions(self):
        modelSelected = self.modelDropdown.get()
        while self.stop_predict is True:
            stream = pd.read_csv('newest_rename.csv')
            if self.check1Var.get()==1 and self.check2Var.get()==0:
                stream = stream.iloc[:, 8:11]
            elif self.check1Var.get()==0 and self.check2Var.get()==1:
                stream = stream.iloc[:, 0:8]
            else:
                stream = stream.iloc[:, 0:11]
            if stream.loc[len(stream)-1].isnull().values.any():
                stream = stream.dropna()
            stream_latest = stream.loc[len(stream)-1]
            #remove the header from stream_latest
            stream_latest = stream_latest.to_numpy()
            if modelSelected[-3:] == "pkl":
                prediction = self.model.predict(stream_latest.reshape(1, -1))
            elif modelSelected[-2:] == ".pt":
                prediction = self.model.eval(stream_latest)
            else:
                print("No model selected")
            #opening tempPred file as empty to write the new prediction
            file = open("tempPred.txt", "w")
            #writing the prediction to the file
            file.write(str(int(prediction[0])))
            file.close()
    def start_prediction_thread(self):
        if self.predict_thread is None or not self.predict_thread.is_alive():
            self.predict_thread = threading.Thread(target=self.start_predictions)
            self.predict_thread.start()
    def stop_predictions(self):
        self.stop_predict = False
        if self.predict_thread is not None and self.predict_thread.is_alive():
            self.predict_thread.join()

    '''Thread for sending predictions to the wheelchair as commands'''
    def predictStream(self):
        self.start_record()
        #Allow stream to start before prompting
        time.sleep(15)
        self.start_prediction_thread()

        while self.stop_predict is True:
            pred_file = open("tempPred.txt", "r")
            #Continue if the file is empty
            if pred_file.read() == ' ':
                prediction = 3
            else:
                prediction = pred_file.seek(0)
            #Read the prediction from the file as an integer
            #print(prediction)
            if prediction == 0:
                wcc.motorForward()
            elif prediction == 1:
                wcc.turnLeft()
            elif prediction == 2:
                wcc.motorBackward()
            elif prediction == 3:
                wcc.turnRight()
            elif prediction == 4:
                wcc.motorStop()
                continue
            else:
                print("Error in prediction")
                wcc.motorStop()
                self.stop_record()
    def start_stream_thread(self):
        if self.stream_thread is None or not self.stream_thread.is_alive():
            self.stream_thread = threading.Thread(target=self.predictStream)
            self.stream_thread.start()
    def stop_stream(self):
        self.stop_predict = False
        if self.stream_thread is not None and self.stream_thread.is_alive():
            self.stream_thread.join()
        self.stop_predictions()
        self.stop_record()
#------------------ USB Output Page ---------------------


#------------------ Main Loop ---------------------------
score = 0
direction = 'down'
# Driver Code
app = App()
app.geometry("1100x800")
app.update()
app.mainloop()
#------------------ Main Loop ---------------------------