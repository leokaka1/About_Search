from SematicSearch.manageProcess import manageProcess
from SematicSearch.postag.wordPostag import WordPosttag
#  远光软件股份有限公司的交付时间是什么时候

if __name__ == '__main__':

    wordpostag = WordPosttag()

    while (True):
        print("--------------------------------------------")
        input_text = input("请输入用户的问题:>>>>>>>>")
        manageProcess(wordpostag,input_text)
        # col.colparse(seg_res[0])
    # text = "远光软件股份有限公司的投标项目"
