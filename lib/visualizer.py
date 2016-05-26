#!/usr/bin/python

from matplotlib import pyplot

import argparse
import json

class Visualizer:
    
    @staticmethod
    def visualize(data):
        visualize_functions = {
            "1d": Visualizer.visualize_1d,
            "2d": Visualizer.visualize_2d
        }
        visualize_functions[data["type"]](data["values"])

    @staticmethod
    def visualize_1d(values):
        figure = pyplot.figure()
        figure.suptitle("Intensity vs motor ticks")
        pyplot.plot(range(len(values)), values)
        pyplot.xlabel("Motor ticks")
        pyplot.ylabel("Relative Intensity")
        pyplot.grid()
        pyplot.show()

    def visualize_2d(values):
        figure = pyplot.figure()
        figure.suptitle("Scanned visualization")
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The JSON file containing the data")
    args = parser.parse_args()

    with open(args.filename) as data_file:
        Visualizer.visualize(json.loads(data_file.read().strip()))
