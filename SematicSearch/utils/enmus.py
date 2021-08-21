from enum import Enum


class Situations(Enum):
    noAttribute = 0
    hasAttribute = 1


class SematicStituations(Enum):
    HED = 1
    HED_SBV = 2
    HED_VOB = 3
    HED_SBV_VOB = 4
    HED_ADV = 5
    HED_ADV_SBV_VOB = 6
    HED_ADV_SBV_VOB_POB = 7
    COO_HED =8
    COO_HED_SBV_VOB = 9