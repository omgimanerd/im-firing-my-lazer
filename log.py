import sys, os, serial, threading

def monitor():

   ser = serial.Serial(COMPORT, BAUDRATE, timeout=0)

   while (1):
       line = ser.readline()
       if (line != ""):
           #print line[:-1]         # strip \n
           fields = line[:-1].split('; ');

           // ID = fields[0]
                 // TIME = int(fields[1])
           # print fields
           print "device ID: ", ID
           # write to file
           text_file = open("Pdata.log", "w")
           line = str(TIME) + ": " + str(CT) + "\n"
           text_file.write(line)
           text_file.close()

       # do some other things here

   print "Stop Monitoring"

""" -------------------------------------------
MAIN APPLICATION
"""  

print "Start Serial Monitor"
print

COMPORT = 4;
BAUDRATE = 115200

monitor()

