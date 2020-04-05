import frames
import time
import sys
import csv
import signal
import math
import roomba as r

#REPLACE WITH YOUR ROOMBA SERIAL HARDWARE

#r.setup("/dev/serial")
r.setup("/dev/serial/by-id/usb-iRobot_Corporation_iRobot_Roomba_xxxxxxxx")
r.light(255)
time.sleep(2)
r.light(0)
r.stop()
