from LAC import LAC


class WordSegmentation:
    def __init__(self):
        self.lac = LAC()
        self.lac.load_customization(r"G:\About_Search\Search_Demo_1\resources\user_dicts", sep=None)

    def word_seg(self, question):
        seg_res = self.lac.run(question)
        print("使用用户自定义词典分词结果:>>>>",seg_res)
        return seg_res
