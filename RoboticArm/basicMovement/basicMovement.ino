#include <Servo.h>

Servo shoulder;
Servo elbow;
Servo wrist1;
Servo wrist2;
Servo hand;
Servo base;

void setup() {
  // put your setup code here, to run once:
  shoulder.attach(11);
  elbow.attach(10);
  wrist1.attach(9);
  wrist2.attach(6);
  hand.attach(5);
  base.attach(3);

  //pickup

   sweep(hand, 90, 160, 30);  
   sweep(wrist2, 90, 160, 30);
   sweep(elbow, 90, 160, 30);
   sweep(shoulder, 90, 15, 30);
   sweep(hand, 160, 0, 30);

  // drop
  
  sweep(shoulder, 15, 90, 30);
  sweep(elbow, 160, 0, 30);
  sweep(wrist2, 160, 90, 30);
  sweep(hand, 0, 160, 30);
}

void loop() {

}

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
