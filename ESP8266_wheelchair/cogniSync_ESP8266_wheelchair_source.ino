
#include <ESP8266WiFi.h>
WiFiClient client;
WiFiServer server(80);

/* WIFI settings */
const char* ssid = "tulane";

/* data received from application */
String  data =""; 

/* define L298N or L293D motor control pins */
int leftMotorForward = 2;     /* GPIO2(D4) -> IN3   */
int rightMotorForward = 15;   /* GPIO15(D8) -> IN1  */
int leftMotorBackward = 0;    /* GPIO0(D3) -> IN4   */
int rightMotorBackward = 13;  /* GPIO13(D7) -> IN2  */


/* define L298N or L293D enable pins */
int rightMotorENB = 14; /* GPIO14(D5) -> Motor-A Enable */
int leftMotorENB = 12;  /* GPIO12(D6) -> Motor-B Enable */

void setup()
{
  /* initialize motor control pins as output */
  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(leftMotorForward, OUTPUT);
  pinMode(rightMotorForward, OUTPUT); 
  pinMode(leftMotorBackward, OUTPUT);  
  pinMode(rightMotorBackward, OUTPUT);

  /* initialize motor enable pins as output */
  pinMode(leftMotorENB, OUTPUT); 
  pinMode(rightMotorENB, OUTPUT);

  /* start server communication */
  Serial.begin(9600);
  delay(2000);
  connectWiFi();
  server.begin();
}

void loop()
{
    /* If the server available, run the "checkClient" function */  
    client = server.available();
    if (!client) return; 
    data = checkClient ();

/************************ Run function according to incoming data from application *************************/

    /* If the incoming data is "forward", run the "MotorForward" function */
    if (data == "forward") MotorForward(client);
    /* If the incoming data is "backward", run the "MotorBackward" function */
    else if (data == "backward") MotorBackward(client);
    /* If the incoming data is "left", run the "TurnLeft" function */
    else if (data == "left") TurnLeft(client);
    /* If the incoming data is "right", run the "TurnRight" function */
    else if (data == "right") TurnRight(client);
    /* If the incoming data is "stop", run the "MotorStop" function */
    else if (data == "stop") MotorStop(client);
} 

/********************************************* FORWARD *****************************************************/
void MotorForward(WiFiClient client)   
{
  digitalWrite(leftMotorENB,HIGH);
  digitalWrite(rightMotorENB,HIGH);
  digitalWrite(leftMotorForward,HIGH);
  digitalWrite(rightMotorForward,LOW);
  digitalWrite(rightMotorBackward,HIGH);
  digitalWrite(leftMotorBackward,LOW);
  client.println("HTTP/1.1 200 OK");
  Serial.println("Foreward");
}

/********************************************* BACKWARD *****************************************************/
void MotorBackward(WiFiClient client)   
{
  digitalWrite(leftMotorENB,HIGH);
  digitalWrite(rightMotorENB,HIGH); 
  digitalWrite(leftMotorForward,LOW);
  digitalWrite(rightMotorForward,HIGH);
  digitalWrite(rightMotorBackward,LOW);
  digitalWrite(leftMotorBackward,HIGH);
  client.println("HTTP/1.1 200 OK");
  Serial.println("Backward");
}

/********************************************* TURN LEFT *****************************************************/
void TurnLeft(WiFiClient client)   
{
  digitalWrite(leftMotorENB,HIGH);
  digitalWrite(rightMotorENB,HIGH);
  digitalWrite(leftMotorBackward,HIGH);
  digitalWrite(rightMotorBackward,HIGH);
  digitalWrite(leftMotorForward,LOW);
  digitalWrite(rightMotorForward,LOW);
  client.println("HTTP/1.1 200 OK");
  Serial.println("Left");
}

/********************************************* TURN RIGHT *****************************************************/
void TurnRight(WiFiClient client)   
{
  digitalWrite(leftMotorENB,HIGH);
  digitalWrite(rightMotorENB,HIGH);
  digitalWrite(leftMotorForward,HIGH);
  digitalWrite(rightMotorForward,HIGH);
  digitalWrite(leftMotorBackward,LOW);
  digitalWrite(rightMotorBackward,LOW);
  client.println("HTTP/1.1 200 OK");
  Serial.println("Right");
}

/********************************************* STOP *****************************************************/
void MotorStop(WiFiClient client)   
{
  digitalWrite(leftMotorENB,LOW);
  digitalWrite(rightMotorENB,LOW);
  digitalWrite(leftMotorForward,LOW);
  digitalWrite(leftMotorBackward,LOW);
  digitalWrite(rightMotorForward,LOW);
  digitalWrite(rightMotorBackward,LOW);
  client.println("HTTP/1.1 200 OK");
  Serial.println("Stop");
}

/********************************** RECEIVE DATA FROM the APP ******************************************/
String checkClient (void)
{
  while(!client.available()) delay(1); 
  String request = client.readStringUntil('\r');
  request.remove(0, 5);
  request.remove(request.length()-9,9);
  return request;
}

void connectWiFi()
{
  Serial.println("Connecting to WIFI");
  WiFi.begin(ssid);
  while ((!(WiFi.status() == WL_CONNECTED)))
  {
    digitalWrite(LED_BUILTIN, HIGH);// turn the LED on (HIGH is the voltage level)
    delay(500);
    Serial.print("..");
    digitalWrite(LED_BUILTIN, LOW);// turn the LED off by making the voltage LOW
    delay(500);
  }
  digitalWrite(LED_BUILTIN, LOW);// turn the LED on (HIGH is the voltage level)
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("NodeMCU Local IP is : ");
  Serial.print((WiFi.localIP()));
}
