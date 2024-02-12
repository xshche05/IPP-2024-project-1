from itertools import product
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from op_code import OpCode
from argument import Argument
from my_exceptions import ArgException


class Instruction:
    def __init__(self, op_code: OpCode, args: list[Argument]):
        self.op_code = op_code
        self.args = args
        self.order = None

    def set_order(self, order) -> None:
        """
        Set order of instruction for xml output
        :param order: instruction order number
        :return:
        """
        self.order = order

    def validate(self) -> bool:
        """
        Validate instruction arguments, check if the number of arguments is correct and if the argument types are correct
        :return: True if the arguments are valid, exception otherwise
        """
        if len(self.args) != len(self.op_code.params):
            raise ArgException("Invalid number of arguments")

        all_param_combinations = list(product(*[arg.possible_types for arg in self.args]))
        need = list(self.op_code.params)
        for got in all_param_combinations:
            if list(got) == list(need):
                cnt = 0
                for arg, arg_type in zip(self.args, got):
                    cnt += 1
                    arg.set_type(arg_type)
                    arg.set_number(cnt)
                    arg.update_xml_val()
                return True
        raise ArgException("Opcode operands type mismatch")

    @property
    def xml(self) -> ET.Element:
        """
        :return: Returns instruction in xml format
        """
        instruction = ET.Element(f'instruction')
        instruction.set('order', str(self.order))
        instruction.set('opcode', str(self.op_code))
        for arg in self.args:
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
