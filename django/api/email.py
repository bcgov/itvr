import os
from enum import Enum


def config():
    return {
        "EMAIL_SERVICE_CLIENT_ID": os.getenv("EMAIL_SERVICE_CLIENT_ID", ""),
        "EMAIL_SERVICE_CLIENT_SECRET": os.getenv("EMAIL_SERVICE_CLIENT_SECRET", ""),
        "CHES_AUTH_URL": os.getenv("CHES_AUTH_URL", ""),
        "CHES_EMAIL_URL": os.getenv("CHES_EMAIL_URL", ""),
        "SENDER_EMAIL": os.getenv("SENDER_EMAIL", "ZEVProgramsDoNotReply@gov.bc.ca"),
        "SENDER_NAME": "CleanBC Go Electric",
        "SEND_EMAIL": os.getenv("SEND_EMAIL", "False") == "True",
    }


class FOUR_THOUSAND_REBATE(Enum):
    ZEV_MAX = 4000
    ZEV_MID = 2688
    ZEV_MIN = 1332
    PHEV_MAX = 2000
    PHEV_MID = 1334
    PHEV_MIN = 666


class TWO_THOUSAND_REBATE(Enum):
    ZEV_MAX = 2000
    ZEV_MID = 1334
    ZEV_MIN = 666
    PHEV_MAX = 1000
    PHEV_MID = 667
    PHEV_MIN = 333


class ONE_THOUSAND_REBATE(Enum):
    ZEV_MAX = 1000
    ZEV_MID = 667
    ZEV_MIN = 333
    PHEV_MAX = 500
    PHEV_MID = 334
    PHEV_MIN = 167
