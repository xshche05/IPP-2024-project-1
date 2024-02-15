import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from sys_arg_parser import SysArgEnum
from op_code import InstructionSet
from instruction import Instruction
from stat_group import StatGroup


class Program:
    def __init__(self, op_codes: InstructionSet):
        self.__instruction_counter = 0
        self.__instruction_flow = []
        self.__stat_list = {i: 0 for i in op_codes}
        self.__defined_labels = {}
        self.__used_labels = {}
        self.__comment_counter = 0
        self.__op_codes = op_codes

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
        if instruction.op_code in self.__op_codes.label_ops:
            if self.__defined_labels.get(instruction.label) is not None:
                self.__defined_labels[instruction.label].append(self.__instruction_counter)
                # print("maybe error") TODO
            else:
                self.__defined_labels[instruction.label] = [self.__instruction_counter]
        elif instruction.op_code in self.__op_codes.label_jump_ops:
            if self.__used_labels.get(instruction.label) is not None:
                self.__used_labels[instruction.label].append(self.__instruction_counter)
            else:
                self.__used_labels[instruction.label] = [self.__instruction_counter]

    @property
    def instructions_stat(self) -> dict[InstructionSet, int]:
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

    @property
    def loc(self) -> int:
        """
        :return: Returns number of instructions
        """
        return self.__instruction_counter

    @property
    def comments(self) -> int:
        """
        :return: Returns number of comments
        """
        return self.__comment_counter

    @property
    def labels(self) -> int:
        """
        :return: Returns number of labels
        """
        return len(self.__defined_labels)

    @property
    def jumps(self) -> int:
        """
        :return: Returns number of jump (conditional and unconditional), call and return instructions
        """
        jump_ops = self.__op_codes.jump_ops
        print(self.__stat_list)
        return sum([self.__stat_list[op] for op in jump_ops])

    @property
    def fwjumps(self) -> int:
        """
        :return: Returns number of forward jumps
        """
        print(self.__defined_labels)
        fw_jumps = 0
        for label, orders in self.__used_labels.items():
            for order in orders:
                if label not in self.__defined_labels:
                    continue
                if order < self.__defined_labels[label][0]:
                    fw_jumps += 1
        return fw_jumps

    @property
    def backjumps(self) -> int:
        """
        :return: Returns number of backward jumps
        """
        back_jumps = 0
        for label, orders in self.__used_labels.items():
            if label not in self.__defined_labels:
                continue
            for order in orders:
                if order > self.__defined_labels[label][0]:
                    back_jumps += 1
        return back_jumps

    @property
    def badjumps(self) -> int:
        """
        :return: Returns number of bad jumps
        """
        bad_jumps = 0
        for label, orders in self.__used_labels.items():
            if label not in self.__defined_labels:
                bad_jumps += len(orders)
        return bad_jumps

    @property
    def frequent(self) -> int:
        """
        :return: Returns most frequent instruction
        """
        return max([b for a, b in self.__stat_list.items()])

    def load_stats_to(self, group: StatGroup) -> None:
        """
        Write statistics to group
        :param group to write to
        """

        stat_map = {
            SysArgEnum.LOC: self.loc,
            SysArgEnum.COMMENTS: self.comments,
            SysArgEnum.LABELS: self.labels,
            SysArgEnum.JUMPS: self.jumps,
            SysArgEnum.FWJUMPS: self.fwjumps,
            SysArgEnum.BACKJUMPS: self.backjumps,
            SysArgEnum.BADJUMPS: self.badjumps,
            SysArgEnum.FREQUENT: self.frequent
        }

        for stat in group.stats:
            if stat.arg not in stat_map.keys():
                continue
            stat.set_value(stat_map[stat.arg])

    def __str__(self) -> str:
        """
        :return: Returns program in xml format
        """
        return self.xml_str
