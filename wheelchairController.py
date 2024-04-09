import urllib.request #defines function and_ classes which help in opening urls

#url handling module for python
root_url = "http://10.129.25.225"

def sendRequest(url):
	n = urllib.request.urlopen(url) # send request to ESP

def motorForward():
    print("Moving forward")
    sendRequest(root_url + "/forward")
    

def motorBackward():
    sendRequest(root_url + "/backward")
    print("Moving backward")

def turnLeft():
    sendRequest(root_url + "/left")
    print("Turning Left")

def turnRight():
    sendRequest(root_url + "/right")
    print("Turning Right")

def motorStop():
     sendRequest(root_url + "/stop")
     print("Stopping")