from .objects import *
from .module import *

from ..munge import munge_ipaddress_raw

class CiscoCDP(MIBModule):

    __oid__  = "1.3.6.1.4.1.9.9.23.1"
    __mib_name__ = "CISCO-CDP-MIB"

    __objects__ = [
        TabularObject('cdpCacheTable', '2.1',
            columns = {
                "cdpCacheAddress"    : [4, munge_ipaddress_raw ],
                "cdpCacheDevicePort" :  7,
                "cdpCacheDeviceId"   :  6,
                "cdpCacheSysName"    : 17,
            })
        ]
