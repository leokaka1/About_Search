from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.relationTranslation.relationTranslation import RelationTranslation
from SematicSearch.utils import *
from SematicSearch.createCypher import cypherCreate
from SematicSearch.setmaticSetting.syntaxTemplate import Template

"""
说明:
posModel - 词性的列表模型
vertexModel - 语义解析模型
analysisModel - 词性语义分析模型

语义解析模式
模式一 ： [HED在最后并且其他的都为ATT] 没有 SBV之类的主谓关系
"""

def sematicSetting(analysisModel: SematicAnalysisModel):
    print("Step:3 解析成语法情况:>>>>>>\n")
    template = Template(analysisModel)
    type = analysisModel.sentenceSematicSituations()
    s_type = SematicStituations
    res = {}
    if type == s_type.HED.value:
        print("Situation 1: 主")
        res = template.has_HED_Words()
    elif type == s_type.HED_SBV.value:
        print("Situation 2:- 主 谓")
        res = template.has_SBV_HED_Words()
    elif type == s_type.HED_VOB.value:
        print("Situation 3: - 主 宾")
        res = template.has_HED_VOB_Words()
    elif type == s_type.HED_SBV_VOB.value:
        print("Situation 4: - 主 谓 宾")
        res = template.has_SBV_HED_VOB_Words()
    elif type == s_type.HED_ADV.value:
        print("Situation 5: - 主 状")
        pass
    elif type == s_type.HED_ADV_SBV_VOB.value:
        print("Situation 6: - 主 谓 宾 状")
        res = template.has_ADV_SBV_VOB_HED_Words()
    elif type == s_type.HED_ADV_SBV_VOB_POB.value:
        print("Situation 7: - 主 谓 宾 状 介")
        res = template.has_HED_ADV_SBV_VOB_POB_Words()
    elif type == s_type.COO_HED.value:
        print("Situation 8: - 并列 主")
        res = template.has_COO_HED()
    elif type == s_type.COO_HED_SBV_VOB.value:
        print("Situation 9: - 并列，主谓宾")
        res = template.has_COO_HED_SBV_VOB()
    elif type == s_type.SBV_VOB_HED_IC.value:
        print("Situation 10:- 有IC子句")
        res = template.has_SBV_HED_VOB_IC()
    elif type == s_type.COO_HED_SBV_VOB_ADV.value:
        print("Situation 11 - 并列，主谓宾状中")
        res = template.has_COO_SBV_HED_ADV_VOB()

    print("final_sequence_res=======>>>>", res)
    print("--------------------------------------------")

    RelationTranslation(analysisModel, res)