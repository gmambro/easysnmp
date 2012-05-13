
def hex2dec(i):
    return int(i, 16)

def munge_macaddress_ids(octects):
    """This Function will convert an id sequence to a mac address"""
    return ":".join(map(lambda i: "%02x" % i, octects))

def munge_macaddress(octects):
    """This Function will convert an id sequence to a mac address"""
    return ":".join(map(lambda i: "%02x" % ord(i), octects))


def munge_ipaddress_ids(octects):
    return ".".join(octects)

def munge_ipaddress(octects):
    return ".".join(map(lambda x: str(ord(x)),octects))
