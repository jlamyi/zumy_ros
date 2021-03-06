# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 06:32:45 2014

@author: ajc
"""

from mbedrpc import *
from fearing import base_cmd
from fearing import carrier_state
from fearing import header
from fearing import xbee
import zumy
import time
import threading
import zc_id
import lcm
import lcm_refresh
import xb.XbRssi

class ZumyLCMNode:
    def __init__(self, robot, lcm, base_cmd_channel, carrier_state_channel, xbee_channel):
        self.robot = robot
        self.lcm = lcm
        self.lcm.subscribe(base_cmd_channel, self.handle_base_cmd)
        self.base_cmd_channel = base_cmd_channel
        self.carrier_state_channel = carrier_state_channel
	self.xbee_channel = xbee_channel
        self.health_thread=threading.Thread(target=self._health_loop)
        self.health_thread.daemon=True
    
    def handle_base_cmd(self, chan, data):
        msg = base_cmd.decode(data)
        print 'handle_base_cmd', msg.left_cmd, msg.right_cmd
        self.robot.cmd(msg.left_cmd, msg.right_cmd)
        
    def start(self):
        self.health_thread.start()
    
    def _health_loop(self):
        volt=0
        msg = carrier_state()
        msg.header=header()
        msg.header.seq=0

	xbee_msg = xbee()        
	xbee_msg.header = header()
	xbee_msg.header.seq = 0

        while True:
            msg.header.seq+=1
            msg.header.time=time.time()
            volt = .9*self.robot.read_voltage() + .1*volt
            msg.battery_voltage=volt

	    xbee_msg.header.seq +=1
	    xbee_msg.header.time = time.time()
            xbee_msg.rssi = xb_rssi.getRssi()
            xbee_msg.addr = xb_rssi.getAddr()
            # print 'rssi = ' + str(xbee_msg.rssi) + '@ address ' + str(xbee_msg.addr)
            try:
                self.lcm.publish(self.carrier_state_channel, msg.encode())
		self.lcm.publish(self.xbee_channel, xbee_msg.encode())
            except IOError, e:
                print e
            time.sleep(.5)

if __name__=='__main__':
    print 'starting zumy lcm node...'
    z=zumy.Zumy('/dev/ttyACM0')
    z.cmd(.1,.1)
    z.cmd(0,0)

    rid = zc_id.get_id()
    cmd_channel='{0}/base_cmd'.format(rid)
    health_channel='{0}/carrier_state'.format(rid)
    xbee_channel = '{0}/xbee'.format(rid)
    xb_rssi = xb.XbRssi.XbRssi('/dev/ttyUSB0')   
    xb_rssi.start()
    print 'receiving base commands on channel=' + cmd_channel
    print 'transmitting health messages on channel=' + health_channel
    
    lc = None
    while lc is None:
        try:
            lc = lcm.LCM('udpm://239.255.76.67:7667?ttl=1')
        except RuntimeError as e:
            print("couldn't create LCM:" + str(e))
            time.sleep(1)
    print("LCM connected properly!")
    
    
    zn=ZumyLCMNode(z, lc, cmd_channel, health_channel, xbee_channel)
    zn.start()
    print 'zumy_lcm_node runnning...'
    
    lcmr = lcm_refresh.LCM_Refresher()
    lcmr.start()
    
    while True:
        
        lc.handle()
        time.sleep(.01)

    
