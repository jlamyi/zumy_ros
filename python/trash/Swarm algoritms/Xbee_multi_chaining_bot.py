import time, threading, serial
#from numpy import *
#from Xbee import XbRssi

from Xbee_chaining_bot import Xbee_chaining_bot
from Xbee_multiBot import Xbee_multiBot

class Xbee_multi_chaining_bot(Xbee_chaining_bot, Xbee_multiBot):
    
