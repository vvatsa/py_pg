from multicorn import ForeignDataWrapper

class DummyFDW(ForeignDataWrapper):

    def __init__(self, options, columns):
        super().__init__(options, columns)
        self.columns = columns
        self.options = options
        self.num_rows = int(self.options.get('num_rows', 20))

    def execute(self, quals, columns):
        for index in range(self.num_rows):
            line = {}
            for col_name in self.columns:
              line[col_name] = f"{col_name}_{index}"
            yield line
