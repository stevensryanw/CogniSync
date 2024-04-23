![CogniSync](https://github.com/stevensryanw/CogniSync/resources/CogniSyncLogo.png)
# [CogniSync: Machine Learning & EEG-Based Directional Controls](https://sse.tulane.edu/2024-engineering-capstone-design-expo/department-computer-science-abstracts)
## Tulane University Computer Science: FALL 2023 - SPRING 2024
## Contributors: Justin Haysbert, Gabriel Sagrera, Shayne Shelton, Ryan Stevens
## Faculty Mentor: Saad Hassan
### SSE EXPO: April 23, 2024

There are millions of paralysis patients in the United States. Electroencephalogram (EEG) headsets offer a way for these patients to operate mechanical devices provided motor imagery related brain waves. Machine learning approaches like SciKit-Learn (LDA, LRC, DTC, and RFC) and PyTorch can accurately and precisely categorize a user’s brain state into directional controls for this application. However, training time is long, training is user specific, and EEGs experience a low signal-to-noise ratio. This project aims to reduce user training time by (1) decreasing the number of movements users perform during training and (2) building a comprehensive graphical user interface (GUI) to streamline the recording, modeling, and prediction processes.

# [YouTube Demo](https://youtu.be/2NKWB9IQvQE)

# [EEG Headset](https://shop.openbci.com/products/3d-print-it-yourself-neurotechnologist-bundle-up-to-8-channels?_pos=3&_psq=print&_ss=e&_v=1.0)

## Project Goals
- [X] Create an easy-to-use GUI for EEG data and modeling
- [X] Provide motor imagery predictions for controls
- [ ] Use predictions to successfully play the snake game
- [ ] Use predictions to accurately control the robotic wheelchair

## Project Features (Tkinter Pages)
- [X] Plotting eeg - ```plotEEG()```
  - [X] Gui for easily customizing Plotly
- [X] User recording - ```UserRecording()```
  - [X] Streaming EEG data (8 Channels, 3 AUX)
  - [X] Prompting (1 Label)
  - [X] Recording (Combining the 11 dimensions of data into one .csv)
- [X] Modeling - ```Modeling()```
  - [X] SciKit-Learn (LDA, DTC, RFC, LRC)
  - [X] PyTorch
  - [ ] Tensorflow (CPU possible, but GPU is too finicky)
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
- [ ] Online training with PyTorch (feedback function)
- [ ] Tensorflow model using a GPU
- [ ] EEG headset alignment protocol/GUI
      - Possibility that the headset placement variability between uses changes the entire feed of data every time
- [ ] Switch to ESP32 for Bluetooth control to easier connect robotic wheelchair
      - Currently requires serial connection to read ip address
- [ ] Fix stopping of threads
      - current solution is to close the GUI and reopen it

# ```gui_bci.py```

### Class ```App()```
  - ```__init__(self, parent, controller)```
    Intializes the application by creating a container frame. Uses an empty dictionary to store all frames used to iterate through all the pages of the GUI. 
  - ```show_frame(self, cont)```
    Takes a frame and raises it to the top making it visible to the user
### Class ```Home()```
  - ```__init__(self, parent, controller)```
    Intializes the home page of the GUI with the needed buttons for all pages plotEEG, UserRecording, Modeling, SnakeGame, and USBOutput. When buttons are clicked they call ```show_frame(self, cont)``` to move that frame to the top. 
### Class ```PlotEEG()```
  - ```__init__(self, parent, controller)```
  - ```updateList(self)```
  - ```slide1(self, value)```
  - ```slide2(self, value)```
  - ```plot_eeg(self)```
### Class ```UserRecording()```
  - ```__init__(self, parent, controller)```
  Initialization function that creates the instruction canvas, initializes the prompt time settings, some default movement settings and all widgets.

  - ```update_movements(self, event)```
  This function is used to update the movement list given that there is user input. If user input is void movements default to right arm, left arm, legs, and jaw.
  - ```start_prompting(self)```
  This function is called when the start button is pressed. It disables the start button and enables the stop button. When pressed sets is prompting to True and calls ```prompt_next_movement(self)``` and ```start_record(self)```. It sets our total_prompts count to the product of the user selected iterations and movement count. If thhe user has not specified it defaults to 4 movements by 40 iterations. This function sleeps 15 seconds to ensure data stream can begin. 
  - ```stop_prompting(self)```
  This function is called when the stop button is pressed while recording. is_promting is set to false and the start button is enables while the stop button is disabled. A label stating 'Training canceled' is printed and the movement index is set to 0. movements are shuffled and prompting times are reset. If the canvas till holds text it is wiped. 
  - ```end_prompting(self)```
  This function is called when the prompting reaches its conclusion. Is_prompting is set to False, start button is enabled, and stop button is disabled. A label stating training completed is printed and the output file name is set to user input. If the output file is blank or filled with whitespace the output file is defaulted to 'YOU_DATA.csv'. The experiment results are then copied into the user specified file. Movement index is set to 0, movements are shuffled and prompt times are reset. 
  - ```shuffle_movements(self)```
  Randomly shuffles order of movements.
  - ```prompt_next_movement(self)```
  If the prompt_count is less that the total_prompts and is_prompting is true we give a text label "Prepare for next movement", delete what was previously held in the canvas and after 5 seconds call ```show_movement_instruction(self)```. If not then```end_prompting(self)``` is called.
  - ```show_movement_instruction(self)```
  If is_prompting is true the text label 'Hold the movement for 10 seconds' is thrown. If no custom movements have been defined recall default movements. current movement is marked as the current movement index of the list of movements. Shows the user the current movement for the full 10 second interval. 2 seconds into the iterval begin writing to our csv data file using ,```start_writing_to_file(self)``` after 6 seconds stop writing with ```stop_writing_to_file(self)```. After 10 second interval show the rest period using ```show_rest_period(self)```. If not promting close our output file, cancel training, and delete canvas content.
  - ```start_writing_to_file(self)```
  Function closes the temp_val.txt then reopens it and writes the current movement and closes it again.
  - ```stop_writing_to_file(self)```
  Function ensures temp_val.txt is closed
  - ```show_rest_period(self)```
  if is_prompting is true throw text "Rest for 10 seconds' and clear the canvas. Close the temp_val.txt file. Increment the prompt_count by 1 and set the current movement index to the next slot. if the current movement index is 0 shuffle the movements using ```shuffle_movements(self)```. After the 10 second rest time prompt the next movement using ```prompt_next_movement(self)```.
  - ```start_record(self)```
  - ```stop_record(self)```
  - ```record_data(self)```
### Class ```Modeling()```
  - ```__init__(self, parent, controller)```
  This creates all the widgets for the model page including dropdowns for selecting the model, data file and label file. The widgets for the checkbox also have an IntVar created to help determine whether it has been clicked or not. 
  - ```model_input(self)```
  - ```updateFiles(self)```

  - ```csvProcessing(self, dataFile, labelFile)```
  This function is to process the csv file chosen by the user in the gui. The dataFile parameter is a string of the file chosen by the user which is then found by going to the data folder and searching for the file there. The labelFile parameter is the same as the dataFile parameter except for label files chosen by the user or that there is no label file. The if statement splits based on whether a label file has been chosen or not. If no label file was chosen then the path to the data file is created and passed to ```pandas.read_csv``` and stored. All rows with NA values are dropped with the label column being stored as a separate dataframe and deleted from the data dataframe. The unique values in the labels frame are taken and sorted in a list by alphabetical order and replaced with numbers unique to each different label value. The else statement follows this format but reads in both the data file and label file given. If the checkbox for the alpha values has been unchecked then the alpha value columns are dropped and if the electrode reading checkbox is unchecked then the electrode reading columns are removed. The dataframes are then turned into numpy arrays and will return a list of the data numpy array, label numpy array, and a dictionary of the label values and corresponding number. 
### Class ```SnakeGame()```
  - ```__init__(self, parent, controller)```
### Class ```USBOutput()```
  - ```__init__(self, parent, controller)```

## ```connect.py```

## ```model_bci.py```
  - ```BCI_sklearn_SVC(data, labels)```  
  This creates a fitted support vector machine bagging classifier model using the ```BaggingClassifier()``` function from scikit-learn. 
  The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. None of the parameters have been specified except for n_jobs which is set to -1. This allows the entire CPU and memory to be used to fit 
  the model. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function.
  This function returns the result of passing the model, test data, and test labels into ```scoring()```. It is heavily recommended that SVC only uses small datasets as it will take a long time to fit otherwise.
 - ```BCI_sklearn_RandomForestClassifier(data, labels)```  
  This creates a fitted random forest classifier model using the ```RandomForestCLassifier()``` function from scikit-learn. 
  The parameters for max_depth, min_samples_split, min_samples_leaf, criterion, n_estimators, max_features, and bootstrap have been given as 
  we found this to be the best during our optimization. The n_jobs parameter has been set to -1 which allows the entire CPU and memory to be used to fit the model. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. This allows the entire CPU and memory to be used to fit the model. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data, and test labels into ```scoring()```.
 - ```BCI_sklearn_DecisionTreeClassifier(data, labels)```  
  This creates a fitted decision tree classifier model using the ```DecisionTreeCLassifier()``` function from scikit-learn. 
  The parameters for max_depth, min_samples_split, min_samples_leaf, max_features, splitter, and criterion have been given as 
  we found this to be the best during our optimization. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data, and test labels into ```scoring()```.

 - ```BCI_sklearn_LogisticRegression(data, labels)```  
  This creates a fitted logistic regression model using the ```LogisticRegression()``` function from scikit-learn. 
  The parameters for C, class_weight, dual, fit_intercept, intercept_scaling, l1_ratio, max_iter, multi_class, penalty, 
  random_state, solver, tol, verbose, and warm_start have been given as we found this to be the best during our optimization. The n_jobs parameter has been set to -1 which allows the entire CPU and memory to be used to fit the model. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data, and test labels into ```scoring()```.

 - ```BCI_sklearn_GradientBoostingClassifier(data, labels)```  
  This creates a fitted gradient boosting classifier model using the ```GradientBoostingClassifier()``` function from scikit-learn. 
  The parameters are all the default ones from scikit-learn. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data , and test labels into ```scoring()```.

 - ```BCI_sklearn_KNeighborsClassifier(data, labels)``` 
  This creates a fitted k nearest neighbors classifier model using the ```KNeighborsClassifier()``` function from scikit-learn. 
  The parameters are all the default ones from scikit-learn. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data , and test labels into ```scoring()```.

 - ```BCI_sklearn_GaussianNB(data, labels)```  
  This creates a fitted gaussian naive bayes classifier model using the ```GaussianNB()``` function from scikit-learn. 
  The parameters are all the default ones from scikit-learn. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data , and test labels into ```scoring()```.

 - ```BCI_sklearn_MLPClassifier(data, labels)```  
  This creates a fitted multi-layer perceptron classifier model using the ```MLPClassifier()``` function from scikit-learn. 
  The parameters are all the default ones from scikit-learn. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data , and test labels into ```scoring()```.

 - ```BCI_sklearn_LinearDiscriminiantAnalysis(data, labels)```  
  This creates a fitted linear discriminant analysis classifier model using the ```LinearDiscriminantAnalysis()``` function from scikit-learn. 
  The parameters for max_depth, min_samples_split, min_samples_leaf, max_features, splitter, and criterion have been given as 
  we found this to be the best during our optimization. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data, and test labels into ```scoring()```.

 - ```BCI_sklearn_QuadraticDiscriminiantAnalysis(data, labels)```  
  This creates a fitted quadratic discriminant analysis classifier model using the ```QuadraticDiscriminantAnalysis()``` function from scikit-learn. 
  The parameters for max_depth, min_samples_split, min_samples_leaf, max_features, splitter, and criterion have been given as 
  we found this to be the best during our optimization. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data, and test labels into ```scoring()```.

 - ```BCI_pytorch_Net(data, labels)```  

 - ```BCI_tensorflow_Net(data, labels)```
 This creates a four layer neural network using the keras module from tensorflow. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The first layer is and input layer with a shape of (11,). The next three layers are dense layers with 64, 32, and 1 node respectively. The first two dense layers have relu activation and the last layer is sigmoid activation. The model is then compiled with the adam optimizer, binary crossentropy loss, and accuracy for the metric. The model is then trained on the training data with 10 epochs and a batch size of 32 with tensorflow's ```fit()``` function. The model then predicts on the training data to obtain the values predicted by the model from the training set. A for loop then goes through all those values and compares it to the training labels and increases the value of correctPreds by one for each accurate prediction. The training accuracy is then calculated by dividing correctPreds by the total length of the training dataset. The model then predicts on the testing set and a similar process occurs to calculate the test accuracy. It then returns score and the layers as a list with the layers being in the following string: {"Type": "Sequential", "Node 1":"Dense, 64, relu", "Node 2":"Dense, 32, relu", "Node 3":"Dense, 1, sigmoid"}.

 - ```scoring(model, x, y)```  
 This creates four different scores (accuracy, f1 score, precision ,and recall) for the model given. The if statement separates the pytorch model and all other models due to needing to call on different attributes depending on whether it is a scikit-learn model or pytorch model. The model parameter is the model that will be scored, x is the test data set, and y is the test label set. Both parts of the if statement work similarly with having the model first predict on the test data set, then evaluating the four different scores using the builtin functions of either the pytorch module or the scikit-learn module. For f1 score, precision, and recall, the average parameter is given to be macro to calculate the metric for each label and then calculate the unweighted mean. This funciton returns a list of the scores and the model in the following order accuracy, f1 score, precision, recall, model.

- ```snake.py```  
- Class ```Snake```  
  This intializes a ```Snake``` object. 
- Class ```Food```
  Blank
- ```check_collisons(coordinates)```  
  This checks if the snake has collided with the borders of the frame.
  If the snake has, it will return ```True```, otherwise, it will return ```False```.  
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

## Pictures
![headset](https://github.com/stevensryanw/CogniSync/resources/headset.png)
![robot](https://github.com/stevensryanw/CogniSync/resources/robot.png)
![wheelchair](https://github.com/stevensryanw/CogniSync/resources/wheelchair.png)