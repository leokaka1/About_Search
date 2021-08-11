
def createCypher(wordDict):
    print("Step:4 把分解出的关系解释成Cypher语句\n")
    print("wordDict为:>>>>>>",wordDict)

    # cypherstr = ""
    #
    # for index,item in enumerate(wordList):
    #     if not index == len(wordList) - 1:
    #         temp = "[{}]->".format(item)
    #         cypherstr += temp
    #     else:
    #         temp = "[{}]".format(item)
    #         cypherstr += temp
    #
    # # TODO：待处理最后的结构
    # print("模拟出的Cypher语句:>>>>>>>",cypherstr)

# # 名词消歧
# def nounsDisambiguration(analysisModel:SematicAnalysisModel):
#     # print("nouns:>>>>>",analysisModel.posModel.nouns)
#     nouns = analysisModel.posModel.nouns
#     # 消除歧义
#     disambiguration_list = open(r"G:\About_Search\Search_Demo_1\resources\disambiguation",encoding="utf-8").readlines()
#
#     for item in disambiguration_list:
#         item = item.strip().split("-")
#         cur_word = item[0]
#         dis_word = item[1]
#         if cur_word in nouns:
#             index = nouns.index(cur_word)
#             nouns.remove(cur_word)
#             nouns.insert(index,dis_word)
#
#     print(nouns)