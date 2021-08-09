from Search_Demo_1.segmentationAndPostag import SegmentationAndPostag
from Search_Demo_1.semanticGraph import createGrammerGraph

"""
HED在最后
远光软件股份有限公司的投标项目的中标人
远光软件股份有限公司的投标项目的中标人有哪些
远光软件股份有限公司的投标的项目的中标的人
远光软件股份有限公司的投标的实际的项目的中标人
远光软件股份有限公司的实际投标的项目的确定的中标的人
合同金额和中标次数最多的合同
中标最多的单位
合同总价和招标总价最多的合同
远光软件股份有限公司和湖南大唐先一科技有限公司的中标合同

施工标的类合同有哪些

基于NLP的上午数据清晰项目投标单位/公司有哪些
哪些单位有投标基于NLP的上午数据清洗项目
北京通用类型项目有哪些
2020年招标文件
2020年招标哪些类型的项目
2020年投标公司有哪些
2020年远光软件股份有限公司有投标服务类项目吗
合同金额大于100万的项目
有超过一千万的项目吗
施工标的类项目都有哪些公司中标
施工标的类合同有哪些
远光软件股份有限公司有投标施工类合同项目吗
远光软件股份有限公司中标项目的类型
远光软件股份有限公司有签服务标的类项目合同吗

"""
if __name__ == '__main__':
    seg_pos = SegmentationAndPostag()

    while(True):
        input_text = input("请输入用户的问题:>>>>>>>>")
        seg_res = seg_pos.segAndPos(input_text)
        createGrammerGraph(seg_res)
        # col.colparse(seg_res[0])
