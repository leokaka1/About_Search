from SematicSearch.postag.wordPostag import WordPosttag


def manageProcess(question):
    # Step 1 用户分词和词性标注
    wordpostag = WordPosttag(question)
    seg_res = wordpostag.segAndPos()

    # Step 2 词性图生成
