import urllib.request #url handling module for python

# defines the local IP address for the ESP controller
# (needs to be defined for each ESP and may change with differing networks)
root_url = "http://10.129.110.181"

def sendRequest(url):
	n = urllib.request.urlopen(url) # send request to ESP

def motorForward():
    # sends "foreward" keyword to ESP via IP
    #print("Moving forward")
    sendRequest(root_url + "/forward")
    
def motorBackward():
    # sends "backward" keyword to ESP via IP
    #print("Moving backward") # confirms fucntion execution
    sendRequest(root_url + "/backward")

def turnLeft():
    # sends "left" keyword to ESP via IP
    #print("Turning Left") # confirms fucntion execution
    sendRequest(root_url + "/left")

def turnRight():
    # sends "right" keyword to ESP via IP
    #print("Turning Right") # confirms fucntion execution
    sendRequest(root_url + "/right")

def motorStop():
    # sends "stop" keyword to ESP via IP
    # print("Stopping") # confirms fucntion execution
    sendRequest(root_url + "/stop")