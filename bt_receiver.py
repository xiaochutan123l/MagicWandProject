#!/usr/bin/env python
# --*--coding=utf-8--*--

import serial

baud_rate = 9600
serial_port = 'COM3'
serial_arduino = serial.Serial(serial_port, baud_rate)

print(f"serial port: {serial_port}, baud_rate: {baud_rate}")
out_list = ["w", "o", "l"]

out_str = ""

while(True):
    data = serial_arduino.readline()

    data = int(data.decode('utf-8'))
    #if int(data) < 3 and int(data) >= 0:
    #    print(f"\r{out_list[int(data)]}", end="")
    if data < 3 and data >= 0:
        if data == 2:
            out_str = out_str[:-1]
            print(f"\r{out_str}_", end="")
        else:
            out_str += out_list[data]
            print(f"\r{out_str}_", end="")