class RadishError(Exception):
    pass

class NotFound(RadishError):
    pass

class MethodNotAllowed(RadishError):
    pass

class AlreadyExists(RadishError):
    pass

class DynamicError(RadishError):
    pass