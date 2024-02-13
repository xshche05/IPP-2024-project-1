from arg_type import ArgType
from program import Program
from my_exceptions import HeaderException, OpCodeException
from op_code import InstructionSet
from instruction import Instruction
from argument import Argument


instruction_set = InstructionSet()
instruction_set.register_header(".IPPcode24")

instruction_set.register_opcode("MOVE", [ArgType.VAR, ArgType.SYMB])
instruction_set.register_opcode("CREATEFRAME", [])
instruction_set.register_opcode("PUSHFRAME", [])
instruction_set.register_opcode("POPFRAME", [])
instruction_set.register_opcode("DEFVAR", [ArgType.VAR])
instruction_set.register_opcode("CALL", [ArgType.LABEL], jump_op=True, label_jump_op=True)
instruction_set.register_opcode("RETURN", [], jump_op=True)
instruction_set.register_opcode("PUSHS", [ArgType.SYMB])
instruction_set.register_opcode("POPS", [ArgType.VAR])
instruction_set.register_opcode("ADD", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("SUB", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("MUL", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("IDIV", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("LT", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("GT", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("EQ", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("AND", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("OR", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("NOT", [ArgType.VAR, ArgType.SYMB])
instruction_set.register_opcode("INT2CHAR", [ArgType.VAR, ArgType.SYMB])
instruction_set.register_opcode("STRI2INT", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("READ", [ArgType.VAR, ArgType.TYPE])
instruction_set.register_opcode("WRITE", [ArgType.SYMB])
instruction_set.register_opcode("CONCAT", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("STRLEN", [ArgType.VAR, ArgType.SYMB])
instruction_set.register_opcode("GETCHAR", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("SETCHAR", [ArgType.VAR, ArgType.SYMB, ArgType.SYMB])
instruction_set.register_opcode("TYPE", [ArgType.VAR, ArgType.SYMB])
instruction_set.register_opcode("LABEL", [ArgType.LABEL], label_set_op=True)
instruction_set.register_opcode("JUMP", [ArgType.LABEL], jump_op=True, label_jump_op=True)
instruction_set.register_opcode("JUMPIFEQ", [ArgType.LABEL, ArgType.SYMB, ArgType.SYMB], jump_op=True, label_jump_op=True)
instruction_set.register_opcode("JUMPIFNEQ", [ArgType.LABEL, ArgType.SYMB, ArgType.SYMB], jump_op=True, label_jump_op=True)
instruction_set.register_opcode("EXIT", [ArgType.SYMB])
instruction_set.register_opcode("DPRINT", [ArgType.SYMB])
instruction_set.register_opcode("BREAK", [])


class Parser:

    def __init__(self, data_lines: list[str]):
        self.__lines = data_lines

    def parse(self) -> Program:
        """
        Parse data from input data
        :return: program object
        """
        look_for_header = True  # Flag for header check
        program = Program(instruction_set)  # Create program object
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
                if instruction != instruction_set.header:
                    raise HeaderException("Header not found")
                look_for_header = False
                continue
            # Split instruction to op_code and args
            op_code, args = (instruction.split()[0].upper(), instruction.split()[1:])
            # Check if OpCode is valid, if not, exit with error
            if op_code not in [op.name for op in instruction_set]:
                raise OpCodeException("Unknown OpCode")
            # Create instruction object
            instruction_obj = Instruction(instruction_set[op_code], [Argument(arg) for arg in args])
            # Validate instruction arguments, if not valid, exit with error
            instruction_obj.validate()
            # Add instruction to program flow
            program.add_instruction(instruction_obj)
        if look_for_header:
            raise HeaderException("Header not found")
        return program
