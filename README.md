![Untitled_Artwork](https://github.com/stevensryanw/CogniSync/assets/70183326/88a7294b-9978-4d16-b423-b14074d80ce6)
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
Intializes the home page of the GUI with the needed buttons for all pages plotEEG, UserRecording, Modeling, SnakeGame, and USBOutput. When buttons are clicked they call.
  - ```show_frame(self, cont)```  
Takes a frame and raises it to the top making it visible to the user
    
### Class ```PlotEEG()```  
  - ```__init__(self, parent, controller)```  
This creates all the widgets for the PlotEEG page and creates a default range for the sliders between 0 and 1,000,000.
  - ```updateList(self)```  
This goes to the data folder and updates the list of files that are present in that folder while excluding any folders and .DS_Store. The data and label dropdown are then updated with the new list. 
  - ```slide1(self, value)```  
This creates failsafes for the first slider to not be above the value set by the second slider. It also prevents the range from being significantly less than the second slider value. The text for the sliders will update when the slider is moved as well with this function running every time slider oen is moved.
  - ```slide2(self, value)```  
This creates failsafes for the second slider to not be below the value set by the second slider. It also prevents the range from being significantly less than the second slider value. The text for the sliders will update when the slider is moved as well with this function running every time slider one is moved.
  - ```plot_eeg(self)```  
This function plots the selected data in a web browser using the plotly package. The data file chosen is read using ```pandas.read_csv()``` and the unique labels are taken using ```.unique()``` as well as removing any rows with NA values. Colors are then assigned to each column and the interval is taken from the values the sliders were placed at. The minimum and maximum values are taken from the data with ```min()``` and ```max()``` and the labels are assigned colors. Each column is then individually graphed using ```fig.add_trace(go.Scatter())``` and dashed vertical lines are added to the graph whenever a new movement occurs in the data. The columns graphed change based on what the user has selected. 

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
If is_prompting is true throw text "Rest for 10 seconds' and clear the canvas. Close the temp_val.txt file. Increment the prompt_count by 1 and set the current movement index to the next slot. if the current movement index is 0 shuffle the movements using ```shuffle_movements(self)```. After the 10 second rest time prompt the next movement using ```prompt_next_movement(self)```.
  - ```start_record(self)```  
This function checks for a record thread then creates one.
  - ```stop_record(self)```  
This function stops the record thread.
  - ```record_data(self)```  
This function calls ```record()``` from connect.py.

### Class ```Modeling()```  
  - ```__init__(self, parent, controller)```  
This creates all the widgets for the model page including dropdowns for selecting the model, data file and label file. The widgets for the checkbox also have an IntVar created to help determine whether it has been clicked or not. 
  - ```model_input(self)```  
This function runs the model and returns the results and fitted model and is activated by pressing the run button. The data file, label file chosen, model selected, and output file selected are all stored using the tkinter ```get()``` function. The following if statement determines which model was selectetd and creates text on the gui based on which one is chosen. The data file and label file selected are sent through ```csvProcessing()``` and the results stored. The processed numpy arrays for data and labels are then sent to the appropriate function in ```model_bci.py``` and the return stored in a variable called results. The fitted model is then saved based on whether it is a tensorflow, pytorch, or scikit-learn model. If  it is tensorflow, a text file is created with the information about the layers of the neural network. The pytorch model is saved using the ```torch.save()``` function in a .pt file and scikit-learn models are saved using the ```joblib.dump()``` in a .pkl file. The name for the output file is either the given output file name or creating the name using the model name, data file name, and specific time to create a unique id for the specific fitted model. The model name results and label mapping are added to a csv file to reference later.
  - ```updateFiles(self)```  
This goes to the data folder and updates the list of files that are present in that folder while excluding any folders and .DS_Store. The data and label dropdown are then updated with the new list. 
  - ```csvProcessing(self, dataFile, labelFile)```  
This function is to process the csv file chosen by the user in the gui. The dataFile parameter is a string of the file chosen by the user which is then found by going to the data folder and searching for the file there. The labelFile parameter is the same as the dataFile parameter except for label files chosen by the user or that there is no label file. The if statement splits based on whether a label file has been chosen or not. If no label file was chosen then the path to the data file is created and passed to ```pandas.read_csv``` and stored. All rows with NA values are dropped with the label column being stored as a separate dataframe and deleted from the data dataframe. The unique values in the labels frame are taken and sorted in a list by alphabetical order and replaced with numbers unique to each different label value. The else statement follows this format but reads in both the data file and label file given. If the checkbox for the alpha values has been unchecked then the alpha value columns are dropped and if the electrode reading checkbox is unchecked then the electrode reading columns are removed. The dataframes are then turned into numpy arrays and will return a list of the data numpy array, label numpy array, and a dictionary of the label values and corresponding number. 

### Class ```SnakeGame()```  
  - ```__init__(self, parent, controller)```  
Intializes the home page of the GUI with the needed buttons for all pages plotEEG, UserRecording, Modeling, SnakeGame, and USBOutput. When buttons are clicked they call ```show_frame(self, cont)``` to move that frame to the top.
  - ```updateFiles(self)```  
This goes to the data folder and updates the list of files that are present in that folder while excluding any folders and .DS_Store. The data dropdown are then updated with the new list. 
  - ```modelSelection(self)```  
This gets the model the user selected and unpackages it according to what file type it is.
  - ```start_record(self)```  
This function checks for a record thread then creates one.
  - ```stop_record(self)```  
This function stops the record thread.
  - ```record_data(self)```
This function calls ```record()``` from connect.py.
  - ```start_predictions(self)```  
This function reads in the recording data, then it selects the latest full row of data and uses the selected model to write a prediction to ```tempPred.txt```.
  - ```start_prediction_thread(self)```  
This function checks for a prediction thread then creates one.
  - ```stop_predictions(self)```   
This stops the prediction thread.
  - ```predict_stream(self)```   
This function turns the predictions in the temporary prediction txt file ```tempPred.txt``` and sends key presses to the snake game.
  - ```start_stream_thread(self)```   
This function checks for a stream thread then creates one.
  - ```stop_stream(self)```   
This functions stops the stream thread.
  - ```drawFrame(self)```  
This function is activated by the snake begin function and a canvas to place the snake game is placed in the gui and the keys are bound as well. 
  - ```move(self, direction, snake, g_food, root, canvas)```  
This is activated when a bound key is pressed activating ```change_direction()``` and ```next_turn()```.
  - ```game_over(self)```  
This creates a gameover screen on the canvas.
  - ```change_direction(self, new_direction)```  
This changes the direction variable to either left right up or down depending on what key was pressed.
  - ```check_collisions(self, coordinates)```  
This checks if the snake is past the boundary returning True if it is or False if not.
  - ```next_turn(self, snake, food, root, canvas)```  
This updates the coordinates of the snake while ensuring it has not collided with anything. If it has not collided with anything then it will update the location of the snake on the canvas. This function also checks if the snake is on the same square as the food and if it is then it will delete the previous food and generate a new one in a random location and increase the point value by one.

### Class ```USBOutput()```
  - ```__init__(self, parent, controller)```  
Intializes the home page of the GUI with the needed buttons for all pages plotEEG, UserRecording, Modeling, SnakeGame, and USBOutput. When buttons are clicked they call ```show_frame(self, cont)``` to move that frame to the top.
  - ```updateFiles(self)```  
This goes to the data folder and updates the list of files that are present in that folder while excluding any folders and .DS_Store. The data dropdown are then updated with the new list. 
  - ```modelSelection(self)```  
This gets the model the user selected and unpackages it according to what file type it is.
  - ```start_record(self)```  
This function checks for a record thread then creates one.
  - ```stop_record(self)```  
This function stops the record thread.
  - ```record_data(self)```
This function calls ```record()``` from connect.py.
  - ```start_predictions(self)```  
This function reads in the recording data, then it selects the latest full row of data and uses the selected model to write a prediction to ```tempPred.txt```.
  - ```start_prediction_thread(self)```  
This function checks for a prediction thread then creates one.
  - ```stop_predictions(self)```   
This stops the prediction thread.
  - ```predict_stream(self)```   
This function turns the predictions in the temporary prediction txt file ```tempPred.txt``` and sends commands to the robotic wheelchair URL.
  - ```start_stream_thread(self)```   
This function checks for a stream thread then creates one.
  - ```stop_stream(self)```   
This functions stops the stream thread.

## ```connect.py```
  - ```record(self)```  
This function uses the pyOpenBCI and pylsl to output all data streamed to a csv, this function is always run on a separate thread to the GUI. This function will also look for a label from tempVal.txt to write to append to the data. We have chosen to use the recomended filtering process from the pyOpenBCI GitHub page.

## ```model_bci.py```
  - ```BCI_sklearn_SVC(data, labels)```  
This creates a fitted support vector machine bagging classifier model using the ```BaggingClassifier()``` function from scikit-learn. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. None of the parameters have been specified except for n_jobs which is set to -1. This allows the entire CPU and memory to be used to fit the model. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data, and test labels into ```scoring()```. It is heavily recommended that SVC only uses small datasets as it will take a long time to fit otherwise.
 - ```BCI_sklearn_RandomForestClassifier(data, labels)```  
This creates a fitted random forest classifier model using the ```RandomForestCLassifier()``` function from scikit-learn. The parameters for max_depth, min_samples_split, min_samples_leaf, criterion, n_estimators, max_features, and bootstrap have been given as we found this to be the best during our optimization. The n_jobs parameter has been set to -1 which allows the entire CPU and memory to be used to fit the model. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. This allows the entire CPU and memory to be used to fit the model. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data, and test labels into ```scoring()```.
 - ```BCI_sklearn_DecisionTreeClassifier(data, labels)```  
This creates a fitted decision tree classifier model using the ```DecisionTreeCLassifier()``` function from scikit-learn. The parameters for max_depth, min_samples_split, min_samples_leaf, max_features, splitter, and criterion have been given as we found this to be the best during our optimization. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data, and test labels into ```scoring()```.
 - ```BCI_sklearn_LogisticRegression(data, labels)```   
This creates a fitted logistic regression model using the ```LogisticRegression()``` function from scikit-learn. The parameters for C, class_weight, dual, fit_intercept, intercept_scaling, l1_ratio, max_iter, multi_class, penalty, random_state, solver, tol, verbose, and warm_start have been given as we found this to be the best during our optimization. The n_jobs parameter has been set to -1 which allows the entire CPU and memory to be used to fit the model. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data, and test labels into ```scoring()```.
 - ```BCI_sklearn_GradientBoostingClassifier(data, labels)```   
This creates a fitted gradient boosting classifier model using the ```GradientBoostingClassifier()``` function from scikit-learn. The parameters are all the default ones from scikit-learn. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data , and test labels into ```scoring()```.
 - ```BCI_sklearn_KNeighborsClassifier(data, labels)```   
This creates a fitted k nearest neighbors classifier model using the ```KNeighborsClassifier()``` function from scikit-learn. The parameters are all the default ones from scikit-learn. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data , and test labels into ```scoring()```.
 - ```BCI_sklearn_GaussianNB(data, labels)```   
This creates a fitted gaussian naive bayes classifier model using the ```GaussianNB()``` function from scikit-learn. The parameters are all the default ones from scikit-learn. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data , and test labels into ```scoring()```.
 - ```BCI_sklearn_MLPClassifier(data, labels)```   
This creates a fitted multi-layer perceptron classifier model using the ```MLPClassifier()``` function from scikit-learn. The parameters are all the default ones from scikit-learn. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data , and test labels into ```scoring()```.
 - ```BCI_sklearn_LinearDiscriminiantAnalysis(data, labels)```  
This creates a fitted linear discriminant analysis classifier model using the ```LinearDiscriminantAnalysis()``` function from scikit-learn. The parameters for max_depth, min_samples_split, min_samples_leaf, max_features, splitter, and criterion have been given as we found this to be the best during our optimization. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data, and test labels into ```scoring()```.
 - ```BCI_sklearn_QuadraticDiscriminiantAnalysis(data, labels)```  
This creates a fitted quadratic discriminant analysis classifier model using the ```QuadraticDiscriminantAnalysis()``` function from scikit-learn. The parameters for max_depth, min_samples_split, min_samples_leaf, max_features, splitter, and criterion have been given as we found this to be the best during our optimization. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The labels are also split at the same time as data conserving which labels are for which data groupings. The model is then trained on the training data set and training label set using scikit-learn's built in ```fit()``` function. This function returns the result of passing the model, test data, and test labels into ```scoring()```.
 - ```BCI_pytorch_Net(data, labels)```  
This function trains a PyTorch neural network model for Brain-Computer Interface (BCI) classification tasks, taking input data samples and corresponding labels as arguments. This function first selects the appropriate device for computation, either CUDA or CPU, based on availability. It then defines model parameters such as batch size, dropout rates, and learning rate, and prepares the input data by converting it into PyTorch tensors and splitting it into training and testing sets. The model architecture consists of multiple linear layers with ReLU activation functions and dropout regularization, followed by an output layer. Training is conducted using the Adam optimizer, with backpropagation applied over multiple epochs to minimize the defined loss function. Finally, the trained model's performance is evaluated on the test data, providing insights into its classification accuracy.
 - ```BCI_tensorflow_Net(data, labels)```  
This creates a four layer neural network using the keras module from tensorflow. The data argument takes in a numpy array of the data that will be split into a training set and a testing set in an 80/20 split using ```train_test_split()``` from scikit-learn. The data can be of any size as long as it is all numerical data since scikit-learn cannot handle nonnumerical information. The labels argument takes in a numpy array that categorizes each grouping of the data and must be numerical necessitating any strings to be converted beforehand. The first layer is and input layer with a shape of (11,). The next three layers are dense layers with 64, 32, and 1 node respectively. The first two dense layers have relu activation and the last layer is sigmoid activation. The model is then compiled with the adam optimizer, binary crossentropy loss, and accuracy for the metric. The model is then trained on the training data with 10 epochs and a batch size of 32 with tensorflow's ```fit()``` function. The model then predicts on the training data to obtain the values predicted by the model from the training set. A for loop then goes through all those values and compares it to the training labels and increases the value of correctPreds by one for each accurate prediction. The training accuracy is then calculated by dividing correctPreds by the total length of the training dataset. The model then predicts on the testing set and a similar process occurs to calculate the test accuracy. It then returns score and the layers as a list with the layers being in the following string: {"Type": "Sequential", "Node 1":"Dense, 64, relu", "Node 2":"Dense, 32, relu", "Node 3":"Dense, 1, sigmoid"}.
 - ```scoring(model, x, y)```  
 This creates four different scores (accuracy, f1 score, precision ,and recall) for the model given. The if statement separates the pytorch model and all other models due to needing to call on different attributes depending on whether it is a scikit-learn model or pytorch model. The model parameter is the model that will be scored, x is the test data set, and y is the test label set. Both parts of the if statement work similarly with having the model first predict on the test data set, then evaluating the four different scores using the builtin functions of either the pytorch module or the scikit-learn module. For f1 score, precision, and recall, the average parameter is given to be macro to calculate the metric for each label and then calculate the unweighted mean. This funciton returns a list of the scores and the model in the following order accuracy, f1 score, precision, recall, model.

## ```snake.py```   
- Class ```Snake```   
This intializes a ```Snake``` object.  
It uses ```canvas.create_rectangle()``` from ```CustomTKinter``` to create the body of the snake and saves the coordinates of the body.  
- Class ```Food```  
This intializes a ```Food``` object.  
It uses ```canvas.create_oval()``` from ```CustomTKinter``` to create the food pellet and saves the coordinates that are intialized with the ```random``` library.   
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

## Resources
# [Capstone Expo Poster](https://github.com/stevensryanw/CogniSync/files/15071372/Capstone.Expo.Poster.CogniSync.pdf)
# [Robotic Wheelchair Budget](https://github.com/stevensryanw/CogniSync/files/15071427/WheelchairBudgetCMPSCapstone.2487.xlsx)
![headset](https://github.com/stevensryanw/CogniSync/assets/70183326/523c1250-2b44-4989-b77d-76bedbf5e4f0)
![robot](https://github.com/stevensryanw/CogniSync/assets/70183326/c2f38436-cbee-4c8f-b313-e1bc45310c0b)
![wheelchair](https://github.com/stevensryanw/CogniSync/assets/70183326/aeb4c9a1-7382-4e1c-840a-5f28a13c301f)
