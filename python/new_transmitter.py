import zc_id
#from Xbee import *
from LCMBot import *
from GAscent import *
from Xbee_chaining_bot import *

if __name__ == '__main__':
        #file_name = raw_input("Please input the file name: ") 
        #f = open(file_name+".csv","w")

        rid = zc_id.get_id()
        r = LCMBot('{0}/base_cmd'.format(rid))
        xb = Xbee_chaining_bot('/dev/ttyUSB0')
        xb.start()
	   #sending = False
	
 #       ascending_bot = GAscent(r, xb)
       #s xb.set_transmit_thread(False)
        xb.send_start_ascend_signal()
        print "DONE"
        while True:
      #      print "DONE"
	    
            xb.transmit_rssi()
            time.sleep(0.1)
            print xb.response
            print 'Transmitting ' + str(xb.sendMessage)
	
