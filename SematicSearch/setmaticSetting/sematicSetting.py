from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.setmaticSetting.syntaxPasing import SematicPasing
from SematicSearch.utils import *
from Search_Demo_1.createCypher import createCypher

"""
说明:
posModel - 词性的列表模型
vertexModel - 语义解析模型
analysisModel - 词性语义分析模型

语义解析模式
模式一 ： [HED在最后并且其他的都为ATT] 没有 SBV之类的主谓关系
"""

# 最终的顺序输出列表
final_sequence_dict = {"includeValues": False, "sequence": []}


def sematicSetting(analysisModel: SematicAnalysisModel):
    sematicpasing = SematicPasing(analysisModel, Situations.noAttribute)
    print("Step:3 确定的语序数组为:>>>>>\n")
    # 1.找到句中有没有确定的entity
    # 先判断词性对象中是否为空，如果为空就不做处理
    if analysisModel.nounsHasWords:
        # coos数组中无词，表示没有并列关系
        # TODO:判断有点需要改进
        if analysisModel.isValueSituation():
            print("Situation: 有属性或者属性值")
        else:
            print("Situation: 无属性或者属性值")
            res = sematicpasing.pasing()
            final_sequence_dict["sequence"] = res
    elif analysisModel.coosHasWords:
        if analysisModel.isValueSituation():
            print("Situation: 并列关系 有属性或者属性值")
        else:
            print("Situation: 并列关系 无属性或者属性值")

    print("final:最后重组之后的句子序列为:>>>>>>:", final_sequence_dict)
    print("--------------------------------------------")
    # createCypher(final_sequence_dict, analysisModel)
