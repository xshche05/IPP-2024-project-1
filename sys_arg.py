from enum import Enum


class SysArgEnum(Enum):
    """
    Enum for system arguments
    """
    HELP = 1  # --help - print help message
    STATS = 2  # --stats=file - print statistics to file
    LOC = 3  # --loc - print lines of code
    COMMENTS = 4  # --comments - print comments count
    LABELS = 5  # --labels - print labels count
    JUMPS = 6  # --jumps - print jumps count
    FWJUMPS = 7  # --fwjumps - print forward jumps count
    BACKJUMPS = 8  # --backjumps - print backward jumps count
    BADJUMPS = 9  # --badjumps - print bad jumps count
    FREQUENT = 10  # --frequent - print most frequent instruction
    PRINT = 11  # --print=STRING - print STRING
    EOL = 12  # --eol - print EOL

    def __str__(self) -> str:
        return self.name.lower()

    def __hash__(self) -> int:
        return hash(self.value)


class SysArg:

    def __init__(self, arg: SysArgEnum, value: str = None):
        self.__arg = arg
        self.__value = value

    @property
    def arg(self) -> SysArgEnum:
        return self.__arg

    @property
    def value(self) -> str:
        return self.__value

    def set_value(self, value: int) -> None:
        self.__value = str(value)

    def __str__(self):
        if self.__value != "\n":
            return f"{self.__arg}=`{self.__value}`"
        return f"{self.__arg}=" + r"`\n`"
