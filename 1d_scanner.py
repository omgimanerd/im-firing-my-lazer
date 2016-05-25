#!/usr/bin/python

from graphics.lib.color import Color
from graphics.lib.drawing import Drawing
from graphics.lib.util import Util

import argparse
import json
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
    argparser = argparse.ArgumentParser()
    argparser.add_argument("serial_port", help="The serial port to read from")
    args = argparser.parse_args()

    print "Generating a scanner data visualization..."
    scanner = Scanner.create(args.serial_port)
    data = scanner.read_laser_info()

    width = len(data)
    height = int(max(data) * 2 + 50)
    drawing = Drawing(width, height)
    for i in range(len(data) - 1):
        drawing.draw_line(i, height - data[i] - 10, 0,
                          i + 1, height - data[i + 1] - 10, 0,
                          Color.BLACK())
    drawing.display()

    print "Type a filename to save, otherwise press enter to exit..."
    filename = raw_input()
    if filename != "":
        drawing.generate("data/png/%s" % filename, extension="png")
        with open("data/json/%s.json" % filename, "w") as f:
            f.write(json.dumps({
                "data": data
            }))
