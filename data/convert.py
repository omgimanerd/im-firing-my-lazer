#!/usr/bin/python

import json
import sys

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "No file specified"

    with open(sys.argv[1]) as f:
        data = json.loads(f.read()).get("values")
    with open("%s.txt"% sys.argv[1][:-5], "w") as f:
        f.write("x y\n")
        for i in range(len(data)):
            f.write("%d %s\n" % (i, data[i]))
