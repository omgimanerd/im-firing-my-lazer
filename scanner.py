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
    argparser.add_argument("type", help="The type of data visualization,"
                           "either graph or gradient")
    args = argparser.parse_args()

    if args.type not in ['graph', 'gradient']:
        raise ValueError("%s is not a valid data visualization" % args.type)

    print "Generating a %s of scanner data..." % args.type
    scanner = Scanner.create(args.serial_port)
    data = scanner.read_laser_info()

    print "Generating %s..." % args.type

    drawing = None
    if args.type == "graph":
        width = len(data)
        height = int(max(data) * 2) + 20
        drawing = Drawing(width, height)
        for i in range(len(data) - 1):
            drawing.draw_line(i, height - int(data[i]) - 10, 0,
                              i + 1, height - int(data[i + 1]) - 10, 0,
                              Color.BLACK())
    elif args.type == "gradient":
        width = len(data)
        height = 100
        drawing = Drawing(width, height)
        low, high = min(data), max(data)
        
        for i in range(len(data) - 1):
            scale = Util.linear_scale(data[i], low, high, 0, 255)
            color = Color([scale, scale, scale])
            drawing.draw_line(i, 0, 0, i, 99, 0, color)

    filename = "%s_%s" % (args.type, time.strftime("%m-%d-%Y_%H-%M-%S"))
    drawing.display()
    print "Type 'save' to save, otherwise type anything to exit"
    if raw_input() == "save":
        drawing.generate("data/png/%s" % filename, extension="png")
        with open("data/json/%s.json" % filename, "w") as f:
            f.write(json.dumps({
                "data": data
            }))
