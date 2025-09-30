from multicorn import ForeignDataWrapper
from dds.cve_utils import get_recent_cves



class CVEData(ForeignDataWrapper):
    def __init__(self, options, columns):
        super().__init__(options, columns)

    def execute(self, quals, columns):
        cves = get_recent_cves()
        return cves
