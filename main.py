# Possible params
# --help, print help and return 0 code, NO OTHER PARAMS ALLOWED
import sys

from sys_arg_parser import ArgParser
from parser import Parser
from reader import Reader
from my_exceptions import HeaderException, OpCodeException, OtherSyntaxLexicalException, SysArgException, StatGroupException


def main():
    arg_parser = ArgParser(sys.argv[1:])  # Create arg_parser object
    arg_parser.parse_to_groups()  # Parse system arguments
    reader = Reader(sys.stdin)  # Create reader object
    reader.read_stream()  # Read input stream
    parser = Parser(reader.get_lines())  # Create parser object
    program = parser.parse()  # Parse input data
    print(program, file=sys.stdout)  # Print program to stdout

    # Fill statistics
    for group in arg_parser.stat_groups:
        program.load_stats_to(group)  # Load statistics to group
        group.write_to_file()  # Write statistics to file


if __name__ == "__main__":
    main()
    # try:
    #     main()
    # except HeaderException as e:
    #     print(e, file=sys.stderr)
    #     sys.exit(21)
    # except OpCodeException as e:
    #     print(e, file=sys.stderr)
    #     sys.exit(22)
    # except OtherSyntaxLexicalException as e:
    #     print(e, file=sys.stderr)
    #     sys.exit(23)
    # except SysArgException as e:
    #     print(e, file=sys.stderr)
    #     sys.exit(10)
    # except StatGroupException as e:
    #     print(e, file=sys.stderr)
    #     sys.exit(12)
    # except Exception:
    #     print("Unknown error", file=sys.stderr)
    #     sys.exit(99)
    # else:
    #     sys.exit(0)


