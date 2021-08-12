from Search_Demo_1.sematicAnalysisModel import SematicAnalysisModel

def createCypher(wordDict,analysisModel:SematicAnalysisModel):
    print("Step:4 把分解出的关系解释成Cypher语句\n")
    print("原始句子为:>>>>>>",wordDict["sequence"])

    includeValues = wordDict["includeValues"]
    sequences = wordDict["sequence"]

    # Step 1 主语谓语消歧
    disambigurate_list = disambiguration(sequences,analysisModel)


# 消歧
def disambiguration(sequences,analysisModel:SematicAnalysisModel):
    # print("nouns:>>>>>",analysisModel.posModel.nouns)
    # 消除歧义
    disambiguration_list = open(r"G:\About_Search\Search_Demo_1\resources\disambiguation",encoding="utf-8").readlines()
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
                sequence.insert(index,dis_word)
                # print("sequence>>>",sequence)
        change_sequence.append(sequence)

    print("消除歧义之后的句子为:>>>>>>",change_sequence)