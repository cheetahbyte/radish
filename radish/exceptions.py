class RadishError(Exception):
    pass

class NotFound(RadishError):
    pass

class MethodNotAllowed(RadishError):
    pass