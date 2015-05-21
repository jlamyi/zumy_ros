import time, lcm, fearing
from fearing import base_cmd


class LCMBot:
	def __init__(self, base_cmd_channel):
		self.lcm=lcm.LCM('udpm://239.255.76.67:7667?ttl=1')
		self.base_cmd_channel = base_cmd_channel
		self.msg=base_cmd()
		self.msg.header = fearing.header()

		self.turn90_time = 0.55
		self.turn90_left = -.18
		self.turn90_right = .18

	def drive(self, l, r):
		self.msg.left_cmd=l
		self.msg.right_cmd=r
		self.lcm.publish(self.base_cmd_channel, self.msg.encode())

	def turn90(self, dir = True):
		try:
			if dir:
				self.drive(self.turn90_left, self.turn90_right)
			else:
				self.drive(-self.turn90_left, -self.turn90_right)
			time.sleep(self.turn90_time)
			self.stop()
		except:
			self.stop()
		finally:
			self.stop()
			time.sleep(.1)

	def drive_in_dist(self, dir, left, right, t):
		try:
			if (dir == True):
				self.drive(left, right)
			elif (dir == False):
				self.drive(-left, -right)
			time.sleep(t)
			self.stop()
		except:
			self.stop()
		finally:
			self.stop()
			time.sleep(.1)
			
	def stop(self):
		self.drive(0, 0)


if __name__=='__main__':
	r0 = LCMBot('/01/base_cmd')
	r0.drive(.9,.9)
	time.sleep(1)
	r0.drive(0,0)
