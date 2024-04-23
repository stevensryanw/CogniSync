![Untitled_Artwork](https://github.com/stevensryanw/CogniSync/assets/70183326/88a7294b-9978-4d16-b423-b14074d80ce6)

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
