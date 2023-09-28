class ParseError(Exception):
    pass


class ParameterTypeError(Exception):
    """
    This error is raised when :func:`nest` encounters parameters with
    conflicting types.
    """
