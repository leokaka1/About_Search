from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.setmaticSetting.syntaxPasing import SematicPasing
from SematicSearch.utils import *
from Search_Demo_1.createCypher import createCypher
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


    print("final_sequence_res=======>>>>", res)
    # return res

# def sematicSetting(analysisModel: SematicAnalysisModel):
#     sematicPasing = SematicPasing(analysisModel)
#     print("Step:3 确定的语序数组为:>>>>>\n")
#     # 1.找到句中有没有确定的entity
#     # 先判断词性对象中是否为空，如果为空就不做处理
#     if analysisModel.nounsHasWords:
#         # coos数组中无词，表示没有并列关系
#         # TODO:判断有点需要改进
#         if analysisModel.isValueSituation():
#             print("Situation: 有属性或者属性值")
#             res = sematicPasing.pasing()
#         else:
#             print("Situation: 无属性或者属性值")
#             res = sematicPasing.pasing()
#             # final_sequence_dict["sequence"] = res




    # elif analysisModel.coosHasWords:
    #     if analysisModel.isValueSituation():
    #         print("Situation: 并列关系 有属性或者属性值")
    #     else:
    #         print("Situation: 并列关系 无属性或者属性值")

    # print("final:最后重组之后的句子序列为:>>>>>>:", final_sequence_dict)
    # print("--------------------------------------------")
    # createCypher(final_sequence_dict, analysisModel)
