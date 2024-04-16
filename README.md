# CogniSync

## Project Goals
- [X] Create an easy to use GUI for EEG data and modeling
- [ ] 

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
