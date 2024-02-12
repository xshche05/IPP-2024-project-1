# Possible params
# --help, print help and return 0 code, NO OTHER PARAMS ALLOWED
import sys

from parser import Parser
from reader import Reader
from my_exceptions import HeaderException, OpCodeException, ArgException


def main():
    reader = Reader(sys.stdin)  # Create reader object
    reader.read_stream()  # Read input stream
    parser = Parser(reader.get_lines())  # Create parser object
    program = parser.parse()  # Parse input data
    print(program, file=sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except HeaderException as e:
        print(e, file=sys.stderr)
        sys.exit(21)
    except OpCodeException as e:
        print(e, file=sys.stderr)
        sys.exit(22)
    except ArgException as e:
        print(e, file=sys.stderr)
        sys.exit(23)
    except Exception:
        print("Unknown error", file=sys.stderr)
        sys.exit(99)
    else:
        sys.exit(0)


