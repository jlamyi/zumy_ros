# the functions need to be added to Class Robot
# 1. def drive_in_dist(self, bool dir) (drive certain distance) (speed and time is default) (true is forward, false is backword)
#    inputs:
#    	(dir: direction, forward or backward)
# 2. def turn90(self) (turn certain angle) (speed and time is default)
#
# external functions
# 1. def calibration(int lastRSSI, Robot r) (find the right angle to go) (true is forward, false is backword)
#    input:
#       (lastRSSI: the best rssi value from the last location)
#	(r: the robot that is in use)
#    output:
#    	(return a bool value, the robot should go forward or backward)
#	(return the best rssi value at the current location)
# 2. def collect_rssi() (collect 30 rssi in the same place, and return the current rssi) 
#    output: the estimated rssi value according to the 30 samples (should be an integer!!!!)

import zc_id
from Xbee import *
from LCMBot import *


def calibration(lastRSSI,xb_bot,zumy_bot,counter):
    difference = -1
    for i in range(4):
        zumy_bot.drive_in_dist(True,0.7+counter*0.2,1)
        rssi = xb_bot.collect_max_rssi()
        difference = lastRSSI - rssi
        if difference > 0:
            return (rssi,0)
        zumy_bot.drive_in_dist(False,1,0.7+counter*0.2)
        zumy_bot.turn90()
    counter = counter + 1
    bestRSSI = lastRSSI
    return (bestRSSI,counter)

def calibration4(xb_bot,zumy_bot):
    bestRSSI = 9999;
    direction = 0;
    for i in range(4):
        zumy_bot.drive_in_dist(True,0.7,1)
        rssi = xb_bot.collect_max_rssi()
        print rssi
	if rssi < bestRSSI:
            bestRSSI = rssi
            direction = i
        zumy_bot.drive_in_dist(False,1,0.7)
        zumy_bot.turn90()

    for j in range(direction):
        zumy_bot.turn90()
    
    zumy_bot.drive_in_dist(True,0.7,1)

    return bestRSSI

try:
    rid = zc_id.get_id()
    r = LCMBot('{0}/base_cmd'.format(rid))
    xb = XbRssi('/dev/ttyUSB0')
    xb.start()


    counter = 0
    bestRSSI = calibration4(xb,r)
    while bestRSSI > 38:
        bestRSSI, counter = calibration(bestRSSI, xb, r, counter) 
        print bestRSSI

    print "end of while loop"
    r.stop()
except:
    r.stop()
finally:
    r.stop()
