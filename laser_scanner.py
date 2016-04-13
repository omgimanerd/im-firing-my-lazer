#!/usr/bin/python

import serial

class LaserScanner():
    
    LOCATION = "/dev/cu/usbmodem1411"
    BAUDRATE = 9600

    def __init__(self, serial):
        self.serial = serial

    @staticmethod
    def create():
        return LaserScanner(serial.Serial(LOCATION, BAUDRATE))

    def read(self):
        return self.serial.readline()

    
if __name__ == "__main__":
    scanner = LaserScanner.create()
    while True:
        scanner.read()
