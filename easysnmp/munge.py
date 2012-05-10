
def hex2dec(i):
    return int(i, 16)

def munge_macaddress(octects):
    """This Function will convert a MacAddress octet string"""
    return ":".join(map(lambda i: "%02x" % i, octects))


def munge_ipaddress(octects):
    return ".".join(octects)

def munge_ipaddress_raw(octects):
    return ".".join(map(lambda x: str(ord(x)),octects))
