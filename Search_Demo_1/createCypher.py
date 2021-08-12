from Search_Demo_1.sematicAnalysisModel import SematicAnalysisModel

cypher_list = []
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


# 消歧
def disambiguration(sequences):
    # print("nouns:>>>>>",analysisModel.posModel.nouns)
    # 消除歧义
    disambiguration_list = open(r"G:\About_Search\Search_Demo_1\resources\disambiguation", encoding="utf-8").readlines()
    change_sequence = []
    for sequence in sequences:
        for item in disambiguration_list:
            item = item.strip().split("-")
            cur_word = item[0]
            dis_word = item[1]
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


# 删除没有的关系词
def deleteNoneRelationWord(sequences):
    relations_list = open(r"G:\About_Search\Search_Demo_1\resources\relations", encoding="utf-8").readlines()
    relation_list = []
    entity_list = []
    for sequence in sequences:
        for type_word in relations_list:
            relation_list.append(type_word.split("-")[1])
            entity_list.append(type_word.split("-")[2])

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
    for sequence in sequences:
        deduceKeyWord(sequence)


def deduceKeyWord(wordList):
    # 判断第一个词
    firstWord = wordList[0]
    if "/" in firstWord:
        # print("True")
        # 实体词
        instanceName = firstWord.split("/")[0]
        # 实体词的类型
        instanceType = firstWord.split("/")[1]

        cypher_entity = replaceInstanceWord(instanceName,instanceType)
        cypher_list.append(cypher_entity)

    for word in wordList[1:]:
        flag_index = 0
        instanceType = estimateRelationWordOrAttributeWord(instanceType,word)
        # print("instanceType",instanceType)
        # print("lastword",wordList[-1])
        if instanceType == wordList[-1]:
            # print("是查询单词:>>>>",wordList[-1])
            # cypher_str = replaceRelationWord()
            cypher_list.append(replaceRelationWord(instanceType))
            break
        else:
            # print("查询单词创建为最后的instanceType:>>>>",instanceType)
            cypher_list.append(replaceRelationWord(instanceType))

        if instanceType and flag_index == 0:
            cypher_list.append(replaceRelationWord(word))
        # print("instanceType=====>",instanceType)
        flag_index += 1

    print('3.转换为cypher_list数组后:>>>>>>>>',cypher_list)


# 转换实例单词
def replaceInstanceWord(instanceName, instanceType):
    # cypher_str = r"(i:{a}\{name:{b}\})".format(a=instanceType, b=instanceName)
    cypher_str = "(" + "i:{}".format(instanceType) + "{" + "name:" + instanceName + "}" + ")"
    # cypher_str = "i:" + '{}'
    # print(cypher_str)
    return cypher_str


# 转换关系词
def replaceRelationWord(word):
    cypher_str = ""
    type_list = open(r"G:\About_Search\Search_Demo_1\resources\type", encoding="utf-8").readlines()
    for typeline in type_list:
        type = typeline.split("-")[0]
        if type == word:
            cypher_str = "[r:{}]".format(word)

    return cypher_str


def estimateRelationWordOrAttributeWord(instanceType,word):

    relation_list = open(r"G:\About_Search\Search_Demo_1\resources\relations",encoding="utf-8").readlines()
    # print("进来没有>>>",instanceType)
    typeWord = ""
    if instanceType:
        # 先判断在不在关系列表中
        for words in relation_list:
            instance_type_word = words.split("-")[0]
            relation_word = words.split("-")[1]
            target_word = words.split("-")[2]
            instead_word = words.split("-")[3]

            if instanceType == instance_type_word:
                if word == relation_word:
                    # print(target_word)
                    # print(instead_word)
                    typeWord = target_word

    else:

        print("继续查询")

    return typeWord