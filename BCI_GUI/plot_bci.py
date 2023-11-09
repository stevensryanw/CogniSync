#Script for gui_bci to plot data to plot data in the gui
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

global dataFolder

dataFolder = 'data/processed/'

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate8(i):
    data = pd.read_csv(dataFolder + filename)
    dataArray = data.iloc[:, :8]
    ax1.clear()
    # Each channel is a line plotted separately on the same graph y-axis is alpha value, x-axis is time, should only show most recent 10 seconds
    for channel in range(8):
        ax1.plot(dataArray.iloc[:, channel])

def animate3(i):
    data = pd.read_csv(dataFolder + filename)
    dataArray = data.iloc[:, 8:]
    ax1.clear()
    # Each alpha is a line plotted separately on the same graph y-axis is alpha value, x-axis is time, should only show most recent 10 seconds
    for alpha in range(3):
        ax1.plot(dataArray.iloc[:, alpha])

def set_filename(file):
    global filename
    filename = file

def plot_eeg(shape, file):
    set_filename(file)
    if shape == 8:
        anim = animation.FuncAnimation(fig, animate8, frames=None, interval=1000, cache_frame_data=False)
        return anim
    elif shape == 3:
        anim = animation.FuncAnimation(fig, animate3, frames=None, interval=1000, cache_frame_data=False)
        return anim
    else:
        print("Error: Invalid shape")

# ani = plot_eeg(8, 'blinksFiltered.csv')
# plt.show()