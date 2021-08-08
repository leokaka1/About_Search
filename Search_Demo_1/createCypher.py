
def createCypher(wordList):
    cypherstr = ""
    print("wordList>>>",wordList)
    for index,item in enumerate(wordList):
        if not index == len(wordList) - 1:
            temp = "[{}]->".format(item)
            cypherstr += temp
        else:
            temp = "[{}]".format(item)
            cypherstr += temp

    print(cypherstr)