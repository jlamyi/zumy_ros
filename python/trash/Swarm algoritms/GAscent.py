#import zc_id
#from Xbee import *
#from LCMBot import *
import time

class GAscent:
    def __init__(self, zumy, xbee):
        self.r = zumy
        self.xb = xbee

    def calibration(self,lastRSSI,counter):
        zumy_bot = self.r
        xb_bot = self.xb

        difference = -1
        drive_time = (abs(lastRSSI)-40)*0.05 + 0.2

        print "navigation stage ", counter
        #data = "navigation stage" + str(counter) + "\n"
        #f.write(data)

        for i in range(4):
            zumy_bot.drive_in_dist(True, 0.22,0.2,drive_time+counter*0.3)
            rssi, rssi_list = xb_bot.get_max_rssi()
            if rssi > -38:
                return (rssi,counter)
            print "measured rssi: ", rssi
            #data = "measured rssi: " + str(rssi) + "\n"
            #f.write(data)
            difference = lastRSSI - rssi
            if difference < 0:
                print "GETTING TO THE NEXT STOP!"
                #f.write("GETTING TO THE NEXT STOP! \n")
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
            #f.write("re-calibrating...\n")
            bestRSSI,rssi_list = xb_bot.get_max_rssi()
            if bestRSSI > -38:
                return (bestRSSI,counter)
            print "re-calibrated bestRSSI: ", bestRSSI
            #f.write("re-calibrated bestRSSI: " + str(bestRSSI) + "\n")
            counter = 0
        return (bestRSSI,counter)

    def start(self):
    
        print "Start.... Welcome to the new age!"
        xb = self.xb

        counter = 0
        bestRSSI = 9999
        #time.sleep(20)

        while bestRSSI == 9999 or bestRSSI == 0:
            bestRSSI, rssi_list = xb.get_max_rssi()
            print bestRSSI

        print "current bestRSSI: ", bestRSSI
        while bestRSSI < -38:
            bestRSSI, counter = self.calibration(bestRSSI, counter) 
            print "current bestRSSI: ",bestRSSI
            #f.write("current bestRSSI: " + str(bestRSSI) + "\n")

        print "Victory!!!"
        self.r.stop()

        #ack = xb.get_data()
        #self.xb.send_arrival_signal()

        #while ~ack.startswith("ACK"):
        #    xb.set_transmit_thread(True)
            
        #    xb.send_arrival_signal()
        print "Exit GAscend"
        # xb.set_ascend(False)

        #print self.xb.sendMessage 
        #f.write("Victory!!!")

        

