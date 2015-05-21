import time
from GDscent import *

class GDscent_multiBot(GDscent):
    def __init__(self, zumy, xbee_multiBot):
        self.r = zumy
        self.xb = xbee_multiBot

        self.left_wheel = 0.22
        self.right_wheel = 0.2

        self.counter_threshold = 1
        self.counter = 0

        self.connections = []
        self.single_stop_rssi = -50
        self.stop_rssi = -50

        self.lastRSSI = 9999
        self.newRSSI = 0
        self.startRSSI = 0
        self.endRSSI = 0

    
    def drive_time_function(self):
        return (abs(self.lastRSSI)-40)*0.05 + 0.4
    '''
    def stage_benefit(self):
        return self.counter*0.3
    '''
    
    def set_connections(self):
        self.connections = self.xb.show_connections()
        #if len(self.connections) != 0:
        #    self.stop_rssi = (self.single_stop_rssi) * len(self.connections)
    # collect the rssi value, and save it in self.newRSSI
    def measure_rssi(self,msg):

        self.newRSSI = 0
        for i in range(len(self.connections)):
            rssi, rssi_list = self.xb.get_max_rssi(self.connections[i])
            self.newRSSI = self.newRSSI + rssi

        self.newRSSI = self.newRSSI / len(self.connections)
        print str(msg) + ": ", self.newRSSI
    
    # check if this algorithm should end
    '''
    def check_end(self):
        if self.newRSSI < self.stop_rssi:
            self.lastRSSI = self.newRSSI
            return True
        return False 
    '''

    '''
    def calibration(self):
        zumy_bot = self.r
        xb_bot = self.xb

        drive_time = self.drive_time_function()

        last_endRssi = 0

        print "++++++++++++++++++++++++++++++++++"
        print "navigation stage ", self.counter

        for i in range(4):

            print "-----------------------------"
            self.measure_rssi("Starting point rssi")
            if self.check_end():
                return
            self.startRSSI = self.newRSSI
            
            zumy_bot.drive_in_dist(True, self.left_wheel,self.right_wheel,drive_time + self.stage_benefit())
            
            self.measure_rssi("Stop point rssi")
            if self.check_end():
                return
            self.endRSSI = self.newRSSI
            #last_endRssi = self.newRSSI

            difference = abs(self.endRSSI) - abs(self.startRSSI) 
            if difference > 0:
                print "GETTING TO THE NEXT STOP!"
                self.counter = 0
                self.lastRSSI = self.endRSSI
                return 

            zumy_bot.drive_in_dist(False,self.left_wheel,self.right_wheel, drive_time + self.stage_benefit())

            #if i > 0 and abs(self.endRSSI) < abs(last_endRssi): 
             #   zumy_bot.turn90(False)
              #  zumy_bot.drive_in_dist(True, self.left_wheel,self.right_wheel,drive_time + self.stage_benefit()) 
               # return               

            zumy_bot.turn90()

        # stage management   
        self.counter = self.counter + 1
        if self.counter > self.counter_threshold:
            self.counter = 0

        return 
    '''
    def start(self):
    
        print "Start.... Welcome to the new age!"
        xb = self.xb

        self.set_connections()
        #time.sleep(20)
        while len(self.connections) == 0:
            print "waiting for connections"
            self.set_connections()

        print "Connections:", self.connections

        while self.lastRSSI == 9999 or self.lastRSSI == 0:
            self.lastRSSI, rssi_list = xb.get_max_rssi(self.connections[0])
            print "waiting for signal"
        #print self.lastRSSI
        while self.lastRSSI > self.stop_rssi:
            self.calibration()

        print "Victory!!!"
        self.r.stop()

        print "Exit GDscend"
    


        

