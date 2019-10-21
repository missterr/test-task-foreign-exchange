import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def requests_retry_session(retries=5, backoff_factor=0.5, session=None, headers=None):
    session = session or requests.Session()

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(500, 502, 504),
    )

    adapter = HTTPAdapter(max_retries=retry)
    adapter.add_headers(headers or dict())

    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
