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

#include "accelerometer_handler.h"

#include <Arduino.h>
#include <Arduino_LSM9DS1.h>

#include "constants.h"

// A buffer holding the last 200 sets of 3-channel values
float save_data[1200] = {0.0};
// Most recent position in the save_data buffer
int begin_index = 0;

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

  TF_LITE_REPORT_ERROR(error_reporter, "Magic starts!");

  return kTfLiteOk;
}

bool ReadAccelerometer(tflite::ErrorReporter* error_reporter, float* input,
                       int length) {
  // Keep track of whether we stored any new data
  bool new_data = false;
  int slide_window = 32; // 128 / 4
  // Loop through new samples and add to buffer
  while (slide_window > 0){
    while (IMU.accelerationAvailable() and IMU.gyroscopeAvailable()) {
      float ax, ay, az, gx, gy, gz;
      // Read each sample, removing it from the device's FIFO buffer
      if (!IMU.readAcceleration(ax, ay, az) or !IMU.readGyroscope(gx, gy, gz)) {
        TF_LITE_REPORT_ERROR(error_reporter, "Failed to read data");
        break;
      }
      // Write samples to our buffer, converting to milli-Gs and rotating the axis
      // order for compatibility with model (sensor orientation is different on
      // Arduino Nano BLE Sense compared with SparkFun Edge).
      // The expected orientation of the Arduino on the wand is with the USB port
      // facing down the shaft towards the user's hand, with the reset button
      // pointing at the user's face:
      //
      //                  ____
      //                 |    |<- Arduino board
      //                 |    |
      //                 | () |  <- Reset button
      //                 |    |
      //                  -TT-   <- USB port
      //                   ||
      //                   ||<- Wand
      //                  ....
      //                   ||
      //                   ||
      //                   ()
      //
      save_data[begin_index++] = ax / 4;
      save_data[begin_index++] = ay / 4;
      save_data[begin_index++] = az / 4;
      save_data[begin_index++] = gx / 1000;
      save_data[begin_index++] = gy / 1000;
      save_data[begin_index++] = gz / 1000;
      
      slide_window -= 1;
      // If we reached the end of the circle buffer, reset
      if (begin_index >= 1200) {
        begin_index = 0;
      }
    }
    //delay(15);
    delay(5);
  }
    
  // Copy the requested number of bytes to the provided input tensor
  for (int i = 0; i < length; ++i) {
    int ring_array_index = begin_index + i - length;
    if (ring_array_index < 0) {
      ring_array_index += 1200;
    }
    input[i] = save_data[ring_array_index];
  }

  return true;
}

#endif  // ARDUINO_EXCLUDE_CODE
