import time

class GAscent_beta_plus:
    def __init__(self, zumy, xbee):
        self.r = zumy
        self.xb = xbee

        self.left_wheel = 0.13
        self.right_wheel = 0.1

        self.counter_threshold = 1
        self.counter = 0
        self.stop_rssi = -38

        self.lastRSSI = 9999
        self.newRSSI = 0
        self.startRSSI = 0
        self.endRSSI = 0

        self.last_difference = 0

    def drive_time_function(self):
        return (abs(self.lastRSSI)-40)*0.05 + 0.2

    def stage_benefit(self):
        return self.counter*0.3

    # collect the rssi value, and save it in self.newRSSI
    def measure_rssi(self,msg):
        self.newRSSI, rssi_list = self.xb.get_max_rssi()
        print str(msg) + ": ", self.newRSSI
    
    # check if this algorithm should end
    def check_end(self):
        if self.newRSSI > self.stop_rssi:
            self.lastRSSI = self.newRSSI
            return True
        return False 

    def calibration(self):

        factor = 0.006

        self.measure_rssi("measuring rssi")

        if self.lastRSSI != 9999 and self.lastRSSI != 0:
            difference = (self.newRSSI - self.lastRSSI) - self.last_difference
            self.last_difference = self.newRSSI - self.lastRSSI

            if difference < 0:
                temp = self.left_wheel
                self.left_wheel = self.right_wheel
                self.right_wheel = temp

                total = self.left_wheel + self.right_wheel

                if self.left_wheel > self.right_wheel:
                    self.left_wheel = (total - difference * factor)/2
                    self.right_wheel = (total + difference * factor)/2
                else:
                    self.left_wheel = (total + difference * factor)/2
                    self.right_wheel = (total - difference * factor)/2

            else:
                self.left_wheel = self.left_wheel + difference * factor
                self.right_wheel = self.right_wheel - difference * factor
            #elif difference < 0: 
             #   self.left_wheel = self.left_wheel - difference * factor
              #  self.right_wheel = self.right_wheel + difference * factor

        print "left: ", self.left_wheel
        print "right: ", self.right_wheel

        self.r.drive(self.left_wheel, self.right_wheel)
        time.sleep(0.03)

        self.lastRSSI = self.newRSSI

        return 

    def start(self):
    
        print "Start.... Welcome to the new age!"
        xb = self.xb

        #time.sleep(20)

        while self.lastRSSI == 9999 or self.lastRSSI == 0:
            self.lastRSSI, rssi_list = xb.get_max_rssi()
            print "waiting for signal"
        #print self.lastRSSI
        while self.lastRSSI < self.stop_rssi:
            self.calibration()

        print "Victory!!!"
        self.r.stop()

        print "Exit GDscend"


        

