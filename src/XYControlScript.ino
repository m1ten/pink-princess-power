#include <Stepper.h>
#include <Servo.h>
using namespace std;


const double stepsPerRevolution = 2052;
int rotate = 0;
const int gear_ratio = 4;
int desired_horiAngle= -30;
int desired_vertAngle = 45;
int HorStepsReq = ((stepsPerRevolution / 360.00)*desired_horiAngle) * gear_ratio;
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);
Servo myServo = Servo();

//73 degrees is completely vertical launch tube. This means that the launcher rests at 17 degrees
//All degree measurements must be adjusted by 17 to ensure accuracy.
//This extra movement of 17 degrees is due to an error in build quality. This will be fixed in integration.
//Vertical: 73, 45-degree: 28
int view_angle = 28;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  myStepper.setSpeed(15);

  //Test Case 1 
  myServo.attach(3);
  if (myServo.attached()){
    myServo.write(view_angle);
  }

  //delay(6000);
  /*if (myServo.attached()){
    myServo.write(0);
  }*/

  //delay(1000);
  //Test Case 2
  myStepper.step(HorStepsReq);
  delay(1000);
  //myStepper.step(-HorStepsReq);

  //Test Case 3
  myStepper.step(HorStepsReq);
  delay(2000);
  myStepper.step(-HorStepsReq *2);
  delay(2000);
  myStepper.step(HorStepsReq);
  
}

void loop() {
  //No looping code
}



