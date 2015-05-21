import zc_id
from Xbee import *
from LCMBot import *
import time


if __name__=='__main__':
    rid = zc_id.get_id()
    xb = XbRssi('/dev/ttyUSB0')
    xb.start()
    xb.stop_transmit()
    f = open("data.csv","w")
    try:
        i = 0
        while True:
            last_RSSI = xb.get_rssi()
            last_addr = xb.get_addr()
            data = str(last_addr) + ", " + str(i) + ", -" + str(last_RSSI) + "\n"
            print "RSSI = -%d dBm @ address %d" % ( last_RSSI, last_addr )
            f.write(data)
            i = i + 1
            time.sleep(1)
            xb.decode_msg()
            #if i%3 == 0:
                #xb.start_transmit()
            #else:
                #xb.stop_transmit()


    except KeyboardInterrupt:
        pass
    finally:
        f.close()