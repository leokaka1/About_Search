from Search_Demo_1.sematicAnalysisModel import SematicAnalysisModel
from Search_Demo_1.searchNeo4j import searchNeo4j


def createCypher(wordDict, analysisModel: SematicAnalysisModel):
    print("Step:4 把分解出的关系解释成Cypher语句\n")
    print("0.原始句子为:>>>>>>", wordDict["sequence"])

    includeValues = wordDict["includeValues"]
    sequences = wordDict["sequence"]
    isSequence = False

    if not includeValues:
        # Step 1 主语谓语消歧
        disambigurate_list = disambiguration(sequences)

        # Step 2 删除列表中没有的关系词
        new_word_list = deleteNoneRelationWord(disambigurate_list)

        # Step 3 进行关系解析
        cypher_list = relationPasing(new_word_list)
        isSequence = True
    else:
        cypher_list = replaceAttributeValueSentence(sequences, analysisModel)
        # print("含有属性值的另外计算")

    print("--------------------------------------------")
    searchNeo4j(cypher_list,isSequence=isSequence)


# 1.消歧
def disambiguration(sequences):
    # print("nouns:>>>>>",analysisModel.posModel.nouns)
    # 消除歧义
    disambiguration_list = open(r"G:\About_Search\Search_Demo_1\resources\disambiguation", encoding="utf-8").readlines()
    change_sequence = []
    for sequence in sequences:
        for item in disambiguration_list:
            item = item.strip().split("-")
            cur_word = item[0].strip()
            dis_word = item[1].strip()
            # print("cur_word>>>",cur_word)
            # print("dis_word>>>",dis_word)

            if cur_word in sequence:
                index = sequence.index(cur_word)
                sequence.remove(cur_word)
                sequence.insert(index, dis_word)
                # print("sequence>>>",sequence)
        change_sequence.append(sequence)

    print("1.消除歧义之后的句子为:>>>>>>", change_sequence)
    return change_sequence


# 2.删除没有的关系词
def deleteNoneRelationWord(sequences, attribute=False):
    """
    删除没有的关系词
    :param sequences: 原始句子
    :param attribute: 是否含有属性词
    :return: []
    """
    relations_list = open(r"G:\About_Search\Search_Demo_1\resources\relations", encoding="utf-8").readlines()
    types_list = open(r"G:\About_Search\Search_Demo_1\resources\type", encoding="utf-8").readlines()
    lines = open(r"G:\About_Search\Search_Demo_1\resources\attributes", encoding="utf-8").readlines()
    relation_list = []
    type_list = []
    entity_list = []
    if not attribute:
        for sequence in sequences:
            # 关系词
            for type_word in relations_list:
                relation_list.append(type_word.split("-")[1].strip())
                entity_list.append(type_word.split("-")[2].strip())

            # 属性词
            for type_word in types_list:
                type_list.append(type_word.split("-")[0].strip())

            for word in sequence:
                if "/" not in word:
                    if word not in relation_list and word not in entity_list and word not in type_list:
                        sequence.remove(word)
    else:
        new_sequences = []
        main_word = sequences[0]
        for word in sequences[1:]:
            for line in lines:
                entity_word = line.split("-")[0].strip()
                attribute_word = line.split("-")[1].strip()
                instead_word = line.split("-")[2].strip()

                if main_word == entity_word:
                    if word == attribute_word:
                        word = instead_word
            new_sequences.append(word)
            sequences = new_sequences
        sequences.insert(0, main_word)

    print("2.删除词表中关系词不存在的词汇:>>>>>", sequences)
    return sequences


# 进行关系解析
def relationPasing(sequences):
    cypher_final_sequence_list = []
    for sequence in sequences:
        cypher_list = deduceKeyWord(sequence)
        cypher_final_sequence_list.append(cypher_list)

    print('3.转换为cypher_list数组后:>>>>>>>>', cypher_final_sequence_list)
    return cypher_final_sequence_list


# 解析关键词
def deduceKeyWord(wordList):
    flag_index = 0
    prepare_cypher_list = []
    cypher_list = []
    # 判断第一个词
    if wordList[0]:
        firstWord = wordList[0]
    else:
        firstWord = ""

    attribute_word = ""

    # 关系数组
    relation_sequence_list = []

    # 如果第一个词是实例，那么就分解实例
    if "/" in firstWord:
        # 实体词
        instanceName = firstWord.split("/")[0]
        # 实体词的类型
        instanceType = firstWord.split("/")[1]

        # cypher_entity = replaceInstanceCypherStr(instanceName, instanceType)
        prepare_cypher_list.append(firstWord)
        # 第一个词如果可分就赋值
        input_word = instanceType
    else:
        input_word = firstWord

    # FIXME: 如果第一个不是实例，分开判断
    for word in wordList[1:]:
        relation_sequence_list.append(word)

    destination_word_list = []
    while flag_index < len(relation_sequence_list):
        relation_word, destination_word, infer_word, attribute_word = estimateRelationWordOrAttributeWord(input_word,
                                                                                                          relation_sequence_list[
                                                                                                              flag_index])

        # FIXME： 如果 infer_word 有值， 说明是需要系统推断出词的 eg:有中标人的项目
        if infer_word:
            # infer_cypher = replaceCypherStr(infer_word, infer_word=True)
            # cypher_list.insert(0, infer_cypher)
            prepare_cypher_list.insert(0, infer_word)

        # 保证正方向反方向都有词的时候添加
        if destination_word and relation_word:
            # relation_cypher = replaceCypherStr(relation_word)
            # print("destination_word>>>>>>", destination_word, flag_index, len(relation_sequence_list))
            # print("relation_word>>>>>>", relation_word)
            # cypher_list.append(relation_cypher)
            prepare_cypher_list.append(relation_word)
            # 还是用数组添加
            destination_word_list.append(destination_word)

        # FIXME: 目标词，最后再添加
        if len(destination_word_list):
            # destination_cpyher = replaceCypherStr(destination_word_list[-1], destionation=True)
            # cypher_list.append(destination_cpyher)
            prepare_cypher_list.append(destination_word)

        # print("relationword,",relation_word)
        # print("destinationword",destination_word)
        # print("infer_word",infer_word)
        # print("attibute_word",attribute_word)
        # FIXME: 如果最后一个目标词不是序列列表最后一个关系词就继续循环，如果相同就跳出循环
        if destination_word != relation_sequence_list[-1]:
            input_word = destination_word
            flag_index += 1
        else:
            break

    # 中间的词布局
    cypher_list = replaceCypherStr(prepare_cypher_list)

    # TODO：这里是生成结尾cpyer短语的地方，需要改进
    if len(cypher_list):
        # 有属性词的时候
        if attribute_word:
            end_cypher = addEndSearchDirection(cypher_list[-1], attributeWord=attribute_word)
            cypher_list.append(end_cypher)
        # 无属性词的时候
        else:
            end_cypher = addEndSearchDirection(cypher_list[-1])
            cypher_list.append(end_cypher)

    # print("prepare_cypher_list>>>>>>",replaceCypherStr(prepare_cypher_list))

    return cypher_list


# 转换实例单词
def replaceInstanceCypherStr(instanceName, instanceType):
    cypher_str = "(" + "i:{}".format(instanceType) + "{" + "name:" + "'" + instanceName + "'" + "}" + ")"
    return cypher_str


# 转换关系词
def replaceCypherStr(relation_list):
    """
    转换关系词
    :param relation_list: 词
    :return: str
    """
    lines = open(r"G:\About_Search\Search_Demo_1\resources\type", encoding="utf-8").readlines()
    final_cypher_list = []

    relation_flag = 1
    entity_flag = 1

    for relation in relation_list:
        for type_line in lines:
            word = type_line.split("-")[0].strip()
            type = type_line.split("-")[1].strip()
            if relation == word and type == "relation":
                cypher_str = "-[r{}:{}]-".format(relation_flag, word)
                # print(cypher_str)
                relation_flag += 1
                final_cypher_list.append(cypher_str)
            elif relation == word and type == "entity":
                cypher_str = "(e{}:{})".format(entity_flag, word)
                # print(cypher_str)
                entity_flag += 1
                final_cypher_list.append(cypher_str)
        if "/" in relation:
            # 实体词
            instanceName = relation.split("/")[0]
            # 实体词的类型
            instanceType = relation.split("/")[1]
            cypher_str = replaceInstanceCypherStr(instanceName, instanceType)
            # print(cypher_str)
            final_cypher_list.append(cypher_str)

    # print(final_cypher_list)
    return final_cypher_list


# 生成最后一步的方向
def addEndSearchDirection(lastWord, attributeWord=""):

    # FIXME ： 有投标项目的单位 最后单位 应该返回单位而不是项目
    refer_word = lastWord.split(":")[0].replace("(", "")
    # print("refer_word>>>>", refer_word)
    cypher_word = ""
    # 表示应该是查询实体
    if refer_word in lastWord:
        if attributeWord:
            cypher_word = "return {}.{}".format(refer_word, attributeWord)
        else:
            cypher_word = "return {}".format(refer_word)
    elif "i:" in lastWord:
        # 表示应该查询的是查询实例
        if attributeWord:
            cypher_word = "return i.{}".format(attributeWord)
        else:
            cypher_word = "return i"

    return cypher_word


# 分析关系，判断两个词之间的关系
def estimateRelationWordOrAttributeWord(instanceType, word):
    relation_list = open(r"G:\About_Search\Search_Demo_1\resources\relations", encoding="utf-8").readlines()
    # print("进来没有>>>",instanceType)
    # 目的词
    destination_word = ""
    # 关系词
    relation_word = ""
    # 推断词
    infer_word = ""
    # 属性词直接返回
    attribute_word = ""

    instance_list = []
    if instanceType:
        # 先判断在不在关系列表中
        for words in relation_list:
            # 实体词
            instance_type_word = words.split("-")[0].strip()
            # FIXME: 解决最后的词不是实体词，那么就是属性词（后期修改）
            instance_list.append(instance_type_word)
            # 关系词
            relation_word = words.split("-")[1].strip()
            # 目标词
            target_word = words.split("-")[2].strip()
            # 替代关系词
            instead_word = words.split("-")[3].strip()
            # 正方向搜索 知道 左边-中间-> 右边
            if instanceType == instance_type_word:
                # print("匹配到第一个词")
                if word == relation_word:
                    destination_word = target_word
                    return instead_word, destination_word, infer_word, attribute_word
                # 知道左边-右边->中间
                elif word == target_word:
                    destination_word = word
                    return instead_word, destination_word, infer_word, attribute_word
            # 反方向搜索 知道 右边-中->左边
            elif instanceType == target_word:
                if word == relation_word:
                    destination_word = instance_type_word
                    return instead_word, destination_word, infer_word, attribute_word
                # 知道右边-左边->中间
                elif word == instance_type_word:
                    destination_word = word
                    return instead_word, destination_word, infer_word, attribute_word
            # 中间搜索 知道 中间-左边->右边 / 中间-右边->左边
            elif instanceType == relation_word:
                if word == instance_type_word:
                    destination_word = target_word
                    infer_word = word
                    return instead_word, destination_word, infer_word, attribute_word
                else:
                    destination_word = instance_type_word
                    infer_word = word
                    return instead_word, destination_word, infer_word, attribute_word

    # print("instead_word   ",instead_word)
    # print("destination_word    ",destination_word)
    # print("infer_word    ",infer_word)
    # print("word    ",word)
    # FIXME: 如果词不在关系列表中，那么可以判断这个词一定是在属性中
    if destination_word == "" and infer_word == "" and word not in instance_list:
        attribute_word = word

    return relation_word, destination_word, infer_word, attribute_word


# TODO: ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ 关于属性值处理的 ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

# 转换有属性值的
def replaceAttributeValueSentence(sequences, analysisModel: SematicAnalysisModel):
    # print("sequences>>>>", sequences)
    # new_sequences = confirmAttributeWord(sequences)
    cypher_list = []
    if len(sequences):
        new_sequences = deleteNoneRelationWord(sequences, attribute=True)
        cypher_list = confirmAttributeWord(new_sequences, analysisModel)

    return cypher_list


# 确定属性词
def confirmAttributeWord(sequences, analysisModel: SematicAnalysisModel):
    # FIXME： 这里可能未来要改
    lines = open(r"G:\About_Search\Search_Demo_1\resources\attributes", encoding="utf-8").readlines()
    attribute_list = []
    final_cypher_list = []
    for line in lines:
        attribute_list.append(line.split("-")[1].strip())
    # set(attribute_list)

    cypher_str = "(e:{})".format(sequences[0])
    # print(cypher_str)
    final_cypher_list.append(cypher_str)

    cypher_str = ""
    for word in sequences[1:]:
        if word in attribute_list:
            cypher = "where e.{}".format(word)
            cypher_str += cypher
        elif analysisModel.vertexModel.wordisDegree(word):
            degree_word = analysisModel.vertexModel.wordForDegreeSymbol(word)
            cypher_str += degree_word
        elif analysisModel.vertexModel.wordisValue(word):
            cypher_str += "'{}'".format(word)

    final_cypher_list.append(cypher_str)
    # FIXME：结尾词
    end_cypher = "return e"
    final_cypher_list.append(end_cypher)

    print("3.简单的属性拼接之后的句子为:>>>>>>", final_cypher_list)
    return final_cypher_list
