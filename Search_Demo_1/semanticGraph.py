from Search_Demo_1.semanticVertexModel import SemanticGraphVertexModel
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
    # 存储属性值
    attriLst = []

    # print(sematic.headID)
    # print(sematic.head_list)

    # 区分属性句和非属性句
    if len(segAndPostList):
        sematic_Model = SemanticGraphVertexModel(segAndPostList)
        # 遍历句法分析表
        for word in sematic_Model.word_list:
            sematic_Model.sematicResponse(word)
            # print(sematic.deprel)
            # print(sematic.head)
            # print(sematic.pos)

            # 判断是名词性节点还是动词性节点
            if isNounWord(sematic_Model.pos):
                # 如果不是虚词成分就加入数组
                if not sematic_Model.wordForDeprel(word) == "MT":
                    nounList.append(word)
            elif isVerbWord(sematic_Model.pos):
                verbList.append(word)
            elif isAdjWord(sematic_Model.pos):
                adjList.append(word)
            else:
                pass

        # 处理并列关系 - 句中含有COO关系的找到其对应的target word并做一个映射
        for nounWord in nounList:
            if sematic_Model.wordForDeprel(nounWord) == "COO":
                target_word = sematic_Model.wordForTargetWord(nounWord)
                if target_word in nounList:
                    coo_list.append(target_word)
                    coo_list.append(nounWord)

        # 删除名词里面相同的词，避免后期再次删除
        for cooWord in coo_list:
            if cooWord in nounList:
                nounList.remove(cooWord)

        # 处理属性值操作
        for index, posWord in enumerate(sematic_Model.pos_list):
            if posWord == "TIME" or posWord == "m" or posWord == "PER":
                attriLst.append(sematic_Model.word_list[index])

        coo_list = set(coo_list) if len(coo_list)>0 else coo_list
        print("Step:2 返回词性:>>>>>>\n")
        print("名词词性:>>>>>", nounList)
        print("并列名词:>>>>>", coo_list)
        print("动词词性:>>>>>", verbList)
        print("形容词性:>>>>>", adjList)
        print("属性值词:>>>>>", attriLst)
        print("--------------------------------------------")

        pos_Model = SematicPosModel(nounList, coo_list, verbList, adjList, attriLst)
        posSetting(pos_Model, sematic_Model)

    else:
        print("数组为空，不予处理")


# 判断是否是名词词性的词
def isNounWord(pos):
    nounList = ["n", "nr", "nz", "nw", "ORG","LOC"]
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
def isAdjWord(pos):
    if pos == "a":
        return True
    else:
        return False



