
import time, threading, serial, zc_id
from xbee import XBee
from numpy import *

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
        self.startReceive = True
        self.sendMessage = self.id+'PKT'
        self.buffer = ['0']
        self.newest_byte = '0'
        self.ser.flush()

    def transmit_loop(self):
        while True:
            self.transmit_rssi()
            time.sleep(2)

    def receive_loop(self):
        while True:
            #if self.startReceive == True:
            # self.get_max_rssi()
            self.receive_pkt()
            self.decode_msg() 
            #time.sleep(10)

    def transmit_rssi(self):
        # print "Sending packet #",self.pktNum
        if (self.transmit == True):
            #message = ''.join(['Hello #', repr(self.pktNum)] )
            self.xbee.tx(dest_addr='\xFF\xFF', data = self.sendMessage)
            self.pktNum = self.pktNum + 1
            time.sleep(2)

    def receive_pkt(self):
        self.response = self.xbee.wait_read_frame()
        self.decode_msg()
        print self.get_data() + ", RSSI = -%d dBm @ address %d" % ( self.get_rssi(), self.get_addr() )
    
    def get_rssi(self):
        if (self.response != 0):
            return -ord(self.response.get('rssi'))
        else:
            return 9999
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
    def get_max_rssi(self):
        rssi_list = []
        for i in range(30):
            #print i
            try:
                self.receive_pkt()
                self.decode_msg()
                self.ser.flush()
            except:
                print i                
            rssi_list.append(self.get_rssi())
        rssi_max = max(rssi_list)
        print rssi_list
        print "rssi_max = " + str(rssi_max)
        return rssi_max, rssi_list
    def get_min_rssi(self):
        rssi_list = []
        for i in range(30):
            self.receive_pkt()
            rssi_list.append(self.get_rssi())
        rssi_min = min(rssi_list)
        print rssi_list
        print "rssi_min = " + str(rssi_min)
        return rssi_min, rssi_list
    def get_med_rssi(self):
        rssi_list = []
        for i in range(30):
            self.receive_pkt()
            rssi_list.append(self.get_rssi())
        rssi_med = median(rssi_list)
        print rssi_list
        print "rssi_med = " + str(rssi_med)
        return rssi_med, rssi_list
    def get_avg_rssi(self):
        rssi_list = []
        for i in range(30):
            self.receive_pkt()
            rssi_list.append(self.get_rssi())
        rssi_avg = mean(rssi_list)
        print rssi_list
        print "rssi_avg = " + str(rssi_avg)
        return rssi_avg, rssi_list
    def decode_msg(self):
        if (self.response != 0):
            msg =  self.get_data()
            #print msg
            if msg.startswith('TRANSMIT_START'):
                if (self.predecessor == self.get_sender_id(msg)):
                    self.transmit = True
                    self.send_ack()
                    #self.sendMessage = 'ACK_TRANSMIT_START'
            elif msg.startswith('TRANSMIT_STOP'):
                print 'Setting transmit flag to false'
                self.transmit = False               
            elif msg.startswith('ASCEND_START'):
                self.ascend = True
                #print 'Starting Gradient Ascend'
                self.send_ack()
                #self.sendMessage = 'ACK_ASCEND_START'
            elif msg.startswith('DESCEND_START'):
                self.descend = True
                print 'Starting Gradient Descend'
                self.send_ack()
  #              self.sendMessage = 'ACK_DESCEND_START'
            elif msg.startswith('ARRIVAL'):
                self.chain_next_bot(msg)
                self.send_ack()
      #          self.sendMessage = 'ACK_ARRIVAL'
            elif msg.startswith('SET_PREDECESSOR'):
                self.set_predecessor(msg)
                self.sendMessage = 'ACK_SET_PREDECESSOR'
                self.send_ack()
            #elif msg.startswith('ACK'):
            #    self.sendMessage = 'STOP_ACK'
            #    self.xbee.tx(dest_addr='\xFF\xFF', data = self.sendMessage)
            #    self.pktNum = self.pktNum + 1
            elif msg.startswith('STOP_ACK'):
                self.sendMessage = ''.join(['Hello #', repr(self.pktNum)] )

            #buff = self.buffer
            #print buff
            #self.buffer = buff.append(msg)
            #print 'a'
            #print self.serial.read()

        else:
            return 0

    def send_ack(self):
        send_msg = 'ACK'+str(self.rid)
        msg = self.get_data()
        strr='0'
        while(~msg.startswith('STOP_ACK')):
            print "Sending ACK"
            self.xbee.tx(dest_addr='\xFF\xFF', data = send_msg)
            self.pktNum = self.pktNum + 1
            msg = self.get_data()
            i = 0
            while True:
                i = i+1
                #try:
                #    signal.signal(signal.SIGALRM, self.read_byte()) 
                #    signal.alarm(10)
                cur_char = str(self.ser.read())

                strr = strr+ cur_char
                #except:
                #    break
                #strr = strr+ str(self.ser.read())
                if i > 20:
                    break
                if 'STOP' in strr:
                    break
                print strr 
            print 'msg:' + msg
            if 'STOP' in strr:
                break
            self.ser.flush()
            strr = '0'
            time.sleep(3)
        self.sendMessage = ''.join(['Hello #', repr(self.pktNum)] )
        send_msg = self.sendMessage
        strr='0'

        while(~msg.startswith('Hello')):
            print "Sending Ending_command"
            self.xbee.tx(dest_addr='\xFF\xFF', data = send_msg)
            self.pktNum = self.pktNum + 1
            msg = self.get_data()
            i = 0
            while True:
                i = i+1
                #try:
                #    signal.signal(signal.SIGALRM, self.read_byte()) 
                #    signal.alarm(10)
                cur_char = str(self.ser.read())

                strr = strr+ cur_char
                #except:
                #    break
                #strr = strr+ str(self.ser.read())
                print strr 
                if i > 20:
                    break
                if 'Hello' in strr:
                    break
             #   if 'STOP' not in strr:
             #       break
                
                #self.ser.flush()
            print 'msg:' + msg
            if 'Hello' in strr:
                break
            if (i > 0 and 'STOP' not in strr):
                break
            #if 'STOP' not in strr:
            #    break
            self.ser.flush()
            strr = '0'
            print msg
            print 'b'
            if msg.startswith('Hello'):
                break
            if 'Hello' in strr:
                break
            #time.sleep(3)
        self.sendMessage = ''.join(['Hello #', repr(self.pktNum)] )
        self.ser.flush()
        print "Exiting Ending_command"

    def send_msg(self, sendmsg):
        msg = self.get_data()
        print sendmsg
        while msg == 0:
            self.xbee.tx(dest_addr='\xFF\xFF', data = sendmsg)
            self.pktNum = self.pktNum + 1
            try:
                signal.signal(signal.SIGALRM, self.receive_pkt_handler())
                signal.alarm(1)
            except:
                print self.pktNum
            msg = self.get_data()
            print msg
            time.sleep(1)

        while(~msg.startswith('ACK')):
            self.xbee.tx(dest_addr='\xFF\xFF', data = sendmsg)
            self.pktNum = self.pktNum + 1
            self.receive_pkt()
            msg = self.get_data()
            time.sleep(2)
            print 'waiting_for_ack for' + sendmsg
        self.sendMessage = 'STOP_ACK'

    def read_byte(self):
        self.newest_byte = self.ser.read()
        return self.newest_byte

    def send_arrival_signal(self):
        self.sendMessage = 'ARRIVAL-'+str(self.rid)
        self.send_msg(self.sendMessage)

    def send_start_transmit_signal(self):
        self.sendMessage = 'TRANSMIT_START-'+str(self.rid)
        self.send_msg(self.sendMessage)

    def send_stop_transmit_signal(self):
        self.sendMessage = 'TRANSMIT_STOP-'+str(self.rid)
        self.send_msg(self.sendMessage)

    def send_set_predecessor_signal(self):
        self.sendMessage = 'SET_PREDECESSOR-'+str(self.rid)
        self.send_msg(self.sendMessage)

    def send_start_ascend_signal(self):
        self.sendMessage = 'ASCEND_START-'+str(self.rid)
        msg = self.sendMessage
        self.send_msg(msg)

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
        self.send_start_ascend_signal()
        self.transmit = False

    def get_sender_id(self, msg):
        start_index = msg.index('-')
        return msg[start_index:]

    def get_ascend_status(self):
        return self.ascend

    def set_receiver_thread(self, b):
        self.startReceive = b

    def set_transmit_thread(self, b):
        self.transmit = b

    def set_ascend(self, b):
        self.ascend = b

    def start(self):
        #self.updateTransmitThread.start()
        self.updateReceiveThread.start()
    
    def close(self):
        self.ser.close()

    def __del__ (self):
        self.ser.close()

if __name__=='__main__':
    xb = XbRssi('/dev/ttyUSB0')
    #xb.start()
    result = xb.get_max_rssi()
    print "the maximum is: ", result
    result = xb.get_min_rssi()
    print "the minimum is: ", result
    result = xb.get_avg_rssi()
    print "the average is: ", result
    result = xb.get_med_rssi()
    print "the median is: ", result


    #while True:
        # print "RSSI = -%d dBm @ address %d" % ( xb.get_max_rssi(), xb.get_addr() )
      #  time.sleep(0.5)
