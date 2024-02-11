# Possible params
# --help, print help and return 0 code, NO OTHER PARAMS ALLOWED
import sys

from instruction import Instruction
from argument import Argument
from op_code import OpCode
from program import Program
from my_exceptions import HeaderException, OpCodeException, ArgException


def main():
    program = Program()  # Create program object
    code = sys.stdin.read().splitlines()  # Read input code
    look_for_header = True  # Flag for header check

    for line in code:
        instruction, *comment = line.split('#', 1)  # Split instruction and comment
        instruction = instruction.lstrip().rstrip()  # Remove leading and trailing whitespaces

        if instruction == '':  # Skip empty lines
            continue

        if look_for_header:  # Check for header, if first non-empty (non_comment) line is not header, exit with error
            if instruction != '.IPPcode24':
                raise HeaderException("Header not found")
            look_for_header = False
            continue

        # Split instruction to op_code and args
        op_code, args = (instruction.split()[0].upper(),instruction.split()[1:])

        # Check if OpCode is valid, if not, exit with error
        if op_code not in [op.name for op in OpCode]:
            raise OpCodeException("Unknown OpCode")

        # Create instruction object
        instruction_obj = Instruction(OpCode[op_code], [Argument(arg) for arg in args])
        # Validate instruction arguments, if not valid, exit with error
        instruction_obj.validate()
        # Add instruction to program flow
        program.add_instruction(instruction_obj)

    # Print program in xml format
    print(program, file=sys.stdout)
    # Print stats to stderr
    # print(f"STATS: {program.stat_list}", file=sys.stdout)


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


