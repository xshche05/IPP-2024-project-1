import xml.etree.ElementTree as ET

from op_code import OpCode
from instruction import Instruction
import xml.dom.minidom as minidom


class Program:
    def __init__(self):
        self.__instruction_counter = 0
        self.__instruction_flow = []
        self.__stat_list = {i: 0 for i in OpCode}
        self.__defined_labels = {}
        self.__used_labels = {}
        self.__comment_counter = 0

    def add_instruction(self, instruction: Instruction) -> None:
        """
        Add instruction to the program flow
        :param instruction: Instruction to add
        :return:
        """
        self.__instruction_counter += 1
        instruction.set_order(self.__instruction_counter)
        self.__instruction_flow.append(instruction)
        self.__stat_list[instruction.op_code] += 1
        if instruction.op_code == OpCode.LABEL:
            if self.__defined_labels.get(instruction.args[0].value) is not None:
                self.__defined_labels[instruction.args[0].value].append(self.__instruction_counter)
            else:
                self.__defined_labels[instruction.args[0].value] = [self.__instruction_counter]
        elif instruction.op_code in [OpCode.CALL, OpCode.JUMP, OpCode.JUMPIFEQ, OpCode.JUMPIFNEQ]:
            if self.__used_labels.get(instruction.args[0].value) is not None:
                self.__used_labels[instruction.args[0].value].append(self.__instruction_counter)
            else:
                self.__used_labels[instruction.args[0].value] = [self.__instruction_counter]

    @property
    def instructions_stat(self) -> dict[OpCode, int]:
        """
        :return: Returns dictionary with instructions statistics {OpCode: count}
        """
        return self.__stat_list

    @property
    def defined_labels(self) -> dict[str, list[int]]:
        """
        :return: Returns dictionary with defined labels {label: [definition_order]}
        """
        return self.__defined_labels

    @property
    def used_labels(self) -> dict[str, list[int]]:
        """
        :return: Returns dictionary with used labels {label: [order]}
        """
        return self.__used_labels

    def inc_comment_counter(self) -> None:
        """
        Increment comment counter
        :return:
        """
        self.__comment_counter += 1

    @property
    def xml(self) -> ET.Element:
        """
        :return: Returns program in xml format
        """
        program = ET.Element(f'program')
        program.set('language', 'IPPcode24')
        for instruction in self.__instruction_flow:
            program.append(instruction.xml)
        return program

    @property
    def xml_str(self) -> str:
        """
        :return: Returns program in xml format
        """
        xml_string = ET.tostring(self.xml, encoding='UTF-8', method='xml', xml_declaration=True).decode('utf-8')
        xml_string = minidom.parseString(xml_string).toprettyxml(indent=f"{' ' * 4}", encoding='UTF-8').decode('utf-8')
        return xml_string

    def __str__(self) -> str:
        """
        :return: Returns program in xml format
        """
        return self.xml_str
