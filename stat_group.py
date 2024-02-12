from sys_arg import SysArg


class StatGroup:

    def __init__(self, file_path: str):
        self.__stats = []
        self.__file_path = file_path

    @property
    def file_path(self) -> str:
        """
        :return: Returns file path to write group to
        :return: name of the file (or path)
        """
        return self.__file_path

    def add_stat(self, stat: SysArg) -> None:
        """
        Add statistic to group
        :param stat: statistic to add
        """
        self.__stats.append(stat)

    @property
    def stats(self) -> list[SysArg]:
        """
        :return: Returns list of statistics in group
        """
        return self.__stats

    def write_to_file(self) -> None:
        """
        Write group to file
        """
        with open(self.__file_path, 'w') as file:
            for stat in self.stats:
                file.write(str(stat.value) + '\n')

    def __eq__(self, other) -> bool:
        return self.file_path == other.file_path

    def __str__(self) -> str:
        return f"File: {self.file_path}; stats: {', '.join([str(i) for i in self.__stats])}"
