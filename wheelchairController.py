#------------------ Importing Libraries -----------------
'''URL hnadling'''
import urllib.request
#------------------ Importing Libraries -----------------

#------------------ Variable Initializations ------------
#defines the local IP address for the ESP controller
#(needs to be defined for each ESP and may change with differing networks)
root_url = "http://10.129.110.181"
#------------------ Variable Initializations ------------

#------------------ URL Request Function ----------------
def sendRequest(url):
    """
    Sends a request to the specified URL.
    
    Parameters:
        url (str): The URL to send the request to.

    Returns:
        None
    """
    n = urllib.request.urlopen(url) #send request to ESP
#------------------ URL Request Function ----------------

#------------------ Motor Control Functions -------------
def motorForward():
    """
    Moves the motor forward by sending a request to the ESP via IP.
    """
    #sends "forward" keyword to ESP via IP
    #print("Moving forward")
    sendRequest(root_url + "/forward")
    
def motorBackward():
    """
    Moves the motor backward by sending a "backward" keyword to the ESP via IP.
    """
    #sends "backward" keyword to ESP via IP
    #print("Moving backward") #confirms function execution
    sendRequest(root_url + "/backward")

def turnLeft():
    """
    Turns the motor left by sending a "left" keyword to the ESP via IP.
    """
    #sends "left" keyword to ESP via IP
    #print("Turning Left") #confirms fucntion execution
    sendRequest(root_url + "/left")

def turnRight():
    """
    Turns the motor right by sending a "right" keyword to the ESP via IP.
    """
    #sends "right" keyword to ESP via IP
    #print("Turning Right") #confirms fucntion execution
    sendRequest(root_url + "/right")

def motorStop():
    """
    Stops the motor by sending a "stop" keyword to the ESP via IP.
    """
    #sends "stop" keyword to ESP via IP
    #print("Stopping") #confirms fucntion execution
    sendRequest(root_url + "/stop")
#------------------ Motor Control Functions -------------