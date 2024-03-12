from itertools import product
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from arg_type import ArgType
from op_code import OpCode
from argument import Argument
from my_exceptions import OtherSyntaxLexicalException


class Instruction:
    def __init__(self, op_code: OpCode, args: list[Argument], order: int):
        self.__op_code = op_code
        self.__args = args
        self.__order = order

    @property
    def op_code(self) -> OpCode:
        """
        :return: Returns instruction op_code
        """
        return self.__op_code

    @property
    def args(self) -> list[Argument]:
        """
        :return: Returns list of instruction arguments
        """
        return self.__args

    @property
    def label(self) -> str | None:
        """
        :return: Returns label of instruction
        """
        for arg in self.__args:
            if arg.type == ArgType.LABEL:
                return arg.value
        return None

    def validate(self) -> bool:
        """
        Validate instruction arguments, check if the number of arguments is correct and the argument types are correct
        :return: True if the arguments are valid, exception otherwise
        """
        if len(self.__args) != len(self.__op_code.params):
            print(self.__op_code)
            raise OtherSyntaxLexicalException("Invalid number of arguments")

        all_param_combinations = list(product(*[arg.possible_types for arg in self.__args]))
        need = list(self.__op_code.params)
        for got in all_param_combinations:
            if list(got) == list(need):
                for arg, arg_type in zip(self.__args, got):
                    arg.set_type(arg_type)
                    arg.update_xml_val()
                return True
        print(need)
        print(self.__op_code)
        raise OtherSyntaxLexicalException("Opcode operands type mismatch")

    @property
    def xml(self) -> ET.Element:
        """
        :return: Returns instruction in xml format
        """
        instruction = ET.Element(f'instruction')
        instruction.set('order', str(self.__order))
        instruction.set('opcode', str(self.__op_code))
        for arg in self.__args:
            instruction.append(arg.xml)
        return instruction

    @property
    def xml_str(self) -> str:
        """
        :return: Returns instruction in xml format
        """
        xml_string = ET.tostring(self.xml, encoding='UTF-8', method='xml', xml_declaration=True).decode('utf-8')
        xml_string = minidom.parseString(xml_string).toprettyxml(indent=f"{' ' * 4}", encoding='UTF-8').decode('utf-8')
        return xml_string

    def __str__(self) -> str:
        return self.xml_str


class InstructionBuilder:
    """
    Class for instruction builder, used to build instruction using builder pattern
    """
    def __init__(self):
        self.__op_code = None
        self.__args = []
        self.__order = None
        self.__arg_count = 0

    def add_arg(self, arg: Argument) -> None:
        """
        Add argument to instruction
        :param arg: argument to add
        """
        self.__arg_count += 1
        arg.set_order(self.__arg_count)
        self.__args.append(arg)

    def set_order(self, order) -> None:
        """
        Set order of instruction for xml output
        :param order: instruction order number
        :return:
        """
        self.__order = order

    def set_op_code(self, op_code: OpCode) -> None:
        """
        Set instruction op_code
        :param op_code: instruction op_code
        """
        self.__op_code = op_code

    def build(self) -> Instruction:
        """
        Build instruction
        :return:
        """
        return Instruction(self.__op_code, self.__args, self.__order)



