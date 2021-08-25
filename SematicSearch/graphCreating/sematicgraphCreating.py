from SematicSearch.model.sematicModel import SemanticModel
from SematicSearch.setmaticSetting.sematicSetting import sematicSetting
from SematicSearch.utils.lexicon import Lexicon
from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils.distinguishwords import *

"""
# 构建词性分组
"""
lexicon = Lexicon()


def seperatingTypeOfWords(segAndPostList):
    # 名词词表
    nounList = []
    # 并列关系的名词
    cooList = []
    # 动词性词表
    verbList = []
    # 形容词表
    adjList = []
    # 存储属性值
    valueList = []
    # 问属性的词
    attributeList = []

    # 区分属性句和非属性句
    if len(segAndPostList):
        sematic_Model = SemanticModel(segAndPostList)
        # 遍历句法分析表
        for index, word in enumerate(sematic_Model.word_list):
            sematic_Model.sematicResponse(word)
            # print(sematic_Model.deprel)
            # print(sematic_Model.head)
            # print(word)
            # print(sematic_Model.pos)

            # 判断是名词性节点还是动词性节点
            if isNounWord(sematic_Model.pos):
                # 如果不是虚词成分就加入数组
                if not sematic_Model.wordForDeprel(word) == "MT":
                    nounList.append(combineWords(word, index))
            elif isVerbWord(sematic_Model.pos):
                verbList.append(combineWords(word, index))
            elif isAdjWord(sematic_Model.pos):
                adjList.append(combineWords(word, index))

        # # 处理并列关系 - 句中含有COO关系的找到其对应的target word并做一个映射
        temp_coos = []
        temp_attribute = []
        for nounWord in nounList:
            orign_word = nounWord.split("-")[0]
            if findInstanceWord(orign_word):
                temp_coos.append(nounWord)
            if lexicon.findWordAndType(orign_word,"attribute"):
                temp_attribute.append(nounWord)

        # 删除名词里面相同的词，避免后期再次删除
        # FIXME: 如果并列名词的长度大于等于2时，进行操作
        if len(temp_coos) >= 2:
            cooList += temp_coos
            for cooWord in cooList:
                if cooWord in nounList:
                    nounList.remove(cooWord)

        # 删除属性里面相同的词，避免后期再次删除
        if temp_attribute:
            attributeList += temp_attribute
            for attribute in temp_attribute:
                if attribute in nounList:
                    nounList.remove(attribute)

        # 处理属性值操作
        for index, posWord in enumerate(sematic_Model.pos_list):
            if valueWord(posWord):
                valueList.append(combineWords(sematic_Model.word_list[index], index))

        if cooList:
            coo_list = list(set(cooList))
        print("Step:2 返回词性:>>>>>>\n")
        print("名词词性:>>>>>", nounList)
        print("并列名词:>>>>>", cooList)
        print("动词词性:>>>>>", verbList)
        print("形容词性:>>>>>", adjList)
        print("属性词:>>>>>>>", attributeList)
        print("--------------------------------------------")

        analysisModel = SematicAnalysisModel(sematic_Model, nounList, cooList, verbList, adjList,attributeList)
        sematicSetting(analysisModel)

    else:
        print("数组为空，不予处理")


def combineWords(word, id):
    combine_word = word + "-" + str(id)
    return combine_word


def findInstanceWord(word):
    instance, instance_type = lexicon.receiveInstanceInfo()
    if word in instance:
        return True

    return False

