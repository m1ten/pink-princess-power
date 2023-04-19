#include <SD.h>

#include <Stepper.h>
#include <Servo.h>
#include <Arduino_JSON.h>
#include <SD.h>
using namespace std;

const double stepsPerRevolution = 2052;
int rotate = 0;
const int gear_ratio = 4;
// from vision system
int desired_horiAngle= 14;
int desired_vertAngle = 45;
int HorStepsReq = ((stepsPerRevolution / 360.00)*desired_horiAngle) * gear_ratio;
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);
Stepper myStepper2(stepsPerRevolution, 5, 7, 6, 4);
Servo myServo = Servo();

//73 degrees is completely vertical launch tube. This means that the launcher rests at 17 degrees
//All degree measurements must be adjusted by 17 to ensure accuracy.
//This extra movement of 17 degrees is due to an error in build quality. This will be fixed in integration.
//Vertical: 73, 45-degree: 28
int view_angle = 28;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) continue;

  // open the file
  // File file = SD.open("img_details.json");
  // while (!file) { 
  //   // wait until file is created 
  //   Serial.println("File not found");
  //   file = SD.open("img_details.json");
  // }

  // read from the file until there's nothing else in it:
  // while (file.available()) {
  //   // read the file
  //   String data = file.readString();
  //   JSONVar doc = JSON.parse(data);
  //   // get the values
  //   desired_horiAngle = doc["angle"];
  //   Serial.println(desired_horiAngle);
  // }

  myStepper.setSpeed(15);
  myStepper2.setSpeed(15);

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
  
  delay(10000);

  myStepper2.step(stepsPerRevolution * 5);

  delay(2000);

  myStepper.step(-HorStepsReq);

  myServo.write(15);

}

void loop() {
  //No looping code
}



