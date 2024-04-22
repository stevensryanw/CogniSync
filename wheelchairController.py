import urllib.request #defines function and_ classes which help in opening urls

#url handling module for python
root_url = "http://10.129.110.181"

def sendRequest(url):
	n = urllib.request.urlopen(url) # send request to ESP

def motorForward():
    #print("Moving forward")
    sendRequest(root_url + "/forward")
    
def motorBackward():
    #print("Moving backward")
    sendRequest(root_url + "/backward")

def turnLeft():
    #print("Turning Left")
    sendRequest(root_url + "/left")

def turnRight():
    #print("Turning Right")
    sendRequest(root_url + "/right")

def motorStop():
    print("Stopping")
    sendRequest(root_url + "/stop")