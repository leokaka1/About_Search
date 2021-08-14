from py2neo import Graph


def searchNeo4j(cypher_list, isSequence):
    print("Step:5 最终形成cypher语句\n")

    # test
    # queryForNeo4j("match (n:`人物`{name:'大傻'}) where n.age=21 return n")

    if isSequence:
        for sequence in cypher_list:
            cypher_search_str = "MATCH "
            for index, word in enumerate(sequence):
                cypher_search_str += word
            print("模拟Cypher语句为:>>>>>>", cypher_search_str)
            queryForNeo4j(cypher_search_str)
    else:
        cypher_search_str = "MATCH "
        for index, word in enumerate(cypher_list):
            cypher_search_str += word
        print("模拟Cypher语句为:>>>>>>", cypher_search_str)
        queryForNeo4j(cypher_search_str)


def queryForNeo4j(query):
    graph = Graph("http://10.10.10.161:7474", auth=("neo4j", "88116142"))
    search_query = query
    cursors = graph.run(search_query)

    if cursors:
        print("查询成功")
        for i in cursors:
            print("查询结果:>>>>>>>>", i)
    else:
        print("查询失败")


