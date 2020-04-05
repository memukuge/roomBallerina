import time
import sys
import csv
import signal
import math
import roomba as r

#REPLACE WITH YOUR ROOMBA SERIAL HARDWARE

#r.setup("/dev/serial")
r.setup("/dev/serial/by-id/usb-iRobot_Corporation_iRobot_Roomba_xxxxxxxx")
#r.toneSetup()
time.sleep(0.1)
r.toneSet(80,32)
time.sleep(0.1)
r.toneKick()
time.sleep(1)
#r.run(120,100)
#time.sleep(2)
#r.run(0,0)
r.stop()
