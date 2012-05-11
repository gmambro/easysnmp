from .objects import *
from .module import *

class CiscoVTP(MIBModule):

    __oid__  = "1.3.6.1.4.1.9.9.46"
    __mib_name__ = "CISCO-VTP-MIB"

    __objects__ = [
        TabularObject('vtpVlanTable', '1.3.1',
            columns = {
                "vtpVlanIndex": 1,
                "vtpVlanState": 2,
                "vtpVlanType": 3,
                "vtpVlanName": 4,
            }),
        ]
