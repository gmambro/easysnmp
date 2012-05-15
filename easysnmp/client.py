from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.rfc1905 import NoSuchInstance


from .exceptions import SNMPError
from .mib.objects import *

# TODO support partial columns fetch
def get_table(addr, comm, mib_table, columns=[]):
    
    oid = mib_table.get_oid()
    oid_l = len(oid.split("."))

    result_table = {}

    if mib_table.index_munger:
        idx_munger = mib_table.index_munger
    else:
        idx_munger = str

    t = snmpwalk(addr, comm, oid)
    
    for r in t:
        id, val = r[0][0], r[0][1]
        col_oid = str( id[: oid_l + 2])
        col_obj = mib_table.get_col_by_oid(col_oid)
        if col_obj is None:
            continue

        row_idx = id[oid_l + 2 : ]
        munged_row_idx = idx_munger(row_idx)
 
        if col_obj.munger:
            val = col_obj.munger(val)
        else:
            val = str(val)

        result_row = result_table.setdefault(str(row_idx), 
                                            { 'index' : munged_row_idx })
        result_row[col_obj.name] = val

    return result_table

def get_scalar(addr, comm, mib_scalar):
        
    oid = mib_scalar.get_oid() + ".0"
    ret_oid, ret_val = snmpget( addr, comm, oid )[0]

    if isinstance(ret_val, NoSuchInstance):
        return None

    if mib_scalar.munger:
        ret_val = mib_scalar.munger(ret_val)
    else:
        ret_val = str(ret_val)

    return ret_val

def snmpwalk( addr, comm, oid  ):  
    """This function will return the table of OID's that I am walking"""
    errorIndication, errorStatus, errorIndex, generic = \
        cmdgen.CommandGenerator().nextCmd(cmdgen.CommunityData('test-agent', comm), \
                                        cmdgen.UdpTransportTarget((addr, 161)), oid)

    if errorIndication:
        raise SNMPError(indication=errorIndication)
    elif errorStatus:
        raise SNMPError(status=errorStatus, 
                        location=generic[int(errorIndex)-1] )

    return generic

def snmpget(addr, comm, oid  ):

    errorIndication, errorStatus, errorIndex, generic = \
        cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', comm), \
                                        cmdgen.UdpTransportTarget((addr, 161)), oid )

    if errorIndication:
        raise SNMPError(indication=errorIndication)
    elif errorStatus:
        raise SNMPError(status=errorStatus, 
                        location=generic[int(errorIndex)-1] )

    return generic

