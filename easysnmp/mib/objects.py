__all__ = [ "ScalarObject", "TabularObject" ]

class MIBObject(object):
    def __init__(self, name, oid_leaf):
        self.name = name
        self.__module = None


        if isinstance(oid_leaf, int):
            oid_leaf = str(oid_leaf)

        if oid_leaf[0] == '/':
            self.__oid      = oid_leaf[1:]
            self.__oid_leaf = None
        else:
            self.__oid_leaf = oid_leaf
            # will be set when added to module
            self.__oid    = None


    def set_module(self, module):
        if self.__module is not None:
            raise RuntimeError("MIBObject already associated to a MIBModule")            
        self.__module = module


    def get_oid(self):
        if self.__oid is not None:
            return self.__oid

        if self.__module is None:
            raise RuntimeError("MIBObject not associated to a MIBModule")

        oid = self.__module.get_oid() + '.' + self.__oid_leaf
        self.__oid = oid
        return oid
        
    def retrieve(self, agent):
        raise NotImplementedError()

class ScalarObject(MIBObject):

    def __init__(self, name, oid_leaf, munger=None):
        super(ScalarObject, self).__init__(name, oid_leaf)
        self.munger = munger


class TabularObject(MIBObject):

    def __init__(self, name, oid_leaf, columns=None, entry_id=1):
        super(TabularObject, self).__init__(name, oid_leaf)
        
        if isinstance(entry_id, int):
            entry_id = str(entry_id)
        self.__entry_id = str(entry_id)
        self.__column_by_name = {}
        self.__column_by_oid  = {}
        self.index_munger = None
        self.columns = []

        if isinstance(columns, list):
            for col in columns:
                self.add_column(col)
        elif isinstance(columns, dict):
            for col_name, col_info in columns.items():
                if isinstance(col_info, list):
                    col = TableColumn(col_name, *col_info)
                elif isinstance(col_info, dict):
                    col = TableColumn(col_name, **col_info)
                elif isinstance(col_info, int):
                    col = TableColumn(col_name, col_info)
                else:
                    raise TypeError("Column specification must be an int, a list or a dictionary. Found %s." % col_info.__class__)
                    
                self.add_column(col)
    

    def add_column(self, col):
        self.__column_by_name[col.name] = col
        self.columns.append(col)

    def set_module(self, module):
        super(TabularObject, self).set_module(module)
        
        for col in self.columns:
            col.oid = ".".join([ self.get_oid(), self.__entry_id, col.oid_leaf])
            self.__column_by_oid[col.oid] = col

    def get_col_by_oid(self, oid):
        return self.__column_by_oid.get(oid)
        

class TableColumn(object):
    def __init__(self, name, oid_leaf, munger=None):
        if isinstance(oid_leaf, int):
            oid_leaf = str(oid_leaf)
        self.name      = name
        self.oid_leaf  = oid_leaf
        self.oid    = None
        self.munger = munger

