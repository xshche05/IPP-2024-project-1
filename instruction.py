from itertools import product
from op_code import OpCode
from argument import Argument
from my_exceptions import ArgException


class Instruction:
    def __init__(self, op_code: OpCode, args: list[Argument]):
        self.op_code = op_code
        self.args = args
        self.order = None

    def set_order(self, order):
        """
        Set order of instruction for xml output
        :param order: instruction order number
        :return:
        """
        self.order = order

    def validate(self):
        """
        Validate instruction arguments, check if the number of arguments is correct and if the argument types are correct
        :return: True if the arguments are valid, error message and exit if not
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

    def __str__(self):
        return f'''{" " * 4}<instruction order="{self.order}" opcode="{self.op_code}">{chr(10) if len(self.args) > 0 else ''}\
{chr(10).join([str(arg) for arg in self.args])}
{" " * 4}</instruction>'''