from Search_Demo_1.segmentationAndPostag import SegmentationAndPostag
from Search_Demo_1.semanticGraph import createGrammerGraph

"""
# 可以解决的问题
# HED在最后
远光软件股份有限公司投标项目的中标人√
远光软件股份有限公司的投标的项目的中标的单位 √
远光软件股份有限公司的投标的实际的项目的中标单位 √
远光软件股份有限公司的实际投标的项目的确定的中标的单位 √

远光软件股份有限公司的投标的项目的中标的单位招标人的中标单位√
远光软件股份有限公司的投标的项目的中标的单位的招标人的招标单位√

远光软件股份有限公司投标项目的招标总价
远光软件股份有限公司投标项目的总价 / （末尾属性词不完整容易删除）

# HED在"有"或者"为"描述性动词上
哪些单位有投标基于NLP的商务数据清洗项目√
远光软件股份有限公司的投标项目的中标人包含哪些 √
远光软件股份有限公司的投标项目的中标单位有哪些 √
远光软件股份有限公司投标的项目是哪些 √
远光软件股份有限公司投标项目有哪些 √
远光软件股份有限公司中标了哪些项目 √
施工标的类合同有哪些 √

# 并列关系
远光软件股份有限公司和湖南大唐先一科技有限公司的投标项目 √

# 问属性
远光软件股份有限公司的交付时间是什么时候 √
远光软件股份有限公司的招标金额是多少 √

# 问属性值
合同总价为100万的项目有哪些
2021年的项目有哪些


合同总价和招标总价最多的合同 
合同金额最多的合同
合同金额和中标次数最多的合同
中标最多的单位
施工标的类合同都有哪些单位中标

远光软件股份有限公司和湖南大唐先一科技有限公司的中标合同的的招标金额大于100万
远光软件股份有限公司和湖南大唐先一科技有限公司和北京科东电力智控有限公司的中标合同

北京通用类型项目有哪些
2020年招标文件
2020年招标了哪些类型的项目
2020年投标公司有哪些
2020年远光软件股份有限公司有投标服务类项目吗
合同金额大于100万的项目
有超过一千万的项目吗
施工标的类项目都有哪些公司中标
施工标的类合同有哪些
远光软件股份有限公司有投标施工类合同项目吗
远光软件股份有限公司中标项目的类型
远光软件股份有限公司有签服务标的类项目合同吗




----------------------------------------------------
基于NLP的商务数据清洗项目投标单位有哪些？√
哪些单位有投标基于NLP的商务数据清洗项目？√
北京通用类项目有哪些？
2020年招标文件
2020年招标那些类型的项目
2020年投标公司有哪些
2020年远光股份有限公司有投标服务类项目吗？
合同金额大于100的项目
有超过一千万的合同吗
服务类有超过一千万的项目吗
服务类项目有超过一千万的吗

基于NLP的商务数据清洗项目中标单位资质文件有哪些 ×？
施工标的类项目都有哪些公司中标？
施工标的类合同有哪些？

远光股份有限公司 有投标施工类 项目吗？

远光股份有限公司中标项目的类型
远光股份有签服务标的类项目合同吗？
远光股份服务（标的类型）项目合同
远光股份签订合同的企业（有哪些）
远光股份有限公司与中国水利电力物资集团有限公司有签订合同吗？
那家（招标）代理机构代招标次数最多？
中标最多的单位？
远光股份有限公司是中标最多的公司吗？
仅次于远光股份有限公司中标次数的公司？
远光股份有限公司中标次数排第几
中标次数排前十单位？
不同类型项目哪家单位中标最多？
投标次数和中标次数最多的企业
投标最多的企业中标次数是最多的吗？
北京施工类项目金额最高的是?金额是多少？
去年那种类型项目投资最多


"""
if __name__ == '__main__':
    seg_pos = SegmentationAndPostag()

    while(True):
        print("--------------------------------------------")
        input_text = input("请输入用户的问题:>>>>>>>>")
        seg_res = seg_pos.segAndPos(input_text)
        createGrammerGraph(seg_res)
        # col.colparse(seg_res[0])
