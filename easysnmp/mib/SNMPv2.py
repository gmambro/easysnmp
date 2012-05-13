from .objects import *
from .module import *

from ..munge import munge_macaddress

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

    __oid__  = "1.3.6.1.2.1.31"
    __mib_name__ = "IF-MIB"

    __objects__ = [
        ScalarObject(  "ifNumber", "/1.3.6.1.2.1.2.1"),
        TabularObject( "ifTable",  "/1.3.6.1.2.1.2.2",
            {
                    'ifIndex': 1,
                    'ifDescr': 2,
                    'ifType': 3,
                    'ifMtu': 4,
                    'ifSpeed': 5,
                    'ifPhysAddress': [6, munge_macaddress ],
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
            }),
        TabularObject( "ifXTable",       "1.1",
            {
                'ifName':                  1, 
                'ifInMulticastPkts':       2,
                'ifInBroadcastPkts':       3,
                'ifOutMulticastPkts':      4,
                'ifOutBroadcastPkts':      5,
                'ifHCInOctets':            6,
                'ifHCInUcastPkts':         7,
                'ifHCInMulticastPkts':     8,
                'ifHCInBroadcastPkts':     9,
                'ifHCOutOctets':          10,
                'ifHCOutUcastPkts':       11,  
                'ifHCOutMulticastPkts':   12,
                'ifHCOutBroadcastPkts':   13,
                'ifLinkUpDownTrapEnable': 14,
                'ifHighSpeed':            15,
                'ifPromiscuousMode':      16,
                'ifConnectorPresent':     17,
                'ifAlias':                18,
                'ifCounterDiscontinuityTime':  19,
            })
        ]


class Bridge(MIBModule):

    __oid__  = "1.3.6.1.2.1.17"
    __mib_name__ = "Bridge-MIB"

    __objects__ = [

        # .1 dot1dBase 
        ScalarObject(  "dot1dBaseBridgeAddress", "1.1", munge_macaddress  ),
        ScalarObject(  "dot1dBaseNumPorts",      "1.2"  ),
        TabularObject( "dot1dBasePortTable",     "1.4", {
              "dot1dBasePort" : 1,
              "dot1dBasePortIfIndex": 2
            }),

        # .4 to1dTp
        TabularObject( "dot1dTpFdbEntry",     "4.3", {
                "dot1dTpFdbAddress" : 1,
                "dot1dTpFdbPort": 2,
                "dot1dTpFdbStatus": 3,
            })
    
    ]
