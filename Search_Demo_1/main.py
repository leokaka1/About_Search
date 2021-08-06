from Search_Demo_1.segmentation import WordSegmentation

"""
远光软件股份有限公司的投标项目
"""
if __name__ == '__main__':
    word_seg = WordSegmentation()
    input_text = input("请输入用户的问题:>>>>>>>>")
    word_seg.word_seg(input_text)