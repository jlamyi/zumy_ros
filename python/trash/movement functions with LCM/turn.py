import zc_id
from Xbee import *
from LCMBot import *


if __name__=='__main__':
    rid = zc_id.get_id()
    r0 = LCMBot('{0}/base_cmd'.format(rid))
    print r0
   # try:
    	#Zumy 1
    r0.turn90()
    r0.drive(0, 0)
    #except:
#	r0.drive(0, 0)
 #   finally:
#	r0.drive(0, 0)
