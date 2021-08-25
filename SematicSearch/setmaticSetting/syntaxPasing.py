from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.setmaticSetting.syntaxTemplate import Template
from SematicSearch.utils import *

lexicon = Lexicon()


class SematicPasing:
    def __init__(self, analysisModel: SematicAnalysisModel):
        self.analysisModel = analysisModel
        self.s_type = SematicStituations

    def pasing(self):
        template = Template(self.analysisModel)
        type = self.analysisModel.sentenceSematicSituations()
        res = {}
        if type == self.s_type.HED.value:
            print("Situation 1: 主")
            res = template.has_HED_Words()
        elif type == self.s_type.HED_SBV.value:
            print("Situation 2:- 主 谓")
            res = template.has_SBV_HED_Words()
        elif type == self.s_type.HED_VOB.value:
            print("Situation 3: - 主 宾")
            res = template.has_HED_VOB_Words()
        elif type == self.s_type.HED_SBV_VOB.value:
            print("Situation 4: - 主 谓 宾")
            res = template.has_SBV_HED_VOB_Words()
        elif type == self.s_type.HED_ADV.value:
            print("Situation 5: - 主 状")
        elif type == self.s_type.HED_ADV_SBV_VOB.value:
            print("Situation 6: - 主 谓 宾 状")
        elif type == self.s_type.HED_ADV_SBV_VOB_POB.value:
            print("Situation 7: - 主 谓 宾 状 介")

        print("final_sequence_res=======>>>>", res)
