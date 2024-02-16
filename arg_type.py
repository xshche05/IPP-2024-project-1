from enum import Enum


class ArgType(Enum):
    INT = 1
    BOOL = 2
    STRING = 3
    NIL = 4
    LABEL = 5
    TYPE = 6
    VAR = 7
    FLOAT = 9
    SYMB = 8

    def __eq__(self, other) -> bool:
        """
        :param other: ArgType - required type
        :return: True if self is of the same type as other or if other is SYMB and self is VAR, INT, BOOL, STRING or NIL
        """
        if isinstance(other, ArgType):
            if other.value == ArgType.SYMB.value:
                return self in [ArgType.VAR, ArgType.INT, ArgType.BOOL, ArgType.STRING, ArgType.NIL, ArgType.FLOAT]
            return self.value == other.value
        return False

    def __str__(self) -> str:
        return self.name.lower()

    def __hash__(self) -> int:
        return hash(self.value)
