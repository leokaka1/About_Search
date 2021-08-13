def searchNeo4j(cypher_list,isSequence):

    print("Step:5 最终形成cypher语句\n")

    if isSequence:
        for sequence in cypher_list:
            cypher_search_str = "MATCH"
            for index, word in enumerate(sequence):
                if index != len(sequence) - 1:
                    cypher_search_str += (word + "->")
                else:
                    cypher_search_str += word
            print("模拟Cypher语句为:>>>>>>", cypher_search_str)
    else:
        cypher_search_str = "MATCH"
        for index, word in enumerate(cypher_list):
            if index != len(cypher_list) - 1:
                cypher_search_str += (word + "->")
            else:
                cypher_search_str += word
        print("模拟Cypher语句为:>>>>>>",cypher_search_str)