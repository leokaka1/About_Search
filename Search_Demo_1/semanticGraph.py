from Search_Demo_1.semanticGraphVertexModel import SemanticGraphVertex
from Search_Demo_1.sematicSetting import posSetting
from Search_Demo_1.sematicPosModel import SematicPosModel


# 构建句法分析返回结果
# 创建语法结构层级
def createGrammerGraph(segAndPostList):
    # 名词词表
    nounList = []
    # 并列关系的名词
    coo_list = []
    # 动词性词表
    verbList = []
    # 形容词表
    adjList = []

    pos_Model = SematicPosModel()

    # print(sematic.headID)
    # print(sematic.head_list)

    # 区分属性句和非属性句
    if len(segAndPostList):
        sematic = SemanticGraphVertex(segAndPostList)
        # 遍历句法分析表
        for word in sematic.word_list:
            sematic.sematicResponse(word)
            # print(sematic.deprel)
            # print(sematic.head)
            # print(sematic.pos)

            # 判断是名词性节点还是动词性节点
            if isNounWord(sematic.pos):
                # 如果不是虚词成分就加入数组
                if not sematic.wordForDeprel(word) == "MT":
                    nounList.append(word)
            elif isVerbWord(sematic.pos):
                verbList.append(word)
            elif isAdjWord(sematic.pos, word):
                adjList.append(word)
            else:
                pass

        # 处理并列关系 - 句中含有COO关系的找到其对应的targetword并做一个映射
        for nounWord in nounList:
            if sematic.wordForDeprel(nounWord) == "COO":
                target_word = sematic.wordForTargetWord(nounWord)
                if target_word in nounList:
                    coo_list.append(target_word)
                    coo_list.append(nounWord)

        pos_Model.isNone = False
        # print("temp_coo_list>>>>",coo_list)
        # print("nounList>>>>>",nounList)

        # 第一种情况 - [HED在最后并且其他的都为ATT] 没有 SBV之类的主谓关系

        """
        example：远光软件股份有限公司的投标项目的中标人
        """
        # if sematic.headID == sematic.wordLength -1:
        #     # 如果动词性数组中没有词直接输出
        #     # if not len(verbList) and not len(adjList):
        #     #     pass
        #     # 没有形容词修饰的时候 因为避免有最多等形容词
        #     if not len(adjList):
        #         # 取出动词和与其修饰的中心词进行拼接
        #         # 剔除 noun中的中心词 并且 追加新的 中心词
        #         for word in verbList:
        #             index = sematic.wordForHead(word)
        #             for i, nounWord in enumerate(nounList):
        #                 if sematic.word_list.index(nounWord) == index:
        #                     word += nounWord
        #                     flagList.append(i)
        #                     tempList.append(word)
        #         # print(tempList)
        #         # print(flagList)
        #         nounList = deleteAndAddInList(flagList,tempList,nounList)
        #     else:
        #         # 处理形容词应该就处理哪个名词指向形容词
        #         print("有形容词修饰")
        #         if not len(verbList):
        #             for word in nounList:
        #                 index = sematic.wordForHead(word)
        #                 for i, adjWord in enumerate(adjList):
        #                     if sematic.wordForId(adjWord) == index:
        #                         word = word + "/" + adjWord
        #                         flagList.append(i)
        #                         tempList.append(word)
        #             print(tempList)
        #             print(flagList)
        #         else:
        #             print("动词不为空，且有可能指向形容词")
        #         nounList = deleteAndAddInList(flagList,tempList,nounList)
        # else:
        #     print("HED不在最后")

        pos_Model.nouns = nounList
        pos_Model.coos = coo_list
        pos_Model.verbs = verbList
        pos_Model.adjs = adjList

        print("Step 2 返回词性:>>>>>>\n")
        print("名词词性:>>>>>", nounList)
        print("并列名词:>>>>>", coo_list)
        print("动词词性:>>>>>", verbList)
        print("形容词性:>>>>>", adjList)
        print("--------------------------------------------")

    else:
        print("数组为空，不予处理")

    posSetting(pos_Model)


# 判断句式中是否含有属性问题
def isContainAtrribute(posList):
    for posTag in posList:
        if posTag == "TIME" or posTag == "m" or posTag == "PER" or posTag == "LOC":
            return True
        else:
            return False


# 判断是否是名词词性的词
def isNounWord(pos):
    nounList = ["n", "nr", "nz", "nw", "ORG"]

    if pos in nounList:
        return True
    else:
        return False


# 判断是否是动词词性的词
def isVerbWord(pos):
    verbList = ["v", "vd", "vn"]

    if pos in verbList:
        return True
    else:
        return False


# 判断一些程度描述性形容词，如"最多"等
def isAdjWord(pos, word):
    if pos == "a" and isDegreeWord(word):
        return True
    else:
        return False


# 判断是都是Coo的并列关系
def isCoo(deprel, word):
    if deprel == "COO" and isDegreeWord(word):
        return True
    else:
        return False


# 判断程度形容词
def isDegreeWord(word):
    # TODO:可以最后写成文件扩展
    degreeList = ["最多", "最少", "最大", "最小"]

    if word in degreeList:
        return True
    else:
        return False


# 删除元素并且替换数组
def deleteAndAddInList(flagList,wordList,targetList):
    for index, flag in enumerate(flagList):
        if index > 0 and flagList[index] == flagList[index - 1]:
            targetList.append(wordList[index])
        else:
            targetList[flag] = wordList[flagList.index(flag)]

    return targetList