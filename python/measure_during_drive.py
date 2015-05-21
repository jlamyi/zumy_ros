import zc_id, time, matplotlib, csv
from Xbee import *
from LCMBot import *
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt

if __name__=='__main__':

    # initialize Zumy, XBee, and file handles.
    rid = zc_id.get_id()
    r = LCMBot('{0}/base_cmd'.format(rid))
    xb = XbRssi('/dev/ttyUSB0')
    file_name = raw_input("Please input the file name: ")
    OUTPUT_NAME = file_name + '.csv'
    f = open(OUTPUT_NAME, "w")

    # time
    start_time = time.time()
    driving_time = 7
    
    # ===============================
    # take measurements
    # ===============================
    r.drive(0.18,0.16)  
    i = 0
    while time.time()-start_time < driving_time: 
        rssi_max, rssi_list = xb.get_max_rssi()
        rssi_avg = mean(rssi_list)
        rssi_med = median(rssi_list)
        f.write(str(i) + ", " + str(rssi_max) + ", " + str(rssi_med) + ", " + str(rssi_avg)  + "\n")
        i = i + 1
    r.stop()
    f.close()

    # ===============================
    # plot
    # ===============================

    # initialize plot
    plt.title('Test_plot')
    plt.xlabel('Position')
    plt.ylabel('RSSI (dB)')

    # initialize variables
    t = []
    rssi_max = []
    rssi_med = []
    rssi_avg = []

    # read csv file
    f = open(OUTPUT_NAME,'rb')
    input = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    rssi_data = [[item for number, item in enumerate(row) if item and (0 <= number <= 3)] for row in input]
    for i in range(len(rssi_data)):
        if i == 0:
            t.append(0);
            rssi_max.append(rssi_data[i][0])
            rssi_med.append(rssi_data[i][1])
            rssi_avg.append(rssi_data[i][2])
        else:
            t.append(rssi_data[i][0]);
            rssi_max.append(rssi_data[i][1])
            rssi_med.append(rssi_data[i][2])
            rssi_avg.append(rssi_data[i][3])
    f.close()

    # plot
    plt.plot(t, rssi_max, color='red', linewidth=2.0, linestyle='-', label='$RSSI_{max}$')
    plt.plot(t, rssi_med, color='black', linewidth=2.0, linestyle='-', label='$RSSI_{med}$')
    plt.plot(t, rssi_avg, color='blue', linewidth=2.0, linestyle='-', label='$RSSI_{avg}$')
    plt.legend(loc='upper right')
    plt.savefig(file_name + '.png')
    del t, rssi_max, rssi_med, rssi_avg
    # plt.show()




    

