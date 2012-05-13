from .objects import *
from .module import *

from ..munge import munge_ipaddress

class CiscoCDP(MIBModule):

    __oid__  = "1.3.6.1.4.1.9.9.23"
    __mib_name__ = "CISCO-CDP-MIB"

    __objects__ = [
        TabularObject('cdpCacheTable', '1.2.1',
            columns = {
                "cdpCacheAddress"    : [4, munge_ipaddress ],
                "cdpCacheDevicePort" :  7,
                "cdpCacheDeviceId"   :  6,
                "cdpCacheSysName"    : 17,
            })
        ]
