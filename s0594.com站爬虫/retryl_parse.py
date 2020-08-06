import requests
from retrying import retry


@retry(stop_max_attempt_number = 5, wait_fixed=1000)
def _parse_url(url, headers, method):
    if method == "GET":
        response = requests.get(url, headers=headers, timeout=5)
    else:
        response = requests.post(url, headers=headers, timeout=5)
    assert response.status_code == 200
    return response


def parse_url(url, headers, method="GET"):
    try:
        html = _parse_url(url, headers, method)
    except:
        html = None
    return html