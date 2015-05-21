#/usr/bin/python

import rospy

from geometry_msgs.msg import Twist
from threading import Condition

class ZumyROS:	
  def __init__(self):
    rospy.init_node('zumy_ros')
    self.cmd = (0,0)
    rospy.Subscriber('cmd_vel', Twist, self.cmd_callback)
    self.lock = threading.Condition()
    self.rate = rospy.Rate(30.0)
    self.zumy = Zumy()

  def cmd_callback(self, msg):
    lv = 0.6
    la = 0.4
    v = msg.linear.x
    a = msg.angular.z
    r = lv*v + la*(abs(a) + a)/2
    l = lv*v + la*(abs(a) - a)/2
    self.lock.acquire()
    self.cmd = (r,l)
    self.lock.release()

  def run(self):
    while not rospy.is_shutdown():
      self.lock.acquire()
      self.zumy.cmd(self.cmd)
      self.lock.release()
      self.rate.sleep()

if __name__ == '__main__':
  zr = ZumyROS()
  zr.run()
