import zc_id
from Xbee import *
from LCMBot import *


if __name__=='__main__':
    rid = zc_id.get_id()
    r0 = LCMBot('{0}/base_cmd'.format(rid))
    xb = XbRssi('/dev/ttyUSB0')
    xb.start()
    try:
        while True:
            lastRSSI = xb.get_rssi()
            while(lastRSSI<45):
                r0.drive(.1,.1)
                print "RSSI = -%d dBm @ address %d" % ( xb.get_rssi(), xb.get_addr() )
                print "running"
                lastRSSI = xb.get_rssi()
                time.sleep(0.5)
            r0.drive(0,0)
            print "RSSI = -%d dBm @ address %d" % ( xb.get_rssi(), xb.get_addr() )
            print "stopped"
            time.sleep(0.5)
    except:
        r0.drive(0, 0)
    finally:
        r0.drive(0, 0)
