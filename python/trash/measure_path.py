import zc_id
from Xbee import *
from LCMBot import *


if __name__=='__main__':
    rid = zc_id.get_id()
    r0 = LCMBot('{0}/base_cmd'.format(rid))
    #print r0
   # try:
    	#Zumy 1
    #r0.turn90()
    file_name = raw_input("Please input the file name: ")
    f = open(file_name + ".csv", "w")
    xb = XbRssi('/dev/ttyUSB0')

    for j in range(1):
	for i in range(3):
	    r0.drive_in_dist(True, 0.7, 1.2, 1)
            rssi, rssi_list = xb.get_max_rssi()
            f.write("Position #" + str(i) + "rssi = " + str(rssi) + " " + str(rssi_list) + "\n")
        f.write("REVERSE")
	#r0.turn90()
	#r0.turn90()
        for i in range(3):
	    r0.drive_in_dist(False, 2.3, 0.9, 0.9)
	    #r0.drive_in_dist(False, 0.7, 1.2, 1.2)
 	    rssi, rssi_list = xb.get_max_rssi()
	    f.write("Position #" + str(i) + "rssi = " + str(rssi) + " " + str(rssi_list) + "\n")
    	#r0.turn90()
	#f.write("TURN90")
    f.close()    
#except:
#	r0.drive(0, 0)
 #   finally:
#	r0.drive(0, 0)
