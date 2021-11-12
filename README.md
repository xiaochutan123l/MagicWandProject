# MagicWandProject
Magic Wand project (Gesture recognition) using Arduino Nano 33 ble and TensorFlow Lite, it's based on the TensorFlow official example [Magic Wand](https://github.com/tensorflow/tflite-micro/tree/main/tensorflow/lite/micro/examples/magic_wand)

The hardware specific setup (install Arduino_TensorFlowLite and Arduino_LSM9DS1 libraries in the Arduino IDE) for Arduino or other MCUs please see the [old readme file](https://github.com/xiaochutan123l/tflite-micro/tree/main/tensorflow/lite/micro/examples/magic_wand) of the original repository.

## Motivation:
Original projects used only accelerometer data, thus a big move needed for a gesture prediction. But the movement of writting in the air should be far smaller, like in the Harry Potter movies. For example:

<img src="https://github.com/xiaochutan123l/MagicWandProject/blob/main/Imags/Tom_Riddle_I_am_Lord_Voldemort.gif"/>

([GIF Source](https://makeagif.com/gif/tom-riddle-i-am-lord-voldemort-5phJc7))

## Goals:
Gesture prediction with more authentic magic wand movement, like "you-know-who" did.

## Contributions:
1. Combinging data acquired from accelerometer and gyroscope, instead of only using accelerometer.
2. Acquired new datasets and modified related data processing and CNN model training code, and pre-trained a new model.
3. Optimized the origin offline real-time gesture prediction method, by introducing a rough gesture detection mechanism to adaptive the combination of two sensors and reduce computing resources.

## Result
<img src="https://github.com/xiaochutan123l/MagicWandProject/blob/main/Imags/magic-wand.gif" width="400" height="710" />
