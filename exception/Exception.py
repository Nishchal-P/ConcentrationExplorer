class MyException(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(MyException):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

class TransitionError(MyException):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        prev -- state at beginning of transition
        next -- attempted new state
        msg  -- explanation of why the specific transition is not allowed
    """

    def __init__(self, prev, next, msg):
        self.prev = prev
        self.next = next
        self.msg = msg

class NoEyesDetected(MyException):
    def __init__(self, msg):
        self.msg = msg

class ListEmpty(MyException):
    def __init__(self, msg):
        self.msg = msg

class ListError(MyException):
    def __init__(self, msg):
        self.msg = msg

class UnknownID(MyException):
    def __init__(self, msg):
        self.msg = msg