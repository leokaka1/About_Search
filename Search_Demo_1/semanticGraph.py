from Search_Demo_1.semanticGraphVertex import SemanticGraphVertex
from Search_Demo_1.createCypher import createCypher

# 构建句法分析返回结果
# 创建语法结构层级
def createGrammerGraph(segAndPostList):
    sematic = SemanticGraphVertex(segAndPostList)

    # 名词词表
    nounList = []
    # 动词性词表
    verbList = []
    # 形容词表
    adjList = []

    # print(sematic.headID)
    # print(sematic.head_list)

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
            elif isAdjWord(sematic.pos):
                adjList.append(word)
            else:
                pass

        # 第一种情况 - [HED在最后并且其他的都为ATT] 没有 SBV之类的主谓关系
        """
        example：远光软件股份有限公司的投标项目的中标人
        """
        if sematic.headID == sematic.wordLength - 1:
            print("hed在句尾")
            # 如果动词性数组中没有词直接输出
            if not len(verbList):
                createCypher(nounList)
            else:
                # 取出动词和与其修饰的中心词进行拼接
                tempList = []
                flagList = []
                finalWordList = []

                # 剔除 noun中的中心词 并且 追加新的 中心词
                for word in verbList:
                    index = sematic.wordForHead(word)
                    for i,nounWord in enumerate(nounList):
                        if sematic.word_list.index(nounWord) == index:
                            word += nounWord
                            flagList.append(i)
                            tempList.append(word)

                for flag in flagList:
                    nounList[flag] = tempList[flagList.index(flag)]

                createCypher(nounList)
        else:
            pass





    else:
        print("包含属性，稍后处理")

    print("名词词性:>>>>>", nounList)
    print("动词词性:>>>>>", verbList)
    print("形容词性:>>>>>", adjList)


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


# 判断一些描述性形容词，如"最多"等
def isAdjWord(pos):
    if pos == "a":
        return True
    else:
        return False
