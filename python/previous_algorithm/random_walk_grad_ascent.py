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


def calibration(lastRSSI,xb_bot,zumy_bot):
    bestDir = 0
    for i in range(4):
        rssi = xb_bot.collect_max_rssi()
        if i==0:
            if rssi > lastRSSI:
                return (False, lastRSSI) 
            bestRSSI = rssi
        if rssi < bestRSSI:
            bestRSSI = rssi
            bestDir = i;
        zumy_bot.turn90()
 
    for j in range(bestDir):
        zumy_bot.turn90()     
        
    return (True, bestRSSI)


rid = zc_id.get_id()
r = LCMBot('{0}/base_cmd'.format(rid))
xb = XbRssi('/dev/ttyUSB0')
xb.start()


bestRSSI = 9999;
while bestRSSI > 38:
    direction, bestRSSI = calibration(bestRSSI, xb, r)
    if bestRSSI < 38:
      print "inside if" 
      break 
    r.drive_in_dist(direction, 1, 0.9)
    if not direction:
      bestRSSI = 9999 
print "end of while loop"
r.stop()
