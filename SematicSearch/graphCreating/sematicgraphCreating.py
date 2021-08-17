from SematicSearch.model.sematicModel import SemanticModel
from SematicSearch.setmaticSetting.sematicSetting import sematicSetting
from SematicSearch.utils.lexicon import Lexicon
from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils.distinguishwords import *

"""
# 构建词性分组
"""


def seperatingTypeOfWords(segAndPostList):
    lexicon = Lexicon()

    # 名词词表
    nounList = []
    # 并列关系的名词
    coo_list = []
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

        # 处理并列关系 - 句中含有COO关系的找到其对应的target word并做一个映射
        for nounWord in nounList:
            if sematic_Model.wordForDeprel(nounWord) == "COO":
                target_word = sematic_Model.wordForTargetWord(nounWord)
                if target_word in nounList:
                    coo_list.append(target_word)
                    coo_list.append(nounWord)
            if lexicon.isAttributeWords(nounWord):
                attributeList.append(nounWord)

        # 删除名词里面相同的词，避免后期再次删除
        for cooWord in coo_list:
            if cooWord in nounList:
                nounList.remove(cooWord)

        for attribute_word in attributeList:
            if attribute_word in nounList:
                nounList.remove(attribute_word)
            elif attribute_word in coo_list:
                coo_list.remove(attribute_word)

        # 处理属性值操作
        for index, posWord in enumerate(sematic_Model.pos_list):
            if posWord == "TIME" or posWord == "m" or posWord == "PER":
                valueList.append(sematic_Model.word_list[index])

        if coo_list:
            coo_list = set(coo_list)
        print("Step:2 返回词性:>>>>>>\n")
        print("名词词性:>>>>>", nounList)
        print("并列名词:>>>>>", coo_list)
        print("动词词性:>>>>>", verbList)
        print("形容词性:>>>>>", adjList)
        print("属性词:>>>>>>>", attributeList)
        print("属性值词:>>>>>", valueList)
        print("--------------------------------------------")

        analysisModel = SematicAnalysisModel(sematic_Model, nounList, coo_list, verbList, adjList, attributeList,
                                             valueList)
        sematicSetting(analysisModel)

    else:
        print("数组为空，不予处理")
