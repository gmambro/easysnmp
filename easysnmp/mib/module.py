__all__ = [ "MIBModule", "ModuleRegistry" ]

import logging
logger = logging.getLogger(__name__)

class ModuleRegistry(object):
    module_by_name = dict()
    module_by_oid  = dict()
    
    @staticmethod
    def add(mod_oid, mod_name, mod_cls):
        ModuleRegistry.module_by_name[mod_name] = mod_cls
        ModuleRegistry.module_by_oid[mod_oid]   = mod_cls


class MIBModuleClass(type):
    
    def __new__(cls, name, bases, dct):
        logger.debug( "New MIB %s (%s): ", name, cls )
        if '__metaclass__' in dct:
            return type.__new__(cls, name, bases, dct)

        oid         = dct['__oid__']
        module_name = dct['__mib_name__']
        #TODO check oid and name, raise exceptio on programming error

        ModuleRegistry.add(oid, module_name, cls)
        MIBModuleClass.register_objects(dct)
        
        cls_type = type.__new__(cls, name, bases, dct)

        MIBModuleClass.setup_objects(cls_type, dct)

        return cls_type

    @staticmethod
    def register_objects(dct):
        objs = dct['__objects__']
        for o in objs:
            name = o.name
            dct[name] = o

    @staticmethod
    def setup_objects(cls_type, dct):
        objs = dct['__objects__']
        for o in objs:
            o.set_module(cls_type)

    __repr__ = lambda c: c.__name__


class MIBModule(object):

    __metaclass__ = MIBModuleClass

    _instance = None
    @classmethod
    def instance(cls):
        if cls._instance:
            return cls._instance
        inst = cls._instance = cls()
        return inst

    @classmethod
    def get_oid(cls):
        return cls.__oid__

    @classmethod
    def get_name(cls):
        return cls.__name__

