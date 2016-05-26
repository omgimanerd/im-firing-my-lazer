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
    AMPLIFYING_FACTOR = 3

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
        sublist = []
        read = None
        while read != "begin":
            self.write("begin")
            read = self.read()
        while read != "end":
            read = self.read()
            print "Received %s" % read
            if read == "row":
                data.append(sublist)
                sublist = []
                continue
            try:
                sublist.append(float(read) * 2)
            except ValueError:
                sublist.append(0)
        return data

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("serial_port", help="The serial port to read from")
    args = argparser.parse_args()

    print "Generating a scanner data visualization..."
    scanner = Scanner.create(args.serial_port)
    data = scanner.read_laser_info()

    width = len(data)
    height = len(data[0])
    drawing = Drawing(width, height)
    flattened_data = [val for row in data for val in row]
    low, high = min(flattened_data), max(flattened_data)
    for x in range(width):
        for x in range(height):
            scale = Util.linear_scale(..., low, high, 0, 255)
            drawing.draw_point()

    filename = "%s_%s" % (args.type, time.strftime("%m-%d-%Y_%H-%M-%S"))
    drawing.display()
    print "Type 'save' to save, otherwise type anything to exit"
    if raw_input() == "save":
        drawing.generate("data/png/%s" % filename, extension="png")
        with open("data/json/%s.json" % filename, "w") as f:
            f.write(json.dumps({
                "data": data
            }))
