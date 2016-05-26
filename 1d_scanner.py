#!/usr/bin/python

from lib.visualizer import Visualizer

import argparse
import json
import serial

class Scanner_1D():

    BAUDRATE = 9600
    AMPLIFYING_FACTOR = 1

    def __init__(self, serial):
        self.serial = serial

    @staticmethod
    def create(location):
        return Scanner_1D(serial.Serial(location, Scanner_1D.BAUDRATE))

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
                data.append(float(read) * Scanner_1D.AMPLIFYING_FACTOR)
            except ValueError:
                continue
        return data

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("serial_port", help="The serial port to read from")
    args = argparser.parse_args()

    print "Generating a scanner data graph..."
    scanner = Scanner_1D.create(args.serial_port)
    data = scanner.read_laser_info()

    # Show a visualization of the data
    Visualizer.visualize_1d(data)

    # Display the drawing, then prompt to save
    print "Type a filename to save, otherwise press enter to exit..."
    filename = raw_input()
    if filename != "":
        with open("data/%s.json" % filename, "w") as data_file:
            data_file.write(json.dumps({
                "type": "1d",
                "values": data
            }))
