from Search_Demo_1.semanticGraphVertex import SemanticGraphVertex


# 构建句法分析返回结果
# 创建语法结构层级
def createGrammerGraph(segAndPostList):
    sematic = SemanticGraphVertex(segAndPostList)

    # 名词此表
    nounList = []
    # 动词性此表
    verbList = []

    print(sematic.headID)
    print(sematic.head_list)

    # 区分属性句和非属性句
    if not isContainAtrribute(sematic.pos_list):
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
            else:
                pass

        # 第一种情况 - [HED在最后并且其他的都为ATT]
        if sematic.headID == sematic.wordLength - 1:
            print("hed在句尾")

    else:
        print("包含属性，稍后处理")

    print("名词词性的:>>>>>", nounList)
    print("动词词性的:>>>>>>", verbList)

# # 将一些助词删除
# def isATTorSBVwords(deprel):




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
