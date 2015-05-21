import zc_id
from Xbee import *
from LCMBot import *


if __name__=='__main__':
    rid = zc_id.get_id()
    r = LCMBot('{0}/base_cmd'.format(rid))
    print r

    r.stop()
