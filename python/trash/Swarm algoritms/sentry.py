import zc_id
#from Xbee import *
from LCMBot import *
from GAscent import *
from Xbee_chaining_bot import *

if __name__ == '__main__':

        rid = zc_id.get_id()
        r = LCMBot('{0}/base_cmd'.format(rid))
        xb = Xbee_chaining_bot('/dev/ttyUSB0')
        xb.transmit = False
        xb.start()
        
        while True:
           
            time.sleep(0.1)
            print xb.response
            if xb.transmit == True:
                xb.transmit_rssi()
                print 'Transmitting ' + str(xb.sendMessage)
	    else:
                print 'Sentry Mode'
                time.sleep(1)
