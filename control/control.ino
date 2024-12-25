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

void loop() {
    if (Serial.available()) {
        String connection = Serial.readStringUntil('\n');  
        int currIndex = 0;
        while (currIndex < connection.length()) {

            int hyphenIndex = connection.indexOf('-', currIndex);
            if (hyphenIndex == -1) {
                break; 
            }

            int pipeIndex = connection.indexOf('|', currIndex);
            if (pipeIndex == -1) {
                pipeIndex = connection.length(); 
            }

            int channel = connection.substring(currIndex, hyphenIndex).toInt();
            int angle = connection.substring(hyphenIndex + 1, pipeIndex).toInt();
            calculate_angle(channel, angle);

            currIndex = pipeIndex + 1;
        }
    }
}


void calculate_angle(int channel, int angle){
  int pulselength = map(angle, 0, 180, SERVO_MIN, SERVO_MAX);
  pwm.setPWM(channel, 0, pulselength);
}