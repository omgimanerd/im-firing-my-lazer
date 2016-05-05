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

    def read_until_interrupt(self):
        data = []
        try:
            while True:
                read = self.read()
                print "Received %s" % read
                try:
                    data.append(float(read))
                except ValueError:
                    continue
        except KeyboardInterrupt:
            return data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python scanner.py <serial location>"
        print "Example: python scanner.py /dev/ttyACM0"
        sys.exit(0)
    print "Reading from %s" % sys.argv[1]

    scanner = Scanner.create(sys.argv[1])
    data = scanner.read_until_interrupt()
    print "Generating image..."

    width = len(data)
    height = int(max(data) * 1.5)
    drawing = Drawing(width, height)
    print width, height
    for i in range(len(data) - 1):
        drawing.draw_line(height - int(data[i]) + 1, i, 0,
                          height - int(data[i + 1]) + 1, i + 1, 0,
                          Color.BLACK())

    filename = "data/%s" % time.strftime("%m-%d-%Y_%H-%M-%S")
    drawing.generate(filename, extension="png")
    with open("%s.json" % filename, "w") as f:
        f.write(json.dumps({
            "data": data
        }))
