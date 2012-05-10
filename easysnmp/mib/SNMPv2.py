from .objects import *
from .module import *

from ..munge import munge_ipaddress_raw

class SNMPv2(MIBModule):

    __oid__  = "1.3.6.1.2.1.1"
    __mib_name__ = "SNMPv2-MIB"

    __objects__ = [
        ScalarObject( "sysDescr",       1  ),
        ScalarObject( "sysObjectID",    2  ),
        ScalarObject( "sysUpTime",      3  ),
        ScalarObject( "sysContact",     4  ),
        ScalarObject( "sysName",        5  ),
        ScalarObject( "sysLocation",    6  ),

        ]


class IFMIB(MIBModule):

    __oid__  = "1.3.6.1.2.1.2"
    __mib_name__ = "IF-MIB"

    __objects__ = [
        ScalarObject(  "ifNumber",      1  ),
        TabularObject( "ifTable",       2,
            {
                    'ifIndex': 1,
                    'ifDescr': 2,
                    'ifType': 3,
                    'ifMtu': 4,
                    'ifSpeed': 5,
                    'ifPhysAddress': 6,
                    'ifAdminStatus': 7,
                    'ifOperStatus': 8,
                    'ifLastChange': 9,
                    'ifInOctets': 10,
                    'ifInUcastPkts': 11,
                    'ifInNUcastPkts': 12,
                    'ifInDiscards': 13,
                    'ifInErrors': 14,
                    'ifInUnknownProtos': 15,
                    'ifOutOctets': 16,
                    'ifOutUcastPkts': 17,
                    'ifOutNUcastPkts': 18,
                    'ifOutDiscards': 19,
                    'ifOutErrors': 20,
                    'ifOutQLen': 21,
                    'ifSpecific': 22,
            })

        ]

