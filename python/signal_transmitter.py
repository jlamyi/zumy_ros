import zc_id
from Xbee import *
from LCMBot import *
import time
#from GAscent import *

if __name__ == '__main__':
        #file_name = raw_input("Please input the file name: ") 
        #f = open(file_name+".csv","w")

        rid = zc_id.get_id()
        r = LCMBot('{0}/base_cmd'.format(rid))
        xb = XbRssi('/dev/ttyUSB0')
        xb.start()

#        ascending_bot = GAscent(r, xb)

        #while True:
      #  xb.send_start_ascend_signal()
        while True:
        	data = xb.get_data()
		print data
		if 'Hello' in data:
			break
        	time.sleep(20)
	xb.send_start_transmit_signal()
	while True:
		data = xb.get_data()
		print data
		time.sleep(15)

	
