#!/usr/bin/python

from matplotlib import pyplot
from PIL import Image

import argparse
import json
import numpy as np

class Visualizer:
    
    @staticmethod
    def visualize(data):
        visualize_functions = {
            "1d": Visualizer.visualize_1d,
            "2d": Visualizer.visualize_2d
        }
        visualize_functions[data["type"]](data)

    @staticmethod
    def visualize_1d(data):
        figure = pyplot.figure()
        figure.suptitle("Intensity vs motor ticks")
        values = data["values"]
        pyplot.plot(range(len(values)), values)
        pyplot.xlabel("Motor ticks")
        pyplot.ylabel("Relative Intensity")
        pyplot.grid()
        pyplot.show()

    @staticmethod
    def _linear_scale(x, a1, a2, b1, b2):
        return ((x - a1) * (b2 - b1) / (a2 - a1)) + b1

    @staticmethod
    def _to_pil_data(values):
        values = [val for sublist in values for val in sublist]
        low, high = min(values), max(values)
        return map(lambda x: Visualizer._linear_scale(x, low, high, 0, 255),
                   values)

    @staticmethod
    def visualize_2d(data):
        width = data["width"]
        height = data["height"]
        image = Image.new("1", (width, height))
        image.putdata(Visualizer._to_pil_data(data["value"]))
        image.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The JSON file containing the data")
    args = parser.parse_args()
    with open(args.filename) as data_file:
        Visualizer.visualize(json.loads(data_file.read().strip()))
