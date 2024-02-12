import re
import sys
from my_exceptions import SysArgException, StatGroupException
from stat_group import StatGroup
from sys_arg import SysArg, SysArgEnum


def print_help():
    print("Help message")


stats_arg_regex = r'^--stats=.+$'
print_arg_regex = r'^--print=.+$'


arg_mapper = {
    '--help': SysArgEnum.HELP,
    '--stats': SysArgEnum.STATS,
    '--loc': SysArgEnum.LOC,
    '--comments': SysArgEnum.COMMENTS,
    '--labels': SysArgEnum.LABELS,
    '--jumps': SysArgEnum.JUMPS,
    '--fwjumps': SysArgEnum.FWJUMPS,
    '--backjumps': SysArgEnum.BACKJUMPS,
    '--badjumps': SysArgEnum.BADJUMPS,
    '--frequent': SysArgEnum.FREQUENT,
    '--eol': SysArgEnum.EOL
}


class ArgParser:

    def __init__(self, args: list[str]):
        self.__args = args
        self.__stat_groups = []

    @property
    def args(self) -> list[str]:
        """
        :return: Returns given system arguments
        """
        return self.__args

    @property
    def stat_groups(self) -> list[StatGroup]:
        """
        :return: Returns list of statistics groups to output
        """
        return self.__stat_groups

    def parse_to_groups(self) -> None:
        """
        Parse system arguments to groups
        """
        groups = []
        last_group = None

        for arg in self.__args:
            if arg in ['--help', '-h']:
                if len(self.__args) > 1:
                    raise SysArgException("Help argument must be the only argument")
                print_help()
                sys.exit(0)
            elif re.match(stats_arg_regex, arg):
                file_path = arg.split('=', 1)[1]
                if last_group is not None:
                    groups.append(last_group)
                last_group = StatGroup(file_path)
                if last_group in groups:
                    raise StatGroupException("File path must be unique")
            elif re.match(print_arg_regex, arg):
                if last_group is None:
                    raise SysArgException("Print argument must be in statistics group")
                last_group.add_stat(SysArg(SysArgEnum.PRINT, arg.split('=', 1)[1]))
            elif arg in arg_mapper.keys():
                if last_group is None:
                    raise SysArgException("System argument must be in statistics group")
                if arg_mapper[arg] == SysArgEnum.EOL:
                    last_group.add_stat(SysArg(arg_mapper[arg], ''))
                else:
                    last_group.add_stat(SysArg(arg_mapper[arg]))
            else:
                raise SysArgException("Unknown system argument")

        if last_group is not None:
            groups.append(last_group)
        self.__stat_groups = groups.copy()


if __name__ == '__main__':
    parser = ArgParser(sys.argv[1:])
    parser.parse_to_groups()
    for group in parser.stat_groups:
        print(group)
