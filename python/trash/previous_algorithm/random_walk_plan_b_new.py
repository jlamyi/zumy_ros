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
import time

def calibration(lastRSSI,xb_bot,zumy_bot,counter,f):
    difference = -1

    #drive_time = (abs(lastRSSI)-40)*0.1 + 1
    drive_time = (abs(lastRSSI)-40)*0.05 + 0.2
    print "navigation stage ", counter
    data = "navigation stage" + str(counter) + "\n"
    f.write(data)
    for i in range(4):
        zumy_bot.drive_in_dist(True, 0.22,0.2,drive_time+counter*0.3)
        rssi, rssi_list = xb_bot.get_max_rssi()
        if rssi > -38:
            return (rssi,counter)
        print "measured rssi: ", rssi
        data = "measured rssi: " + str(rssi) + "\n"
        f.write(data)
        difference = lastRSSI - rssi
        if difference < 0:
            print "GETTING TO THE NEXT STOP!"
            f.write("GETTING TO THE NEXT STOP! \n")
            return (rssi,0)
        time.sleep(0.1)
        zumy_bot.drive_in_dist(False,0.22,0.2, drive_time+counter*0.3)
        lastRSSI, rssi_list = xb_bot.get_max_rssi()
        if lastRSSI > -38:
            return (lastRSSI,counter)
        print "bestRSSI update: ", lastRSSI
        zumy_bot.turn90()

    counter = counter + 1
    bestRSSI = lastRSSI
    if counter > 1:
        print "re-calibrating..."
        f.write("re-calibrating...\n")
        bestRSSI,rssi_list = xb_bot.get_max_rssi()
        if bestRSSI > -38:
            return (bestRSSI,counter)
        print "re-calibrated bestRSSI: ", bestRSSI
        f.write("re-calibrated bestRSSI: " + str(bestRSSI) + "\n")
        counter = 0
    return (bestRSSI,counter)



if __name__ == '__main__':
        file_name = raw_input("Please input the file name: ") 
        f = open(file_name+".csv","w")
    #try:
        rid = zc_id.get_id()
        r = LCMBot('{0}/base_cmd'.format(rid))
        xb = XbRssi('/dev/ttyUSB0')
        #xb.start()


        counter = 0
        bestRSSI, rssi_list = xb.get_max_rssi()
        while bestRSSI == 9999:
            bestRSSI, rssi_list = xb.get_max_rssi()
        #bestRSSI = calibration4(xb,r)
        print "current bestRSSI: ", bestRSSI
        while bestRSSI < -38:
            bestRSSI, counter = calibration(bestRSSI, xb, r, counter,f) 
            print "current bestRSSI: ",bestRSSI
            f.write("current bestRSSI: " + str(bestRSSI) + "\n")
        print "Victory!!!"
        f.write("Victory!!!")
        r.stop()
 #except:
  #      r.stop()
   # finally:
    #    r.stop()
     #   f.close()'''
