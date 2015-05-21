import zc_id
from Xbee import *
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

        ascending_bot = GAscent(r, xb)
        while True:
            print xb.data
            if xb.ascend == True:
                ascending_bot = GAscent(r, xb)
                ascending_bot.start()
                xb.end_gradient_ascend()
            else: 
                xb.get_max_rssi()
                print "NOT ASCENDING"
            time.sleep(1)

       #s xb.set_transmit_thread(False)
#	while True:
#		if xb.get_ascend_status() == True:	
#        		ascending_bot.start()
"""            ascend = xb.get_ascend_status()

            if ascend == True:
                ascending_bot.start()
                xb.set_ascend(False)
     #           xb.set_receiver_thread(False)
            bestRSSI,rssi_list = xb.get_max_rssi()
            print xb.sendMessage
            time.sleep(3)   """
        	#else:
        #		sentry_bot.start()
       
