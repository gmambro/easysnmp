from ..mib.SNMPv2 import SNMPv2, IFMIB


def build_accessor(obj):

    def _accessor(self):
        print obj.name
    
    return _accessor

class SNMPAgentClass(type):

    def __new__(cls, name, bases, dct):
        for m in dct['__mibs__']:
            dct[m.__name__] = m
            
            for o in m.get_objects():
                dct[o.name] = build_accessor(o)
            
        return type.__new__(cls, name, bases, dct)



class SNMPAgent(object):

    __metaclass__ = SNMPAgentClass
    
    __mibs__  = [SNMPv2, IFMIB ]

    def __init__(self):
        pass

from ..mib.CiscoCDP import CiscoCDP
class SNMPTest(SNMPAgent):

    __mibs__ = [ CiscoCDP ]
