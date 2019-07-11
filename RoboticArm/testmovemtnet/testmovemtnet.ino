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

//  sweep(base, 90, 90, 30);
//  sweep(hand, 90, 50, 30);
//  sweep(wrist2, 90, 32, 30);
//  sweep(elbow, 90, 165, 30);
//  sweep(shoulder, 90, 55, 30);
//  sweep(base, 90, 0, 50);
//  sweep(base, 0, 180, 50);
//  sweep(base, 180, 0, 50);

//   sweep(hand, 90, 50, 30);  
//   sweep(wrist2, 90, 35, 30);
//   sweep(elbow, 90, 180, 30);
//   sweep(shoulder, 90, 65, 30);
//   sweep(base, 90, 0, 50);
//   sweep(base, 0, 180, 50);
//   sweep(base, 180, 0, 50);

  sweep(base, 90, 90, 30);
  sweep(hand, 90, 45, 30);
//  sweep(wrist2, 90, 32, 30);
//  sweep(elbow, 90, 150, 30);
//  sweep(shoulder, 90, 45, 30);
//  sweep(base, 90, 180, 50);
//  sweep(base, 180, 0, 50);
//  sweep(base, 0, 180, 50);

  //home
//  sweep(base, 90, 90, 30);
//  sweep(wrist2, 90, 60, 30);
//  sweep(elbow, 90, 110, 30);
//  sweep(shoulder, 90, 65, 30);

//  //middle
//
//   sweep(hand, 90, 160, 30);  
//   sweep(wrist2, 90, 160, 30);
//   sweep(elbow, 90, 160, 30);
//   sweep(shoulder, 90, 15, 30);
//   sweep(hand, 160, 0, 30);
//
//  // drop
//
//  sweep(base, 90, 90, 30);
//  sweep(shoulder, 15, 90, 30);
//  sweep(elbow, 160, 0, 30);
//  sweep(wrist2, 160, 90, 30);
//  sweep(hand, 0, 160, 30);
  

   //close
//   sweep(hand, 90, 160, 30);  
//   sweep(wrist2, 90, 170, 30);
//   sweep(elbow, 90, 180, 30);
//   sweep(shoulder, 90, 22, 30);
//   sweep(hand, 160, 0, 30);



  //far
//   sweep(hand, 90, 160, 30);
//   sweep(wrist2, 90, 140, 30);
//   sweep(elbow, 90, 120, 30);
//   sweep(shoulder, 90, 0, 30);
//   sweep(hand, 160, 70, 30);
//   sweep(shoulder, 0, 90, 30);
//   sweep(elbow, 120, 0, 30);
//   sweep(wrist2, 140, 90, 30);
//   sweep(hand, 70, 160, 30);
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

void pickUp(){
  
}
  
