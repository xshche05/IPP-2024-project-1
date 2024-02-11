from op_code import OpCode
from instruction import Instruction

class Program:
    def __init__(self):
        self.instruction_counter = 0
        self.instruction_flow = []
        self.stat_list = {i: 0 for i in OpCode}
        self.defined_labels = {}
        self.used_labels = {}

    def add_instruction(self, instruction: Instruction):
        """
        Add instruction to the program flow
        :param instruction: Instruction to add
        :return:
        """
        self.instruction_counter += 1
        instruction.set_order(self.instruction_counter)
        self.instruction_flow.append(instruction)
        self.stat_list[instruction.op_code] += 1
        if instruction.op_code == OpCode.LABEL:
            if self.defined_labels.get(instruction.args[0].value) is not None:
                self.defined_labels[instruction.args[0].value].append(self.instruction_counter)
            else:
                self.defined_labels[instruction.args[0].value] = [self.instruction_counter]
        elif instruction.op_code in [OpCode.CALL, OpCode.JUMP, OpCode.JUMPIFEQ, OpCode.JUMPIFNEQ]:
            if self.used_labels.get(instruction.args[0].value) is not None:
                self.used_labels[instruction.args[0].value].append(self.instruction_counter)
            else:
                self.used_labels[instruction.args[0].value] = [self.instruction_counter]

    def __str__(self):
        """
        :return: Returns program in xml format
        """
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<program language="IPPcode24">{chr(10) if self.instruction_counter != 0 else ''}\
{chr(10).join([str(instruction) for instruction in self.instruction_flow])}
</program>'''