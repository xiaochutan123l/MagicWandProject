/*
  Accelerometer_DataCollection.ino

  This code reads data from the Arduino Nano 33 BLE Sense's built-in 
  accelerometer and outputs it to Arduino's serial monitor. It cycles 
  through reading and displaying data for slightly less than 3 seconds,
  and delaying for exactly three seconds. It begins each new cycle of
  readings with spacing and the following characters "-,-,-" to 
  distinguish between the data points. This is the same format that
  the training code takes the data, so the output of the serial monitor
  can be copied directly into plaintext files to be read into the code 
  that trains the model.

  Much of this code, including the general stucture was taken from the 
  following source: 
  Nano33BLESensorExample_accelerometer.ino
  Copyright (c) 2020 Dale Giancono. All rights reserved..

  Other portions of this code were taken from Daniel Hertz from the 
  following article:
  https://maker.pro/arduino/tutorial/how-to-use-the-arduino-nano-33-bles
  -built-in-imu
*/

/*Include Header Files*/
#include "Arduino.h"
//#include "Nano33BLEAccelerometer.h"
#include <Arduino_LSM9DS1.h>


/*Global Variables*/
//a counter to limit the number of cycles where values are displayed
int counter = 0; 
int episode = 0;
int moveLength = 128;

/*Setup Function*/
void setup()
{
  // Serial monitor setup
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  Serial.println("-,-,-");    
}


/*Main loop*/
void loop()
{          
  // Initialize Variables
  float ax, ay, az, gx, gy, gz = 0.05;

  // Check if the accelerometer is ready and if the loop has only
  //   been run less than 200 times (=~3 seconds displayed) 
  if (IMU.accelerationAvailable() and counter < moveLength and IMU.gyroscopeAvailable())
  {
    // Read the accelerometer
    IMU.readAcceleration(ax, ay, az);
    IMU.readGyroscope(gx, gy, gz);
    // Scale up the values to better distinguish movements
    ax = (int) (ax*100);
    ay = (int) (ay*100);
    az = (int) (az*100);
    gx = (int) (gx*100);
    gy = (int) (gy*100);
    gz = (int) (gz*100);

    // Print the values to the Serial Monitor
    //Serial.print(counter);
    //Serial.print('\t');
    Serial.print(ax);
    Serial.print('\t');
    Serial.print(ay);
    Serial.print('\t');
    Serial.print(az);
    Serial.print('\t');
    Serial.print(gx);
    Serial.print('\t');
    Serial.print(gy);
    Serial.print('\t');
    Serial.println(gz);
    
  // When the loop has run 200 times, reset the counter and delay
  //   3 seconds, then print empty lines and the new datapoint sequence
  } else if (counter > moveLength) {

    episode += 1;
    Serial.print("episode: ");
    Serial.println(episode);
    
    Serial.println("\n\n\n\n\n\n\n\n\n\n\n\n\n-,-,-");
    counter = 0;
    delay(3000);
  }
  // Increment the counter and delay .01 seconds
  counter += 1;
  delay(10);
}
