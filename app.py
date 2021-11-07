import sys

import file_reading
import header_parser

class App():
    def __init__(self):

        # экземпляр класса FileReadin
        self.bin_data = file_reading.FileReading()
        self.data = self.bin_data.data

        # экземпляр класса HeaderParser
        self.header_read = header_parser.HeaderParser(self.data)
