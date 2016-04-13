
import serial

ser = serial.Serial("/dev/cu.usbmodem1411", 9600)

while True:
    print ser.readline().strip()

