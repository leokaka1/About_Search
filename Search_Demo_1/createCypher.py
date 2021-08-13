from Search_Demo_1.sematicAnalysisModel import SematicAnalysisModel


def createCypher(wordDict, analysisModel: SematicAnalysisModel):
    print("Step:4 把分解出的关系解释成Cypher语句\n")
    print("0.原始句子为:>>>>>>", wordDict["sequence"])

    includeValues = wordDict["includeValues"]
    sequences = wordDict["sequence"]

    if not includeValues:
        # Step 1 主语谓语消歧
        disambigurate_list = disambiguration(sequences)

        # Step 2 删除列表中没有的关系词
        new_word_list = deleteNoneRelationWord(disambigurate_list)

        # Step 3 进行关系解析
        cypher_list = relationPasing(new_word_list)
    else:
        print("含有属性值的另外计算")


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
    types_list = open(r"G:\About_Search\Search_Demo_1\resources\type", encoding="utf-8").readlines()
    relation_list = []
    type_list = []
    entity_list = []
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

    # destination_word = ""
    # input_word = ""
    attribute_word = ""

    # 关系数组
    relation_sequence_list = []

    # 如果第一个词是实例，那么就分解实例
    if "/" in firstWord:
        # print("True")
        # 实体词
        instanceName = firstWord.split("/")[0]
        # 实体词的类型
        instanceType = firstWord.split("/")[1]

        cypher_entity = replaceInstanceCypherStr(instanceName, instanceType)
        cypher_list.append(cypher_entity)
        # 第一个词如果可分就赋值
        input_word = instanceType
    else:
        input_word = firstWord

    # FIXME: 如果第一个不是实例，分开判断
    # print(cypher_list)

    for word in wordList[1:]:
        relation_sequence_list.append(word)

    # print(instanceType)
    # print(relation_sequence_list)
    destination_word_list = []
    while flag_index < len(relation_sequence_list):
        relation_word, destination_word, infer_word, attribute_word = estimateRelationWordOrAttributeWord(input_word,
                                                                                                          relation_sequence_list[
                                                                                                              flag_index])

        # FIXME： 如果 infer_word 有值， 说明是需要系统推断出词的 eg:有中标人的项目
        if infer_word:
            # print("infer_word有值", infer_word)
            # 添加到cypher_list数组的第一个
            infer_cypher = replaceCypherStr(infer_word, infer_word=True)
            cypher_list.insert(0, infer_cypher)

        # 保证正方向反方向都有词的时候添加
        if destination_word and relation_word:
            relation_cypher = replaceCypherStr(relation_word)
            # print("destination_word>>>>>>", destination_word, flag_index, len(relation_sequence_list))
            # print("relation_word>>>>>>", relation_word)
            cypher_list.append(relation_cypher)
            # 还是用数组添加
            destination_word_list.append(destination_word)

        input_word = destination_word
        flag_index += 1

    # FIXME: 终点词，最后再添加(只添加一次)
    if len(destination_word_list):
        destination_cpyher = replaceCypherStr(destination_word_list[-1], destionation=True)
        cypher_list.append(destination_cpyher)

    # print("relationword,",relation_word)
    # print("destinationword",destination_word)
    # print("infer_word",infer_word)

    if len(cypher_list):
        if attribute_word:
            # TODO：这里是生成结尾cpyer短语的地方，需要改进
            end_cypher = addEndSearchDirection(cypher_list[-1], attributeWord=attribute_word)
            cypher_list.append(end_cypher)
        else:
            # TODO：这里是生成结尾cpyer短语的地方，需要改进
            end_cypher = addEndSearchDirection(cypher_list[-1])
            cypher_list.append(end_cypher)

    return cypher_list


# 转换实例单词
def replaceInstanceCypherStr(instanceName, instanceType):
    # cypher_str = r"(i:{a}\{name:{b}\})".format(a=instanceType, b=instanceName)
    cypher_str = "(" + "i:{}".format(instanceType) + "{" + "name:" + instanceName + "}" + ")"
    # cypher_str = "i:" + '{}'
    # print(cypher_str)
    return cypher_str


# 转换关系词
def replaceCypherStr(word, destionation=False, infer_word=False):
    """
    转换关系词
    :param word: 词
    :param destionation:  目标词
    :param infer_word: 推断词
    :return: str
    """
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

    if infer_word:
        if word in temp_save_list:
            # print("word 在 temp 里")
            cypher_str = "(n:{})".format(word)

    return cypher_str


# 生成最后一步的方向
def addEndSearchDirection(lastword, attributeWord="", degreeWord="", valueWord=""):
    cypher_word = ""
    # 表示应该是查询实体
    if "d:" in lastword:
        if attributeWord:
            if degreeWord and valueWord:
                cypher_word = "where d.{}{}{} return d".format(attributeWord, degreeWord, valueWord)
            else:
                cypher_word = "where d.{} return d".format(attributeWord)
        else:
            cypher_word = "return d"
    elif "i:" in lastword:
        # 表示应该查询的是查询实例
        if attributeWord:
            if degreeWord and valueWord:
                cypher_word = "where i.{}{}{} return i".format(attributeWord, degreeWord, valueWord)
            else:
                cypher_word = "where i.{} return i".format(attributeWord)
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

    # FIXME: 如果词不在关系列表中，那么可以判断这个词一定是在属性中
    attribute_word = word

    return relation_word, destination_word, infer_word, attribute_word
