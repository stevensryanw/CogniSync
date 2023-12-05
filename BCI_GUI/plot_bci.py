#Script for gui_bci to plot data to plot data in the gui
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure

global dataFolder

dataFolder = 'data/processed/'

fig = Figure(figsize=(5,4), dpi=100)
ax1 = fig.add_subplot(1,1,1)
ax2 = fig.add_subplot(1,2,1)

def animate8(i):
    data = pd.read_csv(filename)
    dataArray = data.iloc[:, :8]
    ax1.clear()
    # Each channel is a line plotted separately on the same graph y-axis is alpha value, x-axis is time, should only show most recent 10 seconds
    for channel in range(8):
        ax1.plot(dataArray.iloc[:, channel])

def animate3(i):
    data = pd.read_csv(filename)
    dataArray = data.iloc[:, 8:]
    ax2.clear()
    # Each alpha is a line plotted separately on the same graph y-axis is alpha value, x-axis is time, should only show most recent 10 seconds
    for alpha in range(3):
        ax2.plot(dataArray.iloc[:, alpha])

def set_filename(file):
    global filename
    filename = file

def plot_eeg(file):
    set_filename(file)
    anim8 = animation.FuncAnimation(fig, animate8, frames=None, interval=1000, cache_frame_data=False)
    plt.show()
    return anim8

def plot_alpha(file):
    set_filename(file)
    anim3 = animation.FuncAnimation(fig, animate3, frames=None, interval=1000, cache_frame_data=False)
    plt.show()
    return anim3

#ani = plot_eeg(3, 'blinksFiltered.csv')
#plt.show()