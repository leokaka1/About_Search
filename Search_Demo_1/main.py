from Search_Demo_1.segmentation import WordSegmentation
from Search_Demo_1.colsentence import CollSentence
from Search_Demo_1.segmentationAndPostag import SegmentationAndPostag

"""
远光软件股份有限公司的投标项目的中标人
施工标的类合同有哪些
"""
if __name__ == '__main__':
    seg = WordSegmentation()
    col = CollSentence()
    seg_pos = SegmentationAndPostag()

    while(True):
        input_text = input("请输入用户的问题:>>>>>>>>")
        seg_res = seg_pos.segAndPos(input_text)
        # col.colparse(seg_res[0])
