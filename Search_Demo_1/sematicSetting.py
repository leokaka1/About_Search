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

    # 名词消歧
    nounsDisambiguration(analysisModel)


    # analysisModel.assembleRelationshipWordAtHEDLast()

    # 先判断词性对象中是否为空，如果为空就不做处理
    if not analysisModel.posModel.isNone:
        final_sequence_word_list = []
        # First Situation - 句子末尾是名词，并且是HED中心词
        pass

    print(final_sequence_word_list)
    print("--------------------------------------------")
    createCypher(final_sequence_word_list)

# 名词消歧
def nounsDisambiguration(analysisModel:SematicAnalysisModel):
    # print("nouns:>>>>>",analysisModel.posModel.nouns)
    nouns = analysisModel.posModel.nouns
    disambiguration_list = open(r"G:\About_Search\Search_Demo_1\resources\disambiguation",encoding="utf-8").readlines()

    for item in disambiguration_list:
        item = item.strip().split("-")
        cur_word = item[0]
        dis_word = item[1]
        if cur_word in nouns:
            index = nouns.index(cur_word)
            nouns.remove(cur_word)
            nouns.insert(index,dis_word)

    print(nouns)


def firstStep(analysisModel:SematicAnalysisModel):
    nouns = analysisModel.posModel.nouns
    entities = []
    entities_type = []
    # 读取实例的列表
    entities_list = open(r"G:\About_Search\Search_Demo_1\resources\entities", encoding="utf-8").readlines()

    # print("entities_list:>>>>",entities_list)
    for item in entities_list:
        item = item.strip().split("-")
        # 用"-"分割
        entity = item[0]
        entity_type = item[1]

        # 将类型和type组装成词典
        entities.append(entity)
        entities_type.append(entity_type)

    for noun in nouns:
        if noun in entities:
            index = entities.index(noun)
            e_type = entities_type[index]
            print(noun)
            print(e_type)



# # First situation
# # 远光软件股份有限公司的投标项目的中标人
# def firstSituation(analysisModel: SematicAnalysisModel):
#     # 先拷贝最终返回数组为名词数组
#     final_sequence_word_list = []
#
#     # 不包含属性
#     if not analysisModel.posModel.attriHasWords:
#         temp_sequence_word_list = analysisModel.posModel.nouns.copy()
#         # 不包含并列关系
#         if not analysisModel.posModel.coosHasWords:
#             # 遍历名词性结构
#             for verb in analysisModel.posModel.verbs:
#                 # 如果动词不为HED中心词或者动词在第一个词组位置出现时添加到最后的词组中
#                 if analysisModel.vertexModel.wordForDeprel(verb) != "HED" and analysisModel.vertexModel.word_list.index(verb) != 0:
#                     verb_target_word = analysisModel.vertexModel.wordForTargetWord(verb)
#                     # 如果谓词的目标词不在名词数组中，则解析其中的摆放位置
#                     if verb_target_word not in temp_sequence_word_list:
#                         for index, noun in enumerate(temp_sequence_word_list):
#                             noun_target_word = analysisModel.vertexModel.wordForTargetWord(noun)
#                             if noun_target_word == verb_target_word:
#                                 flag_index = index + 1
#                         temp_sequence_word_list.insert(flag_index, verb)
#
#                     else:
#                         noun_index = temp_sequence_word_list.index(verb_target_word)
#                         temp_sequence_word_list.insert(noun_index, verb)
#                         # analysisModel.vertexModel.removeVerbWordList(verb)
#
#
#             final_sequence_word_list = temp_sequence_word_list
#         else:
#             # 包含并列关系解法
#             print("包含COOs关系")
#             pass
#
#     else:
#         # 包含属性的解法
#         print("包含属性--稍后判断")
#         pass
#
#     print("分析后的三元组为>>>>", final_sequence_word_list)
#     return final_sequence_word_list
