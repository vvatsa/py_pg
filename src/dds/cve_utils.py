import nvdlib
from datetime import datetime, timedelta
from functools import lru_cache

def _cvss_score(cve):
    cvss_score = "N/A"
    if hasattr(cve, 'score') and cve.score:
        if len(cve.score) > 2 and cve.score[2]:  # CVSS v3.x
            cvss_score = cve.score[2]
        elif len(cve.score) > 1 and cve.score[1]:  # CVSS v2
            cvss_score = cve.score[1]

    return cvss_score

def _description(cve):
    if hasattr(cve, 'descriptions') and cve.descriptions:
        return cve.descriptions[0].value
    return "N/A"

@lru_cache(maxsize=None)
def get_recent_cves(days=2):
    # Get the current date and time
    now = datetime.now()
    days_ago = now - timedelta(days=days)

    cves = nvdlib.searchCVE(pubStartDate=days_ago, pubEndDate=now, cvssV3Severity='CRITICAL')
    return [(cve.id, _description(cve), _cvss_score(cve)) for cve in cves]
