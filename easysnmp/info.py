from pysnmp.entity.rfc3413.oneliner import cmdgen

from .munge import *
from .client import snmpget, snmpwalk
from .exceptions import SNMPError


OIDS = {
    "sysName" : (1,3,6,1,2,1,1,5),
        
    # IF-MIB
    "ifName" : (1,3,6,1,2,1,31,1,1,1,1),
        

    # in  "dot1dTpFdbTable"   : (1,3,6,1,2,1,17,4,3),
    "dot1dTpFdbAddress" : (1,3,6,1,2,1,17,4,3,1,1),
    "dot1dTpFdbPort"    : (1,3,6,1,2,1,17,4,3,1,2),

    # in "dot1dTpPortTable" 
    "dot1dBasePortIfIndex" : (1,3,6,1,2,1,17,1,4,1,2),

    # CISCO-CDP
   "cdpCacheAddress"    :       (1,3,6,1,4,1,9,9,23,1,2,1,1,4),
   "cdpCacheDevicePort" :       (1,3,6,1,4,1,9,9,23,1,2,1,1,7),
   "cdpCacheDeviceId"   :       (1,3,6,1,4,1,9,9,23,1,2,1,1,6),
   "cdpCacheCapabilities" :     (1,3,6,1,4,1,9,9,23,1,2,1,1,9),
   "cdpCacheSysName"    :       (1,3,6,1,4,1,9,9,23,1,2,1,1,17),
 }


# decorator for SNMPInfo 
def cached_info(fn):
    def wrapper(self):
        name = fn.__name__     
        try:
            value = self._snmp_cache[name]
        except (KeyError, AttributeError):
            value = fn(self)
            try:
                cache = self._snmp_cache
            except AttributeError:
                cache = self._snmp_cache = {}
            cache[name] = value
        return value
    return wrapper

class SNMPInfo(object):

    def __init__( self, device, community ):
        self.device = device
        self.community = community
   
    @cached_info
    def get_sysname(self):
        ret = snmpget( self.device, self.community, OIDS["sysName"] +(0,) )
        sysname = str(ret[0][1])
        return sysname

    @cached_info 
    def get_ifname(self):
        ifname_map = {}
        ifname  = snmpwalk( self.device, self.community, OIDS["ifName"] )
        for e in ifname:
           ifname_map[ str(e[0][0][-1]) ] = str(e[0][1])

        return ifname_map

    def get_fw_table(self, vlan=None) :
        if hasattr(self, '_fw_table'):
            return self._fw_table

        community = self.community
        if vlan is not None:
            community = community + '@' + str(vlan)

        fwport_table  = snmpwalk( self.device, community, OIDS["dot1dTpFdbPort"] )
        brport_table  = snmpwalk( self.device, community, OIDS["dot1dBasePortIfIndex"] )

        brport_map = {}
        for e in brport_table:
             brport_map[ str(e[0][0][-1]) ] = str(e[0][1])
    
        fw_table = {}
        ifname = self.get_ifname()
        for e in fwport_table:
             macaddr = munge_macaddress(list(e[0][0][-6:]))
             fw_table[macaddr] = ifname [ brport_map [ str( e[0][1] ) ] ]

        self._fw_table = fw_table
        return fw_table

    @cached_info
    def get_cdp_cache(self):
        community = self.community
        device = self.device

        cdp_port = snmpwalk( device, community, OIDS["cdpCacheDevicePort" ])
        cdp_name = snmpwalk( device, community, OIDS["cdpCacheDeviceId"] )
        cdp_addr = snmpwalk( device, community, OIDS["cdpCacheAddress"])

        assert (len(cdp_name) == len(cdp_addr) and
                len(cdp_name) == len(cdp_port))
   
        cdp_cache = []
        for (name, addr, port) in zip(cdp_name, cdp_addr, cdp_port):
            if_index, device_id = str(name[0][0][-2]), str(name[0][0][-1])
      
            cdp_cache.append({
                        'local_port' : self.get_ifname()[if_index], 
                        'hostname': str(name[0][1]),
                        'address': munge_ipaddress(addr[0][1]),
                        'remote_port': str(port[0][1]) })
        return cdp_cache


