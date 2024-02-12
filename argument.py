import re
from arg_type import ArgType
from my_exceptions import ArgException
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


var_regex = r'^[LTG]F@[a-zA-Z0-9_\-&%*$!?]+$'
label_regex = r'^[a-zA-Z0-9_\-&%*$!?]+$'
int_regex = r'^int@[+-]?((\d+)|(0[xX][0-9a-fA-F]+)|(0[oO][0-7]+))$'
bool_regex = r'^bool@(true|false)$'
string_regex = r'^string@([^\x00-\x20\x23\x5C]|(\\[0-9]{3}))*$'
nil_regex = r'^nil@nil$'
type_regex = r'^(int|bool|string)$'


xml_replace_dict = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    '\'': '&apos;'
}


type_regex_dict = {
    ArgType.INT: int_regex,
    ArgType.BOOL: bool_regex,
    ArgType.STRING: string_regex,
    ArgType.NIL: nil_regex,
    ArgType.LABEL: label_regex,
    ArgType.TYPE: type_regex,
    ArgType.VAR: var_regex
}


class Argument:
    def __init__(self, value: str):
        self.value = value
        self.type_is_set = False
        self.type = None
        self.order = None
        self.xml_val = None

    @property
    def possible_types(self) -> list[ArgType]:
        possible_arg_types = []

        for arg_type, regex in type_regex_dict.items():
            if re.match(regex, self.value):
                possible_arg_types.append(arg_type)

        if len(possible_arg_types) == 0:
            raise ArgException("Unknown argument type")

        return possible_arg_types

    def set_type(self, arg_type) -> None:
        """
        Set final argument type
        :param arg_type: final argument type
        :return:
        """
        self.type = arg_type
        self.type_is_set = True

    def update_xml_val(self) -> None:
        if self.type == ArgType.VAR:
            self.xml_val = self.value.split('@', 1)[0].upper() + '@' + self.value.split('@')[1]
        elif self.type in [ArgType.INT, ArgType.BOOL, ArgType.STRING, ArgType.NIL]:
            self.xml_val = self.value.split('@', 1)[1]  # Remove TYPE@ from param value
        elif self.type in [ArgType.LABEL, ArgType.TYPE]:
            self.xml_val = self.value  # Label is already in correct format
        else:
            raise Exception("Something went wrong")
        for key, value in xml_replace_dict.items():
            self.xml_val = self.xml_val.replace(key, value)

    def set_number(self, arg_num) -> None:
        """
        Set argument order number
        :param arg_num: argument order number
        """
        self.order = arg_num

    @property
    def xml(self) -> ET.Element:
        """
        :return: Returns argument in xml format
        """
        arg = ET.Element(f'arg')
        arg.set('type', str(self.type))
        arg.text = self.xml_val
        return arg

    @property
    def xml_str(self) -> str:
        """
        :return: Returns argument in xml format
        """
        xml_string = ET.tostring(self.xml, encoding='UTF-8', method='xml', xml_declaration=True).decode('utf-8')
        xml_string = minidom.parseString(xml_string).toprettyxml(indent=f"{' ' * 4}", encoding='UTF-8').decode('utf-8')
        return xml_string

    def __str__(self) -> str:
        """
        :return: Returns argument in xml format
        """
        return f'''{" " * 8}<arg{self.order} type="{self.type}">{self.xml_val}</arg{self.order}>'''