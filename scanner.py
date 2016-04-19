#!/usr/bin/python

from lib.drawing import Drawing

import serial
import sys
import time

class Scanner():

    BAUDRATE = 9600

    def __init__(self, serial):
        self.serial = serial

    @staticmethod
    def create(location):
        return Scanner(serial.Serial(location, Scanner.BAUDRATE))

    def read(self):
        return self.serial.readline()

if __name__ == "__main__":
    print sys.argv[1]
    scanner = Scanner.create(sys.argv[1])
    while True:
        print scanner.read().strip()
