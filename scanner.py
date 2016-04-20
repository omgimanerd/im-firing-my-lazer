#!/usr/bin/python

from graphics.lib.color import Color
from graphics.lib.drawing import Drawing

import math
import serial
import sys
import time

class Scanner():

    BAUDRATE = 9600

    def __init__(self, serial):
        self.serial = serial
        self.data = []

    @staticmethod
    def create(location):
        return Scanner(serial.Serial(location, Scanner.BAUDRATE))

    def read(self):
        data = self.serial.readline().strip()
        print "Received %s" % data
        try:
            self.data.append(float(data))
        except ValueError:
            pass

    def get_data(self):
        return self.data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python scanner.py <serial location>"
        print "Example: python scanner.py /dev/ttyACM0"
        sys.exit(0)
    print "Reading from %s" % sys.argv[1]
    scanner = Scanner.create(sys.argv[1])
    data = None
    try:
        while True:
            scanner.read()
    except KeyboardInterrupt:
        data = scanner.get_data()
        print "Generating image..."

    width = len(data)
    height = int(max(data) * 1.5)
    drawing = Drawing(width, height)
    for i, point in enumerate(data):
        drawing._set_pixel(height - int(point) + 1, i, Color("#000000"))
    drawing.generate("data/%s" % time.strftime("%m-%d-%Y_%H-%M-%S"),
                     extension="png")
