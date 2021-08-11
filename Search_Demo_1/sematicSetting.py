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
    print("Step:3 确定的语序数组为:>>>>>\n")
    # 最终的顺序输出列表
    final_sequence_dict = {"inCludeValues":False,"sequence":[]}
    # 将两个模型分发给分析模型
    analysisModel = SematicAnalysisModel(vertexModel, posModel)

    # 1.找到句中有没有确定的entity
    # 先判断词性对象中是否为空，如果为空就不做处理
    if analysisModel.posModel.nounsHasWords:
        # coos数组中无词，表示没有并列关系
        if analysisModel.posModel.coosHasWords:
            # TODO:判断有点需要改进
            if not analysisModel.posModel.attriHasWords:
                print("Situation: 无属性关系")
                # 先找到是否有实例
                entity_word = findEntityAndIndex(analysisModel.posModel.nouns)
                # print(entity_word)

                # TODO:测试
                new_verbs = verbInsteadNoun(analysisModel)
                res = combinationNewRelation(entity_word, new_verbs, analysisModel)
                final_sequence_dict["sequence"] = res

            else:
                print("Situation: 有属性关系")
                final_sequence_dict["inCludeValues"] = True
                res = attributeRecombination
                final_sequence_dict["sequence"] = res
        else:
            if analysisModel.posModel.attriHasWords:
                print("Situation: 并列关系中有属性关系")
                final_sequence_dict["inCludeValues"] = True
            else:
                print("Situation: 并列关系中无属性关系")
                res = coosCombinationRelation(analysisModel)
                final_sequence_dict["sequence"] = res

    else:
        print("为空")

    print(final_sequence_dict)
    print("--------------------------------------------")
    # createCypher(final_sequence_word_list)


# 找到对应的实例
def findEntityAndIndex(wordList):
    nouns = wordList
    entities = []
    entities_type = []
    final_word_list = []
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
            final_word_list.append(final_word)

    return final_word_list


# 重组谓语和名词的关系
def verbInsteadNoun(analysisModel: SematicAnalysisModel):
    hed_ver_list = ["有", "是", "包含", "为"]
    wordlist = analysisModel.vertexModel.word_list
    verbsList = analysisModel.posModel.verbs
    final_relation_list = []
    for index, verb in enumerate(verbsList):
        verb_deprel = analysisModel.vertexModel.wordForDeprel(verb)
        verb_position = analysisModel.vertexModel.wordForId(verb)
        # 分析谓语是否是下列几个词，然后并且是HED中心词
        if (verb in hed_ver_list) and verb_deprel == "HED":
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

    # 如果最后一个名词是HED，说明话没有HED谓语，那么则把noun添加到最后
    if analysisModel.isLastNounObject():
        final_relation_list.append(analysisModel.posModel.nouns[-1])

    # print("清除了HED关系动词之后的数组>>>>>>", final_relation_list)
    return final_relation_list


# 重组关系
def combinationNewRelation(entities, new_verbs, analysisModel: SematicAnalysisModel):
    final_combination_list = []

    for entity_word in entities:
        new_combination = []
        entity = entity_word.split("/")[0]
        # 1号位置是实例
        new_combination.append(entity_word)

        # 2号位置是修饰实例的Verb
        for verb in new_verbs:
            verb_head = analysisModel.vertexModel.wordForTargetWord(verb)
            if verb_head == entity:
                new_combination.insert(1, verb)
            else:
                new_combination.append(verb)
        # print(new_combination)
        final_combination_list.append(new_combination)

    # print("重组关系之后的确定数组>>>>>", final_combination_list)
    return final_combination_list


# 多层并列处理关系
def coosCombinationRelation(analysisModel: SematicAnalysisModel):
    coos_list = analysisModel.posModel.coos
    coo_words = findEntityAndIndex(coos_list)
    verbs = verbInsteadNoun(analysisModel)
    combinationNewRelation(coo_words, verbs, analysisModel)


# 属性重组
def attributeRecombination():
    pass