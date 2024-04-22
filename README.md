# CogniSync

## Project Goals
- [X] Create an easy to use GUI for EEG data and modeling
- [X] Provide motor imagery predictions for controls
- [ ] Use predictions to successfully play the snake game
- [ ] Use predictions to accurately control the robotic wheelchair

## Project Features (TKinter Pages)
- [X] Plotting eeg - ```plotEEG()```
  - [X] Gui for easily customizing Plotly
- [X] User recording - ```UserRecording()```
  - [X] Streaming EEG data (8 Channels, 3 AUX)
  - [X] Prompting (1 Label)
  - [X] Recording (Combining the 11 dimensions of data into one .csv)
- [X] Modeling - ```Modeling()```
  - [X] SciKit-Learn (LDA, DTC, RFC, LRC)
  - [X] PyTorch
  - [ ] Tensorflow (CPU possible, but GPU is too finiky)
- [X] Snake Game - ```SnakeGame()```
  - [X] Model selection/input
  - [X] Prediction outputs
  - [ ] Sending predictions as controls
- [X] USB Output - ```USBOutput()```
  - [X] Model selection/input
  - [X] Prediction outputs
  - [ ] Sending predictions as controls

## Future Improvements
- [ ] Further improve model accuracy, f1, precision, and recalls
- [ ] Online training with PyTorch

# ```gui_bci.py```

### Class ```App()```
  - ```__init__(self, parent, controller)```
  - ```show_frame(self, cont)```
### Class ```Home()```
  - ```__init__(self, parent, controller)```
### Class ```PlotEEG()```
  - ```__init__(self, parent, controller)```
  - ```updateList(self)```
  - ```slide1(self, value)```
  - ```slide2(self, value)```
  - ```plot_eeg(self)```
### Class ```UserRecording()```
  - ```__init__(self, parent, controller)```
### Class ```Modeling()```
  - ```__init__(self, parent, controller)```
### Class ```SnakeGame()```
  - ```__init__(self, parent, controller)```
### Class ```USBOutput()```
  - ```__init__(self, parent, controller)```

## ```connect.py```

## ```model_bci.py```

## ```snake.py```

## ```wheelchairController.py```