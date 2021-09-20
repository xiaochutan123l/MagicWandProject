/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#if defined(ARDUINO) && !defined(ARDUINO_ARDUINO_NANO33BLE)
#define ARDUINO_EXCLUDE_CODE
#endif  // defined(ARDUINO) && !defined(ARDUINO_ARDUINO_NANO33BLE)

#ifndef ARDUINO_EXCLUDE_CODE

#include "accelerometer_handler2.h"

#include <Arduino.h>
#include <Arduino_LSM9DS1.h>

#include "constants.h"
int counter = 0;
TfLiteStatus SetupAccelerometer(tflite::ErrorReporter* error_reporter) {
  // Switch on the IMU
  if (!IMU.begin()) {
    TF_LITE_REPORT_ERROR(error_reporter, "Failed to initialize IMU");
    return kTfLiteError;
  }

  // Make sure we are pulling measurements into a FIFO.
  // If you see an error on this line, make sure you have at least v1.1.0 of the
  // Arduino_LSM9DS1 library installed.
  IMU.setContinuousMode();

  // Determine how many measurements to keep in order to
  // meet kTargetHz
  TF_LITE_REPORT_ERROR(error_reporter, "Magic starts!");

  return kTfLiteOk;
}

bool ReadAccelerometer(tflite::ErrorReporter* error_reporter, float* input,
                       int length) {
  counter = 0;
  //float save_data[(length * kChannelNumber)] = {0.0};
  float ax, ay, az, gx, gy, gz;
  bool jump = true;
  
  while (counter < length) {
    while (IMU.accelerationAvailable() and IMU.gyroscopeAvailable()) {
      // Read each sample, removing it from the device's FIFO buffer
      if (!IMU.readAcceleration(ax, ay, az) or !IMU.readGyroscope(gx, gy, gz)) {
        TF_LITE_REPORT_ERROR(error_reporter, "Failed to read data");
        break;
      }
      if (jump){
        jump = false;
        break;
        }
      jump = true;
      input[counter++] = ax / 4;
      input[counter++] = ay / 4;
      input[counter++] = az / 4;
      input[counter++] = gx / 1000;
      input[counter++] = gy / 1000;
      input[counter++] = gz / 1000;
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
      }
    }
  //delay(2000);
  return true;
}

#endif  // ARDUINO_EXCLUDE_CODE
