import serial
import time
import struct

toneIndex=0

def setup(dev): #dev example '/dev/ttyUSB0'
    print("roomba setup")
    global ser
    ser = serial.Serial(dev, 115200)
#    ser.write('\x80');
    ser.write(bytes([0x80]));
    time.sleep(0.4);
    ser.write(bytes([0x83]));
#    ser.write('\x83');
    time.sleep(0.4);
#    ser.write('\x84');
    ser.write(bytes([0x84]));

def toneSetup():
    ser.write(bytes([140]))
    ser.write(bytes([4]))
    ser.write(bytes([1]))
    ser.write(bytes([30]))
    ser.write(bytes([1]))

def toneSet(note,duration):
    global toneIndex
    ser.write(bytes([140]))
    ser.write(bytes([toneIndex]))
    ser.write(bytes([1]))
    ser.write(bytes([note]))
    ser.write(bytes([duration]))

def toneKick():
    global toneIndex
    ser.write(bytes([141]))
    ser.write(bytes([toneIndex]))
    if toneIndex == 0:
        toneIndex = 1
    else:
        toneIndex = 0

def stop():
    print("roomba stop")
#    ser.write('\x85');
    #ser.write(bytes([0x85]));
    ser.close()

def shutdown():
    ser.write(bytes([0x85]));
    ser.close()

def light(io):
    pass
    ser.write(bytes([139]))
    if io > 0:
        ser.write(bytes([0x10]))
    else:
        ser.write(bytes([0x00]))
    ser.write(bytes([0]))
    ser.write(bytes([0]))

def drun(r,l):
    right = struct.pack(">h",r)
    left  = struct.pack(">h",l)
#    rad_h = (radius >> 7) & 127
#    rad_l = radius & 127
#    spd_h = (speed >> 7) & 127
#    spd_l = speed & 127
#    ser.write('\x89')
    ser.write(bytes([0x91]));
    ser.write(right)
    ser.write(left)


def run(rad,spd):
    radius = struct.pack(">h",rad)
    speed  = struct.pack(">h",spd)
#    rad_h = (radius >> 7) & 127
#    rad_l = radius & 127
#    spd_h = (speed >> 7) & 127
#    spd_l = speed & 127
#    ser.write('\x89')
    ser.write(bytes([0x89]));
    ser.write(speed)
    ser.write(radius)

#    ser.write(spd_h.to_bytes(1,'big'))
#    ser.write(spd_l.to_bytes(1,'big'))
#    ser.write(rad_h.to_bytes(1,'big'))
#    ser.write(rad_l.to_bytes(1,'big'))
