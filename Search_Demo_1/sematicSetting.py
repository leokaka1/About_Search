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



    # 1.找到句中有没有确定的entity
    # 先判断词性对象中是否为空，如果为空就不做处理
    if analysisModel.posModel.nounsHasWords:
        # coos数组中无词，表示没有并列关系
        if not analysisModel.posModel.coosHasWords:
            print("无并列关系")
            if not analysisModel.posModel.attriHasWords:
                print("无属性关系")
                # 先找到是否有实例
                entity_word = findEntityAndIndex(analysisModel.posModel.nouns)
                print(entity_word)

                # TODO:测试
                new_verbs = verbInsteadNoun(analysisModel)
                combinationNewRelation(entity_word,new_verbs,analysisModel)

            else:
                print("有属性关系")
        else:
            print("有并列关系")

            if not analysisModel.posModel.attriHasWords:
                print("并列关系中有属性关系")
            else:
                print("并列关系中无属性关系")
    else:
        print("为空")


    # print(final_sequence_word_list)
    print("--------------------------------------------")
    # createCypher(final_sequence_word_list)



def findEntityAndIndex(wordList):
    nouns = wordList
    entities = []
    entities_type = []
    final_word = ""
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
            final_word = noun + "/" + e_type

    return final_word


def verbInsteadNoun(analysisModel:SematicAnalysisModel):
    wordlist = analysisModel.vertexModel.word_list
    verbsList = analysisModel.posModel.verbs
    final_relation_list = []
    for index,verb in enumerate(verbsList):
        verb_deprel = analysisModel.vertexModel.wordForDeprel(verb)
        verb_position = analysisModel.vertexModel.wordForId(verb)
        # 分析谓语是否是下列几个词，然后并且是HED中心词
        if (verb == "有" or verb == "是" or verb == "包含") and verb_deprel == "HED":
            for word in wordlist:
                word_head = analysisModel.vertexModel.wordForHead(word)
                if word_head == verb_position:
                    # 找到指向中心词的词之后判断一下是否是SBV，因为SBV是谓语的主语，所以找到主语
                    # 替换HED为SBV
                    if analysisModel.vertexModel.wordForDeprel(word) == "SBV":
                        # print("SBV====",word)
                        final_relation_list.append(word)
        else:
            final_relation_list.append(verb)

    print("清除了HED关系动词之后的数组>>>>>>",final_relation_list)
    return final_relation_list


def combinationNewRelation(entity,new_verbs,analysisModel:SematicAnalysisModel):
    new_combination = []

    entity_word = entity.split("/")[0]
    # 1号位置是实例
    new_combination.append(entity)

    # 2号位置是修饰实例的Verb
    for verb in new_verbs:
        verb_head = analysisModel.vertexModel.wordForTargetWord(verb)
        if verb_head == entity_word:
            new_combination.insert(1,verb)
        else:
            new_combination.append(verb)

    print(new_combination)

    # verbsList.insert(flag_index,noun_word)
    # print(verbsList)

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
