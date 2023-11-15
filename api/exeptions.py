class DuplicateEntry(Exception):
    "Raised when an SQL entry already exists"
    __name__ = "Duplicate Entry"
    pass

class DBerror(Exception):
    pass
