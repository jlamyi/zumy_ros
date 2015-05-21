import zc_id, time, matplotlib, csv
from Xbee import *
from LCMBot import *
from numpy import *
from collections import Counter
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt

if __name__=='__main__':

    # initialize Zumy, XBee, and file handles.
    rid = zc_id.get_id()
    r = LCMBot('{0}/base_cmd'.format(rid))
    xb = XbRssi('/dev/ttyUSB0')
    file_name = raw_input("Please input the file name: ")
    f1 = open("../data/"+file_name+"_stat.csv", "w")
    f2 = open("../data/"+file_name+"_data.csv", "w")

    # time
    start_time = time.time()
    driving_time = 15
    
    # ===============================
    # take measurements
    # ===============================
    # r.drive(0.18,0.16)  
    # i = 0
    # while time.time()-start_time < driving_time: 
    #     rssi_max, rssi_list = xb.get_max_rssi()
    #     rssi_avg = mean(rssi_list)
    #     rssi_med = median(rssi_list)
    #     f.write(str(i) + ", " + str(rssi_max) + ", " + str(rssi_med) + ", " + str(rssi_avg)  + "\n")
    #     i = i + 1
    # r.stop()
    # f.close()

    for i in range(10):
        r.drive_in_dist(True, 0.22, 0.2, 0.6)
        rssi_max, rssi_list = xb.get_max_rssi()
        data  = Counter(rssi_list)
        rssi_min = min(rssi_list)
        rssi_avg = mean(rssi_list)
        rssi_med = median(rssi_list)
        rssi_mode = data.most_common(1)
        rssi_std = std(rssi_list)
        f1.write(str(i) + ", " + str(rssi_max) + ", " + str(rssi_min) + ", " + str(rssi_avg) + ", " + str(rssi_med) + ", " + str(rssi_std) + "\n")
        f2.write(str(rssi_list) + "\n")
    f1.close()
    f2.close()

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
    rssi_min = []
    rssi_avg = []
    rssi_med = []
    
    # read csv file
    f1 = open("../data/"+file_name+"_stat.csv", "rb")
    input = csv.reader(f1, quoting=csv.QUOTE_NONNUMERIC)
    rssi_data = [[item for number, item in enumerate(row) if item and (0 <= number <= 4)] for row in input]
    for i in range(len(rssi_data)):
        if i == 0:
            t.append(0);
            rssi_max.append(rssi_data[i][0])
            rssi_min.append(rssi_data[i][1])
            rssi_avg.append(rssi_data[i][2])
            rssi_med.append(rssi_data[i][3])

        else:
            t.append(rssi_data[i][0])
            rssi_max.append(rssi_data[i][1])
            rssi_min.append(rssi_data[i][2])
            rssi_avg.append(rssi_data[i][3])
            rssi_med.append(rssi_data[i][4])
    f1.close()

    # plot
    plt.plot(t, rssi_max, color='red', linewidth=2.0, linestyle='-', label='$RSSI_{max}$')
    plt.plot(t, rssi_med, color='black', linewidth=2.0, linestyle='-', label='$RSSI_{med}$')
    plt.plot(t, rssi_avg, color='blue', linewidth=2.0, linestyle='-', label='$RSSI_{avg}$')
    plt.plot(t, rssi_min, color='purple', linewidth=2.0, linestyle='-', label='$RSSI_{min}$')
    plt.legend(loc='lower right')
    plt.savefig("../figure/" + file_name + '.png')
    del t, rssi_max, rssi_min, rssi_avg, rssi_med, rssi_std
    plt.show()




    



