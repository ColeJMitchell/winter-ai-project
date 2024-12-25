#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVO_MIN 100  
#define SERVO_MAX 580

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup(){
  pwm.begin();   
  Serial.begin(250000);           
  pwm.setPWMFreq(50);       
}

void loop(){
  
  if (Serial.available()) {
    String connection = Serial.readStringUntil('\n');  
    
    int hyphenIndex = connection.indexOf('-');
    if (hyphenIndex != -1) {  
      int channel = connection.substring(0, hyphenIndex).toInt();
      int angle = connection.substring(hyphenIndex + 1).toInt();
      calculate_angle(channel, angle);
      }
  }
    

}

void calculate_angle(int channel, int angle){
  int pulselength = map(angle, 0, 180, SERVO_MIN, SERVO_MAX);
  pwm.setPWM(channel, 0, pulselength);

}