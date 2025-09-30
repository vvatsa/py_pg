import numpy as np

from multicorn import ForeignDataWrapper

class NpNormal(ForeignDataWrapper):
    def __init__(self, options, columns):
        super().__init__(options, columns)
        self.mean = int(options.get('mean', 0))
        self.std = int(options.get('std', 1))
        self.size = int(options.get('size', 100))

    def _quals_to_dict(self, quals):
        return {qual.field_name: int(qual.value) for qual in quals if qual.operator == '='}

    def execute(self, quals, columns):
        _quals_dict = self._quals_to_dict(quals)
        mean = _quals_dict.get('mean', self.mean)
        std = _quals_dict.get('std', self.std)
        size = _quals_dict.get('size', self.size)
        for idx, smpl in enumerate(np.random.normal(loc=mean, scale=std, size=size)):
            yield idx, smpl, mean, std, size
