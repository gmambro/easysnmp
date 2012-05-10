class SNMPError(Exception):
    def __init__(self, indication=None, status=None, location=None):
        if status is None and indication is None:
            raise ParamError()
        self.indication = indication
        self.status = status
        self.location = location

    def __str__(self):
        if self.indication:
            return str(self.indication)
        else:
            return '%s at %s\n' % (
                self.status.prettyPrint(), self.location
            )
