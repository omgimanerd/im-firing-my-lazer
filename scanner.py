#!/usr/bin/python

from graphics.graphics.lib.color import Color
from graphics.graphics.lib.drawing import Drawing

import json
import math
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
        return self.serial.readline().strip()

    def write(self, data):
        self.serial.write(data)

    def read_laser_info(self):
        data = []
        read = None
        while read != "begin":
            self.write("begin")
            read = self.read()
        while read != "end":
            read = self.read()
            print "Received %s" % read
            try:
                data.append(float(read) * 2)
            except ValueError:
                continue
        return data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python scanner.py <serial location>"
        print "Example: python scanner.py /dev/ttyACM0"
        sys.exit(0)
    print "Reading from %s" % sys.argv[1]

    scanner = Scanner.create(sys.argv[1])

    data = scanner.read_laser_info()
    print "Generating image..."

    width = len(data)
    height = int(max(data) * 2) + 20
    drawing = Drawing(width, height)
    for i in range(len(data) - 1):
        drawing.draw_line(i, height - int(data[i]) - 10, 0,
                          i + 1, height - int(data[i + 1]) - 10, 0,
                          Color.BLACK())
    filename = "%s" % time.strftime("%m-%d-%Y_%H-%M-%S")
    drawing.display()

    print "Type 'save' to save, otherwise type anything to exit"
    if raw_input() == "save":
        drawing.generate("data/png/%s" % filename, extension="png")
        with open("data/json/%s.json" % filename, "w") as f:
            f.write(json.dumps({
                "data": data
            }))
