from SematicSearch.postag.wordPostag import WordPosttag
from SematicSearch.graphCreating.sematicgraphCreating import seperatingTypeOfWords

def manageProcess(seg,question):
    # Step 1 用户分词和词性标注

    seg_res = seg.segAndPos(question)

    # Step 2 词性图生成
    seperatingTypeOfWords(seg_res)

