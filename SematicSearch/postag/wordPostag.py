from LAC import LAC
from ddparser import DDParser
from SematicSearch.config import *

"""
Step 1 分词
"""


class WordPosttag:
    def __init__(self, ):
        self.lac = LAC()
        self.lac.load_customization(user_dicts, sep=None)
        self.ddp = DDParser()

    def segAndPos(self,question):
        """
        用户分词方法
        :param question: 用户问题
        :return: {}
        """
        if question:
            # 分词
            seg_res = self.lac.run(question)
            # 词语列表
            wordList = seg_res[0]
            # 词性列表
            posList = seg_res[1]
            # 对分词后的词语进行依存分析
            col_res = self.ddp.parse_seg([wordList])
            col_res[0]["pos"] = posList
            print("Step:1 分词和词性分析的数组:>>>>>>\n")
            print(col_res[0])
            print("--------------------------------------------")
        else:
            col_res = []

        return col_res[0]
