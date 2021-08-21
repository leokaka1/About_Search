from LAC import LAC
from ddparser import DDParser
from SematicSearch.config import *
from SematicSearch.utils import *

"""
Step 1 分词
"""


class WordPosttag:
    def __init__(self, ):
        self.lac = LAC()
        self.lac.load_customization(user_dicts, sep=None)
        self.ddp = DDParser()

    def segAndPos(self, question):

        if question:
            # 去掉所有的标点
            question = removePunctuation(question)
            # 分词
            seg_res = self.lac.run(question)
            # print("使用用户自定义词典分词结果:>>>>", seg_res)
            # 词语列表
            wordList = seg_res[0]
            # 词性列表
            posList = seg_res[1]

            # 对分词后的词语进行依存分析
            col_res = self.ddp.parse_seg([wordList])

            punctuation_list = []
            for index, pos in enumerate(posList):
                if pos == "w":
                    punctuation_list.append(index)

            for i in punctuation_list[::-1]:
                del posList[i]
                del col_res[0]["word"][i]
                del col_res[0]["head"][i]
                del col_res[0]["deprel"][i]

            col_res[0]["pos"] = posList
            print("Step:1 分词和词性分析的数组:>>>>>>\n")
            print(col_res[0])
            print("--------------------------------------------")

            return col_res[0]
