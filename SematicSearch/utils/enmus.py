from enum import Enum


class Situations(Enum):
    noAttribute = 0
    hasAttribute = 1


class SematicStituations(Enum):
    HED = 1
    HED_VOB_SBV = 2
    HED_SBV = 3
    HED_ADV = 4
    HED_ADV_SBV_VOB = 5
    HED_ADV_SBV_VOB_POB = 6