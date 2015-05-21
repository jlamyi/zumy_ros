import zc_id
from LCMBot import *

from Xbee import *
from Xbee_chaining_bot import *
from Xbee_multiBot import *

from GAscent import *
from GDscent import *
from GAscent_beta import *
from GAscent_beta_plus import *
from GDscent_multiBot import *

if __name__ == '__main__':

        rid = zc_id.get_id()
        r = LCMBot('{0}/base_cmd'.format(rid))
        # xb = XbRssi('/dev/ttyUSB0')
        xb = Xbee_multiBot('/dev/ttyUSB0')
        xb.start()

        #try:
            #ascending_bot = GAscent(r,xb)
            #ascending_bot.start()

            #ascending_bot = GAscent_beta(r,xb)
            #ascending_bot.start()

            #ascending_bot = GAscent_beta_plus(r,xb)
            #ascending_bot.start()

            #dscending_bot = GDscent(r, xb)
            #dscending_bot.start()

        dscending_bot = GDscent_multiBot(r, xb)
        dscending_bot.start()
        '''    
        except:
            r.stop()
        finally:
            r.stop()
        '''
