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
 - ```BCI_sklearn_SVC(data, labels)```  
  This creates a fitted support vector machine bagging classifier model using the ```BaggingClassifier()``` function from scikit-learn. 
  The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split. 
  The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information.
  The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. None of the parameters have been specified except for n_jobs which is set to -1. This allows the entire CPU and memory to be used to fit 
  the model. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function.
  This function returns the result of passing the model, test data , and test labels into ```scoring()```.
 - ```BCI_sklearn_RandomForestClassifier(data, labels)```  
  This creates a fitted random forest classifier model using the ```RandomForestCLassifier()``` function from scikit-learn. 
  The parameters for max_depth, min_samples_split, min_samples_leaf, criterion, n_estimators, max_features, and bootstrap have been given as 
  we found this to be the best during our optimization. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. None of the parameters have been specified except for n_jobs which is set to -1. This allows the entire CPU and memory to be used to fit 
  the model. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function.
  This function returns the result of passing the model, test data , and test labels into ```scoring()```.
 - ```BCI_sklearn_DecisionTreeClassifier(data, labels)```  

 - ```BCI_sklearn_LogisticRegression(data, labels)```  

 - ```BCI_sklearn_GradientBoostingClassifier(data, labels)```  

 - ```BCI_sklearn_KNeighborsClassifier(data, labels)```  

 - ```BCI_sklearn_GaussianNB(data, labels)```  

 - ```BCI_sklearn_MLPClassifier(data, labels)```  

 - ```BCI_sklearn_LinearDiscriminiantAnalysis(data, labels)```  

 - ```BCI_sklearn_QuadraticDiscriminiantAnalysis(data, labels)```  

 - ```BCI_pytorch_Net(data, labels)```  

 - ```BCI_tensorflow_Net(data, labels)```  

 - ```scoring(model, x, y)```  

## ```snake.py```

## ```wheelchairController.py```
 - ```root_url```  
   This variable is the most important variable of the script as it holds the IP address for the WiFi ESP8266.
   Using this IP, the script can communicate with controller as long as the device running the script is connected to the same network.
 - ```sendRequest(url)```  
   This uses the ```urllib.request``` function ```urlopen``` to send a request to the microcontroller via WiFi.
   The request sent is dependent on the tag attached to the end of the url after the IP address.
 - ```motorForeward()```  
   This uses ```sendRequest(url)``` to send the ```forward``` command to the microcontroller.
 - ```motorBackward()```  
   This uses ```sendRequest(url)``` to send the ```backward``` command to the microcontroller.
 - ```turnLeft()```  
   This uses ```sendRequest(url)``` to send the ```left``` command to the microcontroller.
 - ```turnrRight()```  
   This uses ```sendRequest(url)``` to send the ```right``` command to the microcontroller.
 - ```motorStop()```  
   This uses ```sendRequest(url)``` to send the ```stop``` command to the microcontroller.
