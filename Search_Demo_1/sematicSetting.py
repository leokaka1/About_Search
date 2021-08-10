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
    analysisModel = SematicAnalysisModel(vertexModel, posModel)
    # first situation
    final_sequence_word_list = firstSituation(analysisModel)

    # analysisModel.assembleRelationshipWordAtHEDLast()

    # 先判断词性对象中是否为空，如果为空就不做处理
    if not analysisModel.posModel.isNone:
        final_sequence_word_list = []
        # First Situation - 句子末尾是名词，并且是HED中心词
        pass

    print(final_sequence_word_list)
    print("--------------------------------------------")
    createCypher(final_sequence_word_list)


# First situation
# 远光软件股份有限公司的投标项目的中标人
def firstSituation(analysisModel: SematicAnalysisModel):
    # 先拷贝最终返回数组为名词数组
    final_sequence_word_list = analysisModel.posModel.nouns.copy()

    # 不包含属性
    if not analysisModel.posModel.attriHasWords:
        # 不包含并列关系
        if not analysisModel.posModel.coosHasWords:
            # 遍历名词性结构
            for verb in analysisModel.posModel.verbs:
                if analysisModel.vertexModel.wordForDeprel(verb) != "HED":
                    verb_target_word = analysisModel.vertexModel.wordForTargetWord(verb)
                    # 如果谓词的目标词不在名词数组中，则解析其中的摆放位置
                    if verb_target_word not in final_sequence_word_list:
                        for index, noun in enumerate(final_sequence_word_list):
                            noun_target_word = analysisModel.vertexModel.wordForTargetWord(noun)
                            if noun_target_word == verb_target_word:
                                flag_index = index + 1
                        final_sequence_word_list.insert(flag_index, verb)
                    else:
                        noun_index = final_sequence_word_list.index(verb_target_word)
                        final_sequence_word_list.insert(noun_index, verb)

        else:
            # 包含并列关系解法
            pass

    else:
        # 包含属性的解法
        pass

    print("分析后的三元组为>>>>", final_sequence_word_list)
    return final_sequence_word_list
