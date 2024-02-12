from program import Program
from my_exceptions import HeaderException, OpCodeException
from op_code import OpCode
from instruction import Instruction
from argument import Argument


class Parser:

    def __init__(self, data_lines: list[str]):
        self.__lines = data_lines

    def parse(self) -> Program:
        look_for_header = True  # Flag for header check
        program = Program()  # Create program object
        for line in self.__lines:
            instruction, *comment = line.split('#', 1)  # Split instruction and comment
            if len(comment) > 0:
                program.inc_comment_counter()
            instruction = instruction.lstrip().rstrip()  # Remove leading and trailing whitespaces
            # Skip empty lines
            if instruction == '':
                continue
            # Check for header, if first non-empty (non_comment) line is not header, exit with error
            if look_for_header:
                if instruction != '.IPPcode24':
                    raise HeaderException("Header not found")
                look_for_header = False
                continue
            # Split instruction to op_code and args
            op_code, args = (instruction.split()[0].upper(), instruction.split()[1:])
            # Check if OpCode is valid, if not, exit with error
            if op_code not in [op.name for op in OpCode]:
                raise OpCodeException("Unknown OpCode")
            # Create instruction object
            instruction_obj = Instruction(OpCode[op_code], [Argument(arg) for arg in args])
            # Validate instruction arguments, if not valid, exit with error
            instruction_obj.validate()
            # Add instruction to program flow
            program.add_instruction(instruction_obj)
        return program
