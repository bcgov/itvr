from clamd import ClamdNetworkSocket
from ..settings import CLAMD_HOST, CLAMD_PORT


def get_clamd_scanner():
    return ClamdNetworkSocket(CLAMD_HOST, CLAMD_PORT)
