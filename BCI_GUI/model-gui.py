import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import models.bci_tensorflow as bci_tf

#Window for selecting the model then training and testing it

class ModelGUI(tk.Frame):
    #Initialize the frame
    def __init__(self):
        tk.Frame.__init__(self)
        #Initialize the window
        self.master.title("Model Selection")
        self.master.geometry("500x500")
        #Initialize the frame
        self.grid()
        #Create a selector for the models in model_bci.py
        self.model_selector = ttk.Combobox(self, values = ["SVM", "Random Forest", "Gradient Boosting", "KNN", "Gaussian Naive Bayes", "MLP", "Linear Discriminant Analysis", "Quadratic Discriminant Analysis", "Net"])
        self.model_selector.grid(row = 0, column = 0, padx = 10, pady = 10)

        #Create a button to select the model
        #self.select_model_button = ttk.Button(self, text = "Select Model", command = bci_tf.BCI_tensorflow_sequential)
        #self.select_model_button.grid(row = 0, column = 1, padx = 10, pady = 10)
        #Ask for filename
        #self.filename = filedialog.askopenfilenames()
        #Call each specific model from model_bci.py


#Launch the GUI
app = ModelGUI()
app.mainloop()