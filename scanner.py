#!/usr/bin/python

from lib.visualizer import Visualizer

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
        data = {}
        values = []
        read = None
        while read != "begin":
            self.write("begin")
            read = self.read()
        while True:
            read = self.read()
            if read == "end":
                break
            print "Received %s" % read
            try:
                values.append(float(read) * 2)
            except ValueError:
                try:
                    data.update(json.loads(read))
                except:
                    continue
        data.update({
            "values": values
        })
        return data

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("serial_port", help="The serial port to read from")
    args = argparser.parse_args()

    print "Generating a scanner data visualization..."
    scanner = Scanner.create(args.serial_port)
    data = scanner.read_laser_info()

    Visualizer.visualize(data)

    print "Type a filename to save, otherwise press enter to exit..."
    filename = raw_input()
    if filename != "":
        with open("data/%s.json" % filename, "w") as f:
            f.write(json.dumps(data))
