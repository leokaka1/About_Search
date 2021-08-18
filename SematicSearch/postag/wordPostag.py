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

    def segAndPos(self, question):
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
            # 去掉带MT的词（也就是虚词）
            deltete_list = []

            # 删除MT的虚词
            for index,deprel in enumerate(col_res[0]["deprel"]):
                if deprel == "MT":
                    deltete_list.append(index)

            for i in deltete_list[::-1]:
                del wordList[i]
                del posList[i]

            deltete_list = []
            # 删除结尾是哪些，什么的VOB词
            for index,word in enumerate(wordList):
                if self.isContainQuestionWord(word) and  col_res[0]["deprel"][index] == "VOB":
                    deltete_list.append(index)

            for i in deltete_list[::-1]:
                del wordList[i]
                del posList[i]

            # 再次区分词性
            col_res = self.ddp.parse_seg([wordList])
            col_res[0]["pos"] = posList
            print("Step:1 分词和词性分析的数组:>>>>>>\n")
            print(col_res[0])
            print("--------------------------------------------")
            return col_res[0]
        else:
            return []

    # 疑问词结尾
    def isContainQuestionWord(self,word):
        question_word = ["哪些","什么"]
        if word in question_word:
            return True

        return False