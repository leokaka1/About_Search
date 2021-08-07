from LAC import LAC
from ddparser import DDParser


class SegmentationAndPostag:
    def __init__(self):
        self.lac = LAC()
        self.lac.load_customization(r"G:\About_Search\Search_Demo_1\resources\user_dicts", sep=None)
        self.ddp = DDParser()

    def segAndPos(self,question):

        # 分词
        seg_res = self.lac.run(question)
        print("使用用户自定义词典分词结果:>>>>", seg_res)
        # 词语列表
        wordList = seg_res[0]
        # 词性列表
        posList = seg_res[1]

        # 对分词后的词语进行依存分析
        col_res = self.ddp.parse_seg([wordList])

        #组装成["word":[],"pos":[]."deprel":[]]  也就是词语，词性，和句法结构的组合
        print(col_res)
        segAndpos_list = [{'word':col_res[0]["word"],"pos":posList,"deprel":col_res[0]["deprel"]}]
        print("返回最终的分词和词性分析的数组:>>>>>>",segAndpos_list)

        return segAndpos_list

