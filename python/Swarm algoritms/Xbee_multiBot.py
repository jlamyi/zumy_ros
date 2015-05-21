import time, threading, serial
from numpy import *
from Xbee import XbRssi

class Xbee_multiBot(XbRssi):
    def __init__(self,serial_port): 
        XbRssi.__init__(self,serial_port)  
        '''      
        self.predecessor = 0
        self.successor = 0
        self.transmit = True
        self.ascend = False
        self.descend = False
        self.startReceive = True
        self.sendMessage = self.id+'PKT'
        self.cmdList = []
        '''
    
    def show_connections(self):
        connections = []

        sender_id = self.get_sender_id(self.data)
        if sender_id == "NO_SENDER":
            return connections
        connections.append(sender_id)

        for i in range(50): 

            sender_id = self.get_sender_id(self.data)

            if sender_id not in connections:
                connections.append(sender_id)

            time.sleep(.01)

        return connections

    # receiver
    def get_rssi_list(self, bot_id):
        rssi_list = []
        index_list = []

        msg = self.data
        pkt_index = self.get_index(msg)

        rssi_list.append(self.rssi)
        index_list.append(pkt_index)

        i = 1
        while i<30:  

            msg = self.data
            sender_id = self.get_sender_id(msg)
            pkt_index = self.get_index(msg)

            if pkt_index != index_list[-1] and bot_id == sender_id:
                rssi_list.append(self.rssi)
                index_list.append(pkt_index)
                i = i + 1

            time.sleep(.01)
        return rssi_list

    # data processing functions
    def get_max_rssi(self,bot_id):
        rssi_list = self.get_rssi_list(bot_id)
        rssi_max = max(rssi_list)
        return rssi_max, rssi_list

    def get_min_rssi(self,bot_id):
        rssi_list = self.get_rssi_list(bot_id)
        rssi_min = min(rssi_list)
        return rssi_min, rssi_list

    def get_med_rssi(self,bot_id):
        rssi_list = self.get_rssi_list(bot_id)
        rssi_med = median(rssi_list)
        return rssi_med, rssi_list

    def get_avg_rssi(self,bot_id):
        rssi_list = self.get_rssi_list(bot_id)
        rssi_avg = mean(rssi_list)
        return rssi_avg, rssi_list

'''
if __name__=='__main__':
    xb = Xbee_chiaing_bot('/dev/ttyUSB0')

    result = xb.get_max_rssi()
    print "the maximum is: ", result
    result = xb.get_min_rssi()
    print "the minimum is: ", result
    result = xb.get_avg_rssi()
    print "the average is: ", result
    result = xb.get_med_rssi()
    print "the median is: ", result
'''
