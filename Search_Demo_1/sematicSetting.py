from Search_Demo_1.sematicPosModel import SematicPosModel
from Search_Demo_1.semanticVertexModel import SemanticGraphVertexModel
from Search_Demo_1.createCypher import createCypher
from Search_Demo_1.sematicAnalysisModel import SematicAnalysisModel

"""
说明:
posModel - 词性的列表模型
vertexModel - 语义解析模型
analysisModel - 词性语义分析模型

语义解析模式
模式一 ： [HED在最后并且其他的都为ATT] 没有 SBV之类的主谓关系
"""


def posSetting(posModel: SematicPosModel, vertexModel: SemanticGraphVertexModel):
    print("Step 3 确定的语序数组为:>>>>>\n")
    # 最终的顺序输出列表
    final_sequence_word_list = []
    # 将两个模型分发给分析模型
    analysisModel = SematicAnalysisModel(vertexModel,posModel)

    # 先判断词性对象中是否为空，如果为空就不做处理
    if not analysisModel.posModel.isNone:

        final_sequence_word_list = generateWordSequence(analysisModel)
    else:
        pass


    print(final_sequence_word_list)
    print("--------------------------------------------")
    createCypher(final_sequence_word_list)


# First situation
# 远光软件股份有限公司的投标项目的中标人
def generateWordSequence(analysisModel:SematicAnalysisModel):
    final_sequence_word_list = []



    # FIXME：这里暂时处理了组装的情况
    analysisModel.assembleRelationshipWord()









    # 假设动词和形容词表没有词
    # if not analysisModel.posModel.adjsHasWords:
    #     if not analysisModel.posModel.coosHasWords:
    #         # FIXME: First Situation
    #         # 如果最后一个名词是HED或者是SBV的话说明最后一个名词是中心词或者是中心词谓动词的主语(subject)
    #         if analysisModel.isLastNounAndVerbObject():
    #             if not analysisModel.posModel.verbsHasWords:
    #                 # 如果没有动词的情况下直接赋值
    #                 final_sequence_word_list = analysisModel.posModel.nouns
    #             else:
    #                 # 如果有动词的情况下需要考虑拼装动词和名词
    #                 pass
    #         elif not analysisModel.analysisVerbsLastWord() == "HED":
    #             print("有动词但是不是HED的情况")

    return final_sequence_word_list
