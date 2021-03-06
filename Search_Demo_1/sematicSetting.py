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
    final_sequence_dict = {"includeValues": False, "sequence": []}
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
                # print("entity_word>>>>>",entity_word)

                # TODO:测试
                new_verbs = verbInsteadNoun(analysisModel)
                res = combinationNewRelation(entity_word, new_verbs, analysisModel)
                final_sequence_dict["sequence"] = res
            else:
                print("Situation: 有属性关系")
                final_sequence_dict["includeValues"] = True
                # TODO: 待完成
                res = attributeRecombination(analysisModel)
                final_sequence_dict["sequence"] = res
        else:
            if analysisModel.posModel.attriHasWords:
                print("Situation: 并列关系中有属性关系")
                final_sequence_dict["includeValues"] = True
            else:
                print("Situation: 并列关系中无属性关系")
                res = coosCombinationRelation(analysisModel)
                final_sequence_dict["sequence"] = res
    else:
        print("为空")

    print("重组关系之后的确定数组:", final_sequence_dict)
    print("--------------------------------------------")
    createCypher(final_sequence_dict, analysisModel)


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

    # print("1. 搜索实例词，如果实例词在实例词库中，则构建成:>>>>>>>",final_word_list)
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
                        # print("SBV====",word)清除了HED关系动词之后的数组
                        final_relation_list.append(word)
        # FIXME: 谓词不能放在第一个，- eg:有中标人的项目 则不添加
        elif analysisModel.vertexModel.wordForId(verb) != 0:
            final_relation_list.append(verb)

    # 如果verbs有词，则执行下面的体系，如果没有词，则不执行 eg: 项目的招标金额
    if len(verbsList):
        # 如果最后一个名词是HED，说明话没有HED谓语，那么则把noun添加到最后(如果只有一个HED则不添加，说明就是实例本身)
        if analysisModel.isLastNounObject() and len(analysisModel.posModel.nouns) != 1:
            final_relation_list.append(analysisModel.posModel.nouns[-1])

    # print("清除了HED关系动词之后的数组>>>>>>", final_relation_list)
    return final_relation_list


# 重组关系
def combinationNewRelation(entities, new_verbs, analysisModel: SematicAnalysisModel):
    final_combination_list = []
    new_combination = []

    print("entity>>>>", entities)
    print("new_verbs>>>>>", new_verbs)

    # 如果实例和动词库都有词
    # or 查询一个实例 远光软件股份有限公司 能过 and 不能过
    # and 有投标项目的单位
    if len(entities):
        for entity_word in entities:
            new_combination = []
            entity = entity_word.split("/")[0]
            # 1号位置是实例
            new_combination.append(entity_word)
            if len(new_verbs):
                # 2号位置是修饰实例的Verb
                for verb in new_verbs:
                    verb_head = analysisModel.vertexModel.wordForTargetWord(verb)
                    if verb_head == entity:
                        new_combination.insert(1, verb)
                    else:
                        new_combination.append(verb)
                    # print(new_combination)
                # FIXME: 不知道这里改动有没有影响，先记录
            final_combination_list.append(new_combination)
    # 如果动词库有词
    elif len(new_verbs):
        # 2号位置是修饰实例的Verb
        for verb in new_verbs:
            new_combination.append(verb)
        final_combination_list.append(new_combination)
    else:
        # FIXME: 如果动词和实例都没有则直接使用名词库里的词 eg:有乙方的单位
        final_combination_list.append(analysisModel.posModel.nouns)

    print("重组关系之后的确定数组>>>>>", final_combination_list)
    return final_combination_list


# 多层并列处理关系
def coosCombinationRelation(analysisModel: SematicAnalysisModel):
    coos_list = analysisModel.posModel.coos
    coo_words = findEntityAndIndex(coos_list)
    verbs = verbInsteadNoun(analysisModel)
    final = combinationNewRelation(coo_words, verbs, analysisModel)
    return final


# 属性重组

# 总价为100万的合同有哪些
# 合同总价为100万的有哪些
# 2021年的项目有哪些
# 2020年投标单位有哪些
# 2020年有招标总价超过1000万的项目吗
# 2020年招标总价有超过1000万的项目吗
def attributeRecombination(analysisModel: SematicAnalysisModel):
    # 实体库判断
    type_lines = open(r"G:\About_Search\Search_Demo_1\resources\type", encoding="utf-8").readlines()
    types = []
    final_sequence = []
    verb_deprel_list = []
    # step 1 谓词程度词解析
    verbs = analysisModel.posModel.verbs
    nouns = analysisModel.posModel.nouns
    attris = analysisModel.posModel.attri

    # type添加集合
    for type in type_lines:
        types.append(type.split("-")[0].strip())

    for verb in verbs:
        verb_deprel = analysisModel.vertexModel.wordForDeprel(verb)
        verb_deprel_list.append(verb_deprel)

    for noun in nouns:
        if analysisModel.vertexModel.wordForDeprel(noun) == "SBV":
            final_sequence.append(noun)
        # if len(verbs) > 1 and "HED" in verb_deprel_list:
        noun_target_word = analysisModel.vertexModel.wordForTargetWord(noun)
        for verb in verbs:
            if noun_target_word == verb:
                for type in type_lines:
                    word = type.split("-")[0].strip()
                    type = type.split("-")[1].strip()

                    if noun not in final_sequence:
                        if noun == word and type == "entity":
                            final_sequence.insert(0, noun)
                        elif noun == word:
                            final_sequence.append(noun)

    for verb in verbs:
        if analysisModel.vertexModel.wordForDeprel(verb) != "HED":
            final_sequence.append(verb)

    for attr in attris:
        attr_target_word = analysisModel.vertexModel.wordForTargetWord(attr)
        if attr_target_word not in final_sequence or analysisModel.vertexModel.wordForPos(attr) == "TIME":
            final_sequence.append(attr)
        else:
            index = final_sequence.index(attr_target_word)
            final_sequence.insert(index + 1, attr)

    # 重新再次排序
    for type in type_lines:
        word = type.split("-")[0].strip()
        type = type.split("-")[1].strip()
        if noun == word and type == "entity":
            flag_noun = word
            final_sequence.remove(noun)
            final_sequence.insert(0, flag_noun)



    # # 如果动词的长度大于1并且有HED中心在其中
    # if len(verbs) > 1 and "HED" in verb_deprel_list:
    #     for verb in verbs:
    #         verb_position = analysisModel.vertexModel.wordForId(verb)
    #         verb_deprel = analysisModel.vertexModel.wordForDeprel(verb)
    #         for noun in nouns:
    #             noun_target_word = analysisModel.vertexModel.wordForTargetWord(noun)
    #             if noun_target_word == verb:
    #                 # 遍历type看名词是否在type里是entity，如果是则优先添加
    #                 for type in type_lines:
    #                     word = type.split("-")[0].strip()
    #                     type = type.split("-")[1].strip()
    #                     if noun == word and type == "entity":
    #                         final_sequence.append(noun)
    # final_sequence.append(noun)
    # if verb_deprel != "HED":
    #     final_sequence.append(verb)
    # else:
    #     print("NO")

    # for verb in verbs:
    #     # verb位置

    #
    #     # 找出名词指代的指代词
    #     for noun in nouns:
    #         noun_target_word = analysisModel.vertexModel.wordForTargetWord(noun)
    #         if noun_target_word == verb:
    #             # 判断有没有名词在type中=entity的
    #             for type in type_lines:
    #                 word = type.split("-")[0].strip()
    #                 type = type.split("-")[1].strip()
    #                 # 如果名词在typ中=entity
    #                 if noun == word and type == "entity":
    #                     final_sequence.append(noun)
    #             final_sequence.append(noun)
    #
    #     break

    # for verb in verbs:
    #     # verb中心词
    #     verb_deprel = analysisModel.vertexModel.wordForDeprel(verb)
    #     verb_target_word = analysisModel.vertexModel.wordForTargetWord(verb)
    #     attr_for_sbv_word = ""
    #     flag_noun = ""
    #     flag_attr = ""
    #     # eg : 总价为100万的合同（只适合有名词不为HED的情况）
    #     if verb_deprel != "HED":
    #         # verb位置
    #         # verb_position = analysisModel.vertexModel.wordForId(verb)
    #         # 遍历名词
    #         """
    #         如果名词和属性词都指代同一个动词，说明这个名词和属性词是有关联的，添加到一起
    #         """
    #         # 找出名词指代的指代词
    #         for noun in nouns:
    #             noun_target_word = analysisModel.vertexModel.wordForTargetWord(noun)
    #             if noun_target_word == verb:
    #                 flag_noun = noun
    #
    #         # 找出属性词对应的指代词
    #         for attr in attris:
    #             attr_target_word = analysisModel.vertexModel.wordForTargetWord(attr)
    #             if attr_target_word == verb:
    #                 flag_attr = attr
    #             elif attr_target_word == analysisModel.isSBVword():
    #                 attr_for_sbv_word = attr
    #
    #         # 保证加入的SBV等主语不是"的"等语气词
    #         if analysisModel.vertexModel.wordForPos(verb_target_word) != "u":
    #             final_sequence.append(verb_target_word)
    #         # FIXME:如果标记名词不为空，则添加
    #         if flag_noun != "":
    #             final_sequence.append(flag_noun)
    #         if verb != "":
    #             final_sequence.append(verb)
    #         if flag_attr != "":
    #             final_sequence.append(flag_attr)
    #
    #         # 如果有多属性指向sbv词才添加
    #         if attr_for_sbv_word:
    #             final_sequence.append(attr_for_sbv_word)
    #     else:
    #         if len(analysisModel.posModel.verbs) == 1:
    #             # 如果谓词只有一个中心词 , 找主语和属性词的关系 - 2021年的项目有哪些
    #             for attr in attris:
    #                 attr_target_word = analysisModel.vertexModel.wordForTargetWord(attr)
    #                 final_sequence.append(attr_target_word)
    #                 final_sequence.append(attr)
    #         else: # 动词含有HED并且数量不为1
    #             print("动词数量不等于1哦")
    #             print("final_sequence>>>>", final_sequence)
    #
    # # if not len(verbs):
    # #     # 如果没有有属性值词
    # #     if not len(attris):
    # #         for noun in nouns:
    # #             if analysisModel.vertexModel.wordForDeprel(noun) == "HED":
    # #                 print("haha",noun)
    # #     else:
    # #         print("有属性词")

    print("final_sequence>>>>", final_sequence)
    return final_sequence
