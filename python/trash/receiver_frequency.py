from xbee import XBee
import serial, time, zc_id

import numpy as np

def main():
    """
    Sends an API AT command to read the lower-order address bits from 
    an XBee Series 1 and looks for a response
    """
    ser = serial.Serial('/dev/ttyUSB0', 57600)
    xbee = XBee(ser)
    rid = zc_id.get_id()
    rid = rid.split("/",1)[1] 
    xbee.at(frame='A', command='MY', parameter='\x20'+chr(int(rid)))
    xbee.at(frame='B', command='CH', parameter='\x0e')
    xbee.at(frame='C', command='ID', parameter='\x99\x99')


    sample = 30

    ch1_list = []
    ch6_list = []
    ch11_list = []
    f = open("data.csv","w")    
    try:
        i = 0
        while(1):

            xbee.at(frame='B', command='CH', parameter='\x0e')
            response = xbee.wait_read_frame()
            #print response
            lastRSSI = ord(response.get('rssi'))
            lastAddr = response.get('source_addr')
            ch1_list.append(lastRSSI)
            if len(ch1_list) > sample:
                ch1_list = []
            #print "RSSI = -%d dBm @ %d at index %d" % (lastRSSI,ord(lastAddr[1]), i)
            #data = str(i) + ", -" + str(lastRSSI) +"\n"
            #f.write(data)
            #i = i+1

            xbee.at(frame='B', command='CH', parameter='\x13')
            response = xbee.wait_read_frame()
            #print response
            lastRSSI = ord(response.get('rssi'))
            lastAddr = response.get('source_addr')
            ch6_list.append(lastRSSI)
            if len(ch6_list) > sample:
                ch6_list = []


            xbee.at(frame='B', command='CH', parameter='\x18')
            response = xbee.wait_read_frame()
            #print response
            lastRSSI = ord(response.get('rssi'))
            lastAddr = response.get('source_addr')
            ch11_list.append(lastRSSI)
            if len(ch11_list) > sample:
                ch11_list = []
            
            if len(ch1_list) == sample:
                print "ch1_list max: ", max(ch1_list), " std: ", np.std(ch1_list)
                print "ch6_list max: ", max(ch6_list), " std: ", np.std(ch6_list)
                print "ch11_list max: ", max(ch11_list), " std: ", np.std(ch11_list)
                std = [np.std(ch1_list),np.std(ch6_list),np.std(ch11_list)]

                for i in range(3):
                    if std[i] == min(std):
                        break
                
                if i == 0:
                    print "result: ", max(ch1_list)
                if i == 1:
                    print "result: ", max(ch6_list)
                if i == 2:
                    print "result: ", max(ch11_list)

                print  " "

    except KeyboardInterrupt:
        pass
    finally:
        f.close()
        ser.close()

if __name__ == '__main__':
    main()
