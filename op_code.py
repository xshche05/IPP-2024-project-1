from enum import Enum
from arg_type import ArgType
from my_exceptions import OpCodeException


class OpCode(Enum):
    # No args
    CREATEFRAME = 1
    PUSHFRAME = 2
    POPFRAME = 3
    RETURN = 4
    BREAK = 5

    # 1 var arg
    DEFVAR = 6
    POPS = 7

    # 1 symb arg
    PUSHS = 8
    WRITE = 9
    EXIT = 10
    DPRINT = 11

    # 1 label arg
    CALL = 12
    LABEL = 13
    JUMP = 14

    # 1 var, 1 symb arg
    MOVE = 15
    STRLEN = 16
    TYPE = 17
    NOT = 18
    INT2CHAR = 19

    # 1 var, 1 type arg
    READ = 20

    # 1 var, 2 symb args
    ADD = 21
    SUB = 22
    MUL = 23
    IDIV = 24
    LT = 25
    GT = 26
    EQ = 27
    AND = 28
    OR = 29
    STRI2INT = 30
    CONCAT = 31
    GETCHAR = 32
    SETCHAR = 33

    # 1 label, 2 symb args
    JUMPIFEQ = 34
    JUMPIFNEQ = 35

    @property
    def params(self) -> list[ArgType]:
        """
        :return: Returns a list of ArgType that the OpCode needs
        """
        if self in [OpCode.CREATEFRAME, OpCode.PUSHFRAME, OpCode.POPFRAME, OpCode.RETURN, OpCode.BREAK]:
            return []
        elif self in [OpCode.DEFVAR, OpCode.POPS]:
            return [ArgType.VAR]
        elif self in [OpCode.PUSHS, OpCode.WRITE, OpCode.EXIT, OpCode.DPRINT]:
            return [ArgType.SYMB]
        elif self in [OpCode.CALL, OpCode.LABEL, OpCode.JUMP]:
            return [ArgType.LABEL]
        elif self in [OpCode.MOVE, OpCode.STRLEN, OpCode.TYPE, OpCode.NOT, OpCode.INT2CHAR]:
            return [ArgType.VAR, ArgType.SYMB]
        elif self in [OpCode.READ]:
            return [ArgType.VAR, ArgType.TYPE]
        elif self in [OpCode.JUMPIFEQ, OpCode.JUMPIFNEQ]:
            return [ArgType.LABEL, ArgType.SYMB, ArgType.SYMB]
        elif self in [OpCode.ADD, OpCode.SUB, OpCode.MUL, OpCode.IDIV, OpCode.LT, OpCode.GT, OpCode.EQ, OpCode.AND,
                      OpCode.OR, OpCode.STRI2INT, OpCode.CONCAT, OpCode.GETCHAR, OpCode.SETCHAR]:
            return [ArgType.VAR, ArgType.SYMB, ArgType.SYMB]
        else:
            raise OpCodeException("Unknown OpCode")

    def __str__(self) -> str:
        return self.name.upper()
