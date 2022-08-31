from enum import Enum

# for each income tested maximum rebate ($4000, $2000, $1000), there are different rebate levels for certain ZEV types and lease terms
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
