from Search_Demo_1.sematicAnalysisModel import SematicAnalysisModel


def createCypher(wordDict, analysisModel: SematicAnalysisModel):
    print("Step:4 把分解出的关系解释成Cypher语句\n")
    print("0.原始句子为:>>>>>>", wordDict["sequence"])

    includeValues = wordDict["includeValues"]
    sequences = wordDict["sequence"]

    # Step 1 主语谓语消歧
    disambigurate_list = disambiguration(sequences)

    # Step 2 删除列表中没有的关系词
    new_word_list = deleteNoneRelationWord(disambigurate_list)

    # Step 3 进行关系解析
    relationPasing(new_word_list)


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
def deleteNoneRelationWord(sequences):
    relations_list = open(r"G:\About_Search\Search_Demo_1\resources\relations", encoding="utf-8").readlines()
    relation_list = []
    entity_list = []
    for sequence in sequences:
        for type_word in relations_list:
            relation_list.append(type_word.split("-")[1].strip())
            entity_list.append(type_word.split("-")[2].strip())

        # for entity_word in entity_list:
        #     instance_list.append(entity_word.split("-")[0])

        for word in sequence:
            if "/" not in word:
                if word not in relation_list and word not in entity_list:
                    sequence.remove(word)

    print("2.删除词表中关系词不存在的词汇:>>>>>", sequences)
    return sequences


# 进行关系解析
def relationPasing(sequences):
    cypher_final_sequence_list = []
    for sequence in sequences:
        cypher_list = deduceKeyWord(sequence)
        cypher_final_sequence_list.append(cypher_list)

    print('3.转换为cypher_list数组后:>>>>>>>>', cypher_final_sequence_list)


# 解析关键词
def deduceKeyWord(wordList):
    flag_index = 0
    cypher_list = []
    # 判断第一个词
    firstWord = wordList[0]

    # 关系数组
    relation_sequence_list = []
    if "/" in firstWord:
        # print("True")
        # 实体词
        instanceName = firstWord.split("/")[0]
        # 实体词的类型
        instanceType = firstWord.split("/")[1]

        cypher_entity = replaceInstanceCypherStr(instanceName, instanceType)
        cypher_list.append(cypher_entity)

    # print(cypher_list)

    for word in wordList[1:]:
        relation_sequence_list.append(word)

    # print(instanceType)
    # print(relation_sequence_list)

    while flag_index < len(relation_sequence_list):
        relation_word, destination_word = estimateRelationWordOrAttributeWord(instanceType,
                                                                              relation_sequence_list[flag_index])

        if destination_word:
            # print("relation_word>>>>>>", relation_word)
            relation_cypher = replaceCypherStr(relation_word)
            # print("destination_word>>>>>>", destination_word,flag_index,len(relation_sequence_list))
            destination_cpyher = replaceCypherStr(destination_word, destionation=True)
            cypher_list.append(relation_cypher)

        instanceType = destination_word
        flag_index += 1

    # FIXME: 终点词，最后再添加(只添加一次)
    cypher_list.append(destination_cpyher)

    return cypher_list


# 转换实例单词
def replaceInstanceCypherStr(instanceName, instanceType):
    # cypher_str = r"(i:{a}\{name:{b}\})".format(a=instanceType, b=instanceName)
    cypher_str = "(" + "i:{}".format(instanceType) + "{" + "name:" + instanceName + "}" + ")"
    # cypher_str = "i:" + '{}'
    # print(cypher_str)
    return cypher_str


# 转换关系词
def replaceCypherStr(word, destionation=False):
    # print("word>>>>>>>>>>>>>>>>>>>>", word)
    cypher_str = ""
    type_list = open(r"G:\About_Search\Search_Demo_1\resources\type", encoding="utf-8").readlines()
    temp_save_list = []
    for typeline in type_list:
        type_word = typeline.split("-")[0].strip()
        temp_save_list.append(type_word)

    if destionation:
        if word in temp_save_list:
            # print("word 在 temp 里")
            cypher_str = "(d:{})".format(word)
    else:
        # print("temp_save_list",temp_save_list)
        if word in temp_save_list:
            # print("word 在 temp 里")
            cypher_str = "[r:{}]".format(word)

    return cypher_str


# 分析关系，判断两个词之间的关系
def estimateRelationWordOrAttributeWord(instanceType, word):
    relation_list = open(r"G:\About_Search\Search_Demo_1\resources\relations", encoding="utf-8").readlines()
    # print("进来没有>>>",instanceType)
    destinationWord = ""
    relation_word = ""
    if instanceType:
        # 先判断在不在关系列表中
        for words in relation_list:
            # 实体词
            instance_type_word = words.split("-")[0].strip()
            # 关系词
            relation_word = words.split("-")[1].strip()
            # 目标词
            target_word = words.split("-")[2].strip()
            # 替代关系词
            instead_word = words.split("-")[3].strip()

            if instanceType == instance_type_word:
                # print("匹配到第一个词")
                if word == relation_word:
                    # 如果有关系，则把关系变成替代词加入cypher_list数组
                    # print(word)
                    # print("instead_word",instead_word)
                    # cypher_list.append(relation_cpyher_str)
                    destinationWord = target_word
                    return instead_word, destinationWord

    else:
        print("继续查询")

    return relation_word, destinationWord
