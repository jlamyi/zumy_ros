import time, threading, serial, zc_id
from xbee import XBee

class XbRssi:
    def __init__(self, serial_port): 
        self.ser = serial.Serial(serial_port, 57600)
        self.xbee = XBee(self.ser)
        self.rid = zc_id.get_id()
        self.rid = self.rid.split("/",1)[1] 
        self.id = chr(int(self.rid))
        self.xbee.at(frame='A', command='MY', parameter='\x20'+chr(int(self.rid)))
        self.xbee.at(frame='B', command='CH', parameter='\x0e')
        self.xbee.at(frame='C', command='ID', parameter='\x99\x99')
        self.updateTransmitThread = threading.Thread(target=self.transmit_loop)
        self.updateTransmitThread.daemon = True
        self.updateReceiveThread = threading.Thread(target=self.receive_loop)
        self.updateReceiveThread.daemon = True
        self.response = 0
        self.pktNum = 0
        self.predecessor = 0
        self.successor = 0
        self.transmit = True
        self.ascend = False
        self.descend = False
        self.sendMessage = self.id+'PKT'


    def transmit_loop(self):
        while True:
            self.transmit_rssi()
	    time.sleep(0.1)
    def receive_loop(self):
        while True:
            # self.collect_max_rssi()
            self.receive_pkt()
            self.decode_msg()

    def transmit_rssi(self):
        print "Sending packet #",self.pktNum,self.sendMessage
        #message = ''.join(['Hello #', repr(self.pktNum)] )
        if (self.transmit == True):
            self.xbee.tx(dest_addr='\xFF\xFF', data = self.sendMessage)
            self.pktNum = self.pktNum + 1
            #time.sleep(0.001)

    def send_msg(self, msg):
	self.xbee.tx(dest_addr='\xFF\xFF', data = msg)
	self.pktNum = self.pktNum + 1

    def receive_pkt(self):
        self.response = self.xbee.wait_read_frame()
        print self.get_data() + ", RSSI = -%d dBm @ address %d" % ( self.get_rssi(), self.get_addr() )
    
    def collect_max_rssi(self):
        # print "inside collect_max_rssi()"
        self.receive_pkt()
        current_max_rssi = self.get_rssi()
        current_max_pkt  = self.get_data()
        for i in range(30):
            # print "inside for loop"
            self.receive_pkt()
            self.decode_msg()
            next_rssi = self.get_rssi()
            next_pkt  = self.get_data()
            if next_rssi > current_max_rssi:
                # print "inside if statemene"
                current_max_rssi = next_rssi
                current_max_pkt  = next_pkt
            #print "rssi=" + str(current_max_rssi) + ", pkt=" + next_pkt
        return current_max_rssi
    def decode_msg(self):
        if (self.response != 0):
            msg =  self.get_data()
            #print msg
            if msg.startswith('TRANSMIT_START'):
                if (self.predecessor == self.get_sender_id(msg)):
                    self.transmit = True
                    self.sendMessage = 'ACK_TRANSMIT_START'
            elif msg.startswith('TRANSMIT_STOP'):
                print 'Setting transmit flag to false'
                self.transmit = False               
            elif msg.startswith('ASCEND_START'):
                self.ascend = True
                print 'Starting Gradient Ascend'
                self.sendMessage = 'ACK_ASCEND_START'
            elif msg.startswith('DESCEND_START'):
                self.descend = True
                print 'Starting Gradient Descend'
                self.sendMessage = 'ACK_DESCEND_START'
            elif msg.startswith('ARRIVAL'):
                self.chain_next_bot(msg)
                self.sendMessage = 'ACK_ARRIVAL'
            elif msg.startswith('SET_PREDECESSOR'):
                self.set_predecessor(msg)
                self.sendMessage = 'ACK_SET_PREDECESSOR'
            elif msg.startswith('ACK'):
                self.sendMessage = 'STOP_ACK'
            elif msg.startswith('STOP_ACK'):
                self.sendMessage = ''.join(['Hello #', repr(self.pktNum)] )
        else:
            return 0

    def send_arrival_signal(self):
        self.sendMessage = 'ARRIVAL-'+str(self.rid)

    def send_start_transmit_signal(self):
        self.sendMessage = 'TRANSMIT_START-'+str(self.rid)

    def send_stop_transmit_signal(self):
        self.sendMessage = 'TRANSMIT_STOP-'+str(self.rid)

    def send_set_predecessor_signal(self):
        self.sendMessage = 'SET_PREDECESSOR-'+str(self.rid)

    def send_start_ascend_signal(self):
        self.sendMessage = 'ASCEND_START-'+str(self.rid)

    def end_gradient_ascend(self):
        self.ascend = False
        self.send_arrival_signal()

    def set_predecessor(self, msg):
        if (self.predecessor == 0):
            self.predecessor = self.get_sender_id(msg)
            print 'Predecessor is set to'+str(self.predecessor)

    def chain_next_bot(self, msg):
        self.send_start_transmit_signal()
        if (self.successor == 0):
            self.successor = self.get_sender_id(msg)
            print 'Successor is set to'+str(self.successor)
            self.send_set_predecessor_signal()
        #self.send_start_ascend_signal()
        self.transmit = False

    def get_rssi(self):
        if (self.response != 0):
            return ord(self.response.get('rssi'))
        else:
            return 9999

    def get_sender_id(self, msg):
        start_index = msg.index('-')
        return msg[start_index:]

    def get_addr(self):
        if (self.response != 0):
            return ord(self.response.get('source_addr')[1])
        else:
            return 0
    def get_data(self):
        if (self.response != 0):
            return self.response.get('rf_data')
        else:
            return 0
    def start(self):
        self.updateTransmitThread.start()
        self.updateReceiveThread.start()
    # def close(self):
    #     self.ser.close()
    # def __del__ (self):
    #     self.ser.close()

if __name__=='__main__':
    xb = XbRssi('/dev/ttyUSB0')
    xb.start()
    while True:
        # print "RSSI = -%d dBm @ address %d" % ( xb.collect_max_rssi(), xb.get_addr() )
        time.sleep(0.5)
