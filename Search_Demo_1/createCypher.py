
def createCypher(wordList):
    cypherstr = ""

    for index,item in enumerate(wordList):
        if not index == len(wordList) - 1:
            temp = "[{}]->".format(item)
            cypherstr += temp
        else:
            temp = "[{}]".format(item)
            cypherstr += temp

    # TODO：待处理最后的结构
    print("模拟出的Cypher语句:>>>>>>>",cypherstr)