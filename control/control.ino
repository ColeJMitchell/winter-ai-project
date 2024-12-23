#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVO_MIN 100  
#define SERVO_MAX 580

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup(){
  pwm.begin();              
  pwm.setPWMFreq(50);       
}

void loop(){
  
 
  pwm.setPWM(1, 0, SERVO_MIN); 
  delay(1000);
  pwm.setPWM(1, 0, SERVO_MAX);
  delay(1000);

}

void calculate_angle()