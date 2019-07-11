// add Servo library 
#include <Servo.h>

// create variables to store data from RPI
int numBlink = 0;
int distance = 0;
int material = 0;
int angle = 90;

// create variables to store servo posistions
int shoulderPos = 90;
int elbowPos = 90;
int wrist1Pos = 90;
int wrist2Pos = 90;
int handPos = 90;
int basePos = 90;

// create Servo objects to control servos
Servo shoulder;
Servo elbow;
Servo wrist1;
Servo wrist2;
Servo hand;
Servo base;

// create flash function (will flash Arduino LED by the number you input)
void flash(int n){
  for (int i = 0; i < n; i++){
    digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
  }
}

void setup() {
  // begin serial communication with RPI and send default string to RPI to confirm connection
  Serial.begin(9600);
  Serial.println("Connected to Arduino");

  // assign Arduino LED to pin 13
  pinMode(13, OUTPUT);

  // attach servo objects to correct pin number
  shoulder.attach(11);
  elbow.attach(10);
  wrist1.attach(9);
  wrist2.attach(6);
  hand.attach(5);
  base.attach(3);

  // move arm to home position to face camera down 
  homeState();
}

void loop() {
  // send default string to RPI to confirm connection
  Serial.println("Connected to Arduino");

  // if the RPI sends a signal to Arduino
  if(Serial.available()){
    // change values of variables to what the RPI sends
    numBlink = Serial.parseInt();
    material = Serial.parseInt();
    distance = Serial.parseInt();
    angle = Serial.parseInt();
    
    // flash LED and move the arm to pick and drop the object based on its material 
    flash(numBlink);
    pickUp();
    dropOff();

    // go back to home state
    homeState();

    // send string to let RPI know that the arm is done moving
    Serial.println("Done Moving");
    Serial.flush();
  }
  delay(1000);
}

/*
 * sweep function to make servos move slowly!
 * 
 * input the servo object, the current servo angle, the angle you 
 * want the servo to move to, and the speed at which you want to turn 
 * the servo. Bigger number ==> slower speed. Smaller number ==> faster speed.
 */
void sweep(Servo servo,int oldPos, int newPos, int servoSpeed){
  if (oldPos <= newPos){
    for (oldPos; oldPos <= newPos; oldPos += 1){
      servo.write(oldPos);
      delay(servoSpeed);
   }
  }

  else if (oldPos >= newPos){
    for (oldPos; oldPos >= newPos; oldPos -= 1){
      servo.write(oldPos);
      delay(servoSpeed);
    }
  }
}

// pickUp function that will move robotic arm to specified distance and angle sent from RPI
void pickUp(){
  if (distance == 1){
    sweep(base, basePos, angle, 30);
    basePos = angle;
    sweep(hand, handPos, 160, 30);
    handPos = 160;  
    sweep(wrist2, wrist2Pos, 35, 30);
    wrist2Pos = 35;
    sweep(elbow, elbowPos, 180, 30);
    elbowPos = 180;
    sweep(shoulder, shoulderPos, 65, 30);
    shoulderPos = 65;
    sweep(hand, handPos, 45, 30);
    handPos = 45;
    distance = 0;
  }
 else if (distance == 2){
   sweep(base, basePos, angle, 30);
   basePos = angle;
   sweep(hand, handPos, 160, 30);
   handPos = 160;  
   sweep(wrist2, wrist2Pos, 32, 30);
   wrist2Pos = 32;
   sweep(elbow, elbowPos, 165, 30);
   elbowPos = 165;
   sweep(shoulder, shoulderPos, 55, 30);
   shoulderPos = 55;
   sweep(hand, handPos, 45, 30);
   handPos = 45;
   distance = 0;
 }
 else if (distance == 3){
  sweep(base, basePos, angle, 30);
  basePos = angle;
  sweep(hand, handPos, 160, 30);
  handPos = 160;
  sweep(wrist2, wrist2Pos, 32, 30);
  wrist2Pos = 32;
  sweep(elbow, elbowPos, 150, 30);
  elbowPos = 150;
  sweep(shoulder, shoulderPos, 45, 30);
  shoulderPos = 45;
  sweep(hand, handPos, 45, 30);
  handPos = 45;
  distance = 0;
 }
}

// dropOff function that will drop off the object to a location based off its material
void dropOff(){
  if (material == 1){
   sweep(shoulder, shoulderPos, 90, 30);
   shoulderPos = 90;
   sweep(elbow, elbowPos, 0, 30);
   elbowPos = 0;
   sweep(wrist2, wrist2Pos, 90, 30);
   wrist2Pos = 90;
   sweep(base, basePos, 0, 30);
   basePos = 0;
   sweep(hand, handPos, 160, 30);
   handPos = 160;
   material = 0;
  }

  else if (material == 2){
   sweep(shoulder, shoulderPos, 90, 30);
   shoulderPos = 90;
   sweep(elbow, elbowPos, 0, 30);
   elbowPos = 0;
   sweep(wrist2, wrist2Pos, 90, 30);
   wrist2Pos = 90;
   sweep(base, basePos, 45, 30);
   basePos = 45;
   sweep(hand, handPos, 160, 30);
   handPos = 160;
   material = 0;
  }

  else if (material == 3){
   sweep(shoulder, shoulderPos, 90, 30);
   shoulderPos = 90;
   sweep(elbow, elbowPos, 0, 30);
   elbowPos = 0;
   sweep(wrist2, wrist2Pos, 90, 30);
   wrist2Pos = 90;
   sweep(base, basePos, 90, 30);
   basePos = 90;
   sweep(hand, handPos, 160, 30);
   handPos = 160;
   material = 0;
  }

  else if (material == 4){
   sweep(shoulder, shoulderPos, 90, 30);
   shoulderPos = 90;
   sweep(elbow, elbowPos, 0, 30);
   elbowPos = 0;
   sweep(wrist2, wrist2Pos, 90, 30);
   wrist2Pos = 90;
   sweep(base, basePos, 135, 30);
   basePos = 135;
   sweep(hand, handPos, 160, 30);
   handPos = 160;
   material = 0;
  }

  else if (material == 5){
   sweep(shoulder, shoulderPos, 90, 30);
   shoulderPos = 90;
   sweep(elbow, elbowPos, 0, 30);
   elbowPos = 0;
   sweep(wrist2, wrist2Pos, 90, 30);
   wrist2Pos = 90;
   sweep(base, basePos, 180, 30);
   basePos = 180;
   sweep(hand, handPos, 160, 30);
   handPos = 160;
   material = 0;
  }
}

// homeState function that will hold the camera facing down to perform obejct detection
void homeState(){
  sweep(base, basePos, 90, 30);
  basePos = 90;
  sweep(wrist2, wrist2Pos, 60, 30);
  wrist2Pos = 60;
  sweep(elbow, elbowPos, 110, 30);
  elbowPos = 110;
  sweep(shoulder, shoulderPos, 65, 30);
  shoulderPos = 65;
  sweep(hand, handPos, 90, 30);
  handPos = 90;
}
