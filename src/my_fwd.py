from multicorn import ForeignDataWrapper
from tkinter.constants import YES

class DummyFDW(ForeignDataWrapper):

    def __init__(self, options, columns):
        super().__init__(options, columns)
        self.columns = columns

    def execute(self, quals, columns):
        for index in range(20):
            line = {}
            for col_name in self.columns:
              line[col_name] = f"{col_name}_{index}"
            yield line
