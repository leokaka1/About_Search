from SematicSearch.config import *
from SematicSearch.postag.wordPostag import WordPosttag

if __name__ == '__main__':
    print(attribute_path)
    text = "远光软件股份有限公司的投标项目"
    postag = WordPosttag()
    res = postag.segAndPos(text)