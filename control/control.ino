#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVO_MIN 100  
#define SERVO_MAX 580

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup(){
  pwm.begin();   
  Serial.begin(9600);           
  pwm.setPWMFreq(50);       
}

void loop(){
  if (Serial.available()) {
    char received = Serial.read();
    if (received == '1') {
      Serial.println("Arduino received '1'");
    }
  }

}

void calculate_angle(int channel, int angle){
  int pulselength = map(angle, 0, 180, SERVO_MIN, SERVO_MAX);
  pwm.setPWM(channel, 0, pulselength);

}