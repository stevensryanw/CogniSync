#Script for the gui to get and load the selected data
#This script will be called by the gui
#This script will load the data and labels for the user selected movements
#This script will return the data and labels to the gui

import pandas as pd
import numpy as np
import random

def process_data(file):
    data = pd.read_csv(file, sep=",", header=None)

    #Removing columns 12-22
    data = data.drop(data.columns[12:22], axis=1)
    #Remove the first 1000 samples
    data = data.drop(data.index[0:1000])
    #Reindex the data
    data = data.reset_index(drop=True)
    data

    #Create a dataframe for the data, columns 1-11
    useful_data = data.iloc[:,1:12]

    #Create alpha labels, columns 9-11
    alphaLabels = data.iloc[:,9:12]

    #Create a 1d dataframe of the alphas summed
    alphaSum = alphaLabels.mul([9,10,11]).sum(axis=1)

    #Plot alpha labels
    alphaLabels.plot()

    #Ploting the data
    useful_data.plot()

    n_samps = len(useful_data)
    n_blinks = 40
    lenRangeDown = 30
    lenRangeUp = 60
    labels = pd.DataFrame()

    #Append 21491 norm labels to the dataframe
    for i in range(n_samps):
        labels = labels._append(['norm'])

    #Generate random blink labels
    for _ in range(n_blinks):
        # Randomly select the start and end indices for each blink
        start_idx = random.randint(0, n_samps - lenRangeUp)
        end_idx = start_idx + random.randint(lenRangeDown, lenRangeUp)
        
        # Set the blink labels for the selected range
        for i in range(start_idx, end_idx):
            labels.iloc[i] = 'blink'

    labels.value_counts()

    #Outputing our final data and labels to csv
    useful_data.to_csv('../../Data/Processed/blinksFiltered.csv', index=False)
    labels.to_csv('../../Data/Processed/blinksFilteredLabels.csv', index=False)

def get_data(file):
    useless_data = pd.read_csv(file, sep=",", header=None)
    #data is columns 0-11
    data = useless_data.iloc[:,0:12]
    #labels is the last column
    labels = useless_data.iloc[:,-1]
    return data, labels