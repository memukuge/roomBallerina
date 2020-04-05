import frames
import time
import sys
#import pandas as pd
import csv
import signal
import math
#import numpy
import roomba as r
import singer as s
#measure,beat,hex,beat_r,hex_r,radius,speed,angle
MEASURE=0
BEAT=1
HEX=2
BEAT_R=3
HEX_R=4
RADIUS=5
SPEED=6
ANGLE=7

LIGHTTICK_PRESET=1

#args
#player.py sequence.csv beat tempo

def closehandler(signal, frame):
    if dryRun == 0:
        r.run(0,0)
        r.stop()

    print("closehandler")
    sys.exit(0)


def dbgprt(arg):
    print(arg)


def row2abshex(row):
    if row.get("measure"):
        #dbgprt("measure : " + row.get("measure"))
        r2_measure=int(row.get("measure"))
    else:
        return None
    if row.get("beat"):
        #dbgprt("beat : " + row.get("beat"))
        r2_beat=int(row.get("beat"))
    else:
        r2_beat=0
    if row.get("hex"):
        #dbgprt("hex : " + row.get("hex"))
        r2_hex=int(row.get("hex"))
    else:
        r2_hex=0
    absolutehex=r2_hex+r2_beat*4+r2_measure*4*int(musicbeat)
    #dbgprt("absolutehexInDef : " + str(absolutehex) + " beat : " + str(musicbeat))
    return absolutehex

def row2relhex(row):
    if row.get("beat_r"):
        #dbgprt("beat : " + row.get("beat"))
        r2_beat=int(row.get("beat_r"))
    else:
        r2_beat=0
    if row.get("hex_r"):
        #dbgprt("hex : " + row.get("hex"))
        r2_hex=int(row.get("hex_r"))
    else:
        r2_hex=0
    relativehex=r2_hex+r2_beat*4
    #dbgprt("absolutehexInDef : " + str(absolutehex) + " beat : " + str(musicbeat))
    return relativehex


def caliculateSpeedFromAngle(angle,radius,waittick):
    driveDulation = float(waittick) * secPerTick
    amplify = math.pow(float(radius), -0.531) * 25.26
    wheelRadius=float(radius) / amplify + 124.0

    dbgprt("tempo " + str(tempo) + " bpm")
    dbgprt("waittick " + str(waittick) + " ticks")
    dbgprt("secpertick " + str(secPerTick) + " sec")
    dbgprt("dulation " + str(driveDulation) + " sec")
    dbgprt("WheelRadius " + str(wheelRadius) + " mm")
    dbgprt("targetAngleInPiRadian " + str(float(angle) / 180))
    #
    # if rad=1,speed =pi, when dulation=1sec, angle=180
    # if rad =2, dulation = 1sec angle = 90
    # pi x dulation / radius  = radian
    # angle = rad2ang(pi*dulation/radius)
    # ex rad = 120 , wheelradius = 240,
    # to go 180 deg = piradian, 240 x pi mm
    # in 2 sec:  speed = 240 x pi / 2
    # therefore speed = wheelradius x pi / driveDulation
    caliculatedSpeed = wheelRadius * math.pi / driveDulation * float(angle) / 180.0

    #distance = wheelRadius * math.pi
    #angleMultiply = (float)angle / 180.0
    #caliculatedSpeed = distance / driveDulation * angle / 180.0
    #caliculatedSpeed = wheelRadius * math.pi / driveDulation * angle / 180.0
    return str(round(caliculatedSpeed))


def caliculateRLFromAngle(angle,radius,waittick):
    driveDulation = float(waittick) * secPerTick
    segment = 126
    #amplify = math.pow(float(radius), -0.531) * 25.26
    if float(radius) > 0:
        radiusR=float(radius)+segment
        radiusL=float(radius)-segment
    if float(radius) < 0:
        radiusR=float(radius)-segment
        radiusL=float(radius)+segment

    spdR = radiusR * math.pi / driveDulation * float(angle) / 180.0
    spdL = radiusL * math.pi / driveDulation * float(angle) / 180.0
    return spdR,spdL



signal.signal(signal.SIGINT, closehandler)
print(time.time())

args = sys.argv
if(len(args) < 3):
    print("args: main.py mml stepcsv beat tempo")
    sys.exit()

filename = args[1]
csvname = args[2]
musicbeat = args[3]
tempo = float(args[4])
secPerTick= 60.0 / float(tempo) / 4.0
starthex = 0

try:
    sys.argv[5]
    dryRun = int(args[5])
except:
    dryRun=0

#startmeasure = int(args[4])
index = 0
#df=pd.read_csv(filename)
mml = open(filename, "r")
csv_file = open(csvname, "r")
#f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
#f = csv.reader(csv_file, delimiter=",")
f = csv.DictReader(csv_file)
ticktempo = tempo * 4 / 60

if dryRun == 0:
    r.setup("/dev/ttyACM0")


soundWaittick=0
lightWaittick=0
stepWaittick =0
diffhex=0

"""
1 get note
2 set note

3 ring note
4 get next note
5 set next note
6 set wait for note
"""

chroma,tonelen,dot,finflg = s.parseNext(mml)
toneTicks = 16/tonelen
if dot == True:
    toneTicks = toneTicks + toneTicks / 2
toneTime = toneTicks * secPerTick * 0.9
toneDur = int(toneTime * 64)
if chroma == -1:
    chroma = 0
r.toneSet(chroma,toneDur)
print("toneSet",chroma,toneTime,tonelen,dot,toneDur)


print ('hit any key to start')
input_test_word = input('>>>  ')
#time.sleep(1)
frames.timer = frames.Timer(ticktempo)
#len=len(df)


row=next(f);
if row.get("measure"):
    currenthex=int(row2abshex(row))
    dbgprt("absolutehex : " + str(row2abshex(row)))
else:
    dbgprt("noabsolutehex")
    closehandler(None,None)



while True:
    #if currenthex >= starthex:
    if frames.timer.tick():
        raise ValueError('cannot maintain desired FPS rate')
    print(time.perf_counter())

    if soundWaittick == 0:
        #currenthex = currenthex + diffhex
        r.toneKick()
        print("toneKick")
        if chroma != 0:
            pass
            r.light(255)
        lightWaittick = LIGHTTICK_PRESET

    if lightWaittick == 0:
        pass
        r.light(0)

    if soundWaittick == 0:
        soundWaittick = toneTicks
        chroma,tonelen,dot,finflg = s.parseNext(mml)
        toneTicks = 16/tonelen
        if dot == True:
            toneTicks = toneTicks + toneTicks / 2
        toneTime = toneTicks * secPerTick * 0.9
        toneDur = int(toneTime * 64)
        if chroma == -1:
            chroma = 0

        r.toneSet(chroma,toneDur)
        print("toneSet",chroma,toneTime,tonelen,dot,toneDur)



    if stepWaittick == 0:
        currenthex = currenthex + diffhex
        try:
            nextrow=next(f)
        except:
            break # file end
        dbgprt(nextrow)
        if nextrow.get("measure"):
            nexthex=row2abshex(nextrow)
            diffhex=nexthex-currenthex
            #dbgprt("nexthex : " + str(row2abshex(nextrow)) + " diffhex : "+ str(diffhex) )
        else:
            diffhex=row2relhex(nextrow)
            #dbgprt("diffhex : " + str(diffhex))
        if diffhex==0:
            print("error diff 0")
            closehandler(None,None)
        stepWaittick=diffhex

        if row.get("radius"):
            radius=row.get("radius")
        else:
            print("error no radius")
            closehandler(None,None)

        if row.get("speed"):
            speed=row.get("speed")
            print("run in " + radius + " " + speed)
            if dryRun == 0 and currenthex > starthex:
                r.run(int(radius),int(speed))
        else:
            if row.get("angle"):
                angle=row.get("angle")
            else:
                print("no speed, angle")
                closehandler(None,None)
            RLspeed=caliculateRLFromAngle(angle,radius,waittick)
            print("run in R" + str(RLspeed[0]) + " L" + str(RLspeed[1]))
            if RLspeed[0] > 500 or RLspeed[1] > 500:
                print("overspeed")
                closehandler(None,None)
            if dryRun == 0 and currenthex > starthex:
                r.drun(int(RLspeed[0]),int(RLspeed[1]))
        row = nextrow


    soundWaittick = soundWaittick - 1
    lightWaittick = lightWaittick - 1
    stepWaittick = stepWaittick - 1

closehandler(None,None)
