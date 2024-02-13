class Reader:
    def __init__(self, stream):
        self.__input_stream = stream
        self.__read_data = None

    def read_stream(self) -> None:
        """
        Reads full input stream
        """
        self.__read_data = self.__input_stream.read()

    def get_lines(self) -> list[str]:
        """
        Returns read input stream as list of lines
        :return: list of lines
        """
        return self.__read_data.splitlines()
