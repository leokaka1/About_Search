from SematicSearch.manageProcess import manageProcess
from SematicSearch.postag.wordPostag import WordPosttag
#  远光软件股份有限公司的交付时间是什么时候

"""
基于NLP的商务数据清洗项目投标单位有哪些？  √
哪些单位有投标基于NLP的商务数据清洗项目？  √
北京通用类型项目有哪些？
2020年招标文件
2020年招标那些类型的项目
2020年投标公司有哪些
2020年远光股份有限公司有投标服务类项目吗？
合同金额大于100的项目
有超过一千万的合同吗
服务类有超过一千万的项目吗
服务类项目有超过一千万的吗
基于NLP的商务数据清洗项目中标单位资质文件有哪些？
施工标的类项目都有哪些公司中标？    √
施工标的类合同有哪些？     √
远光股份有限公司有投标施工类项目吗？  √
远光股份有限公司中标项目的类型
远光股份有签服务标的类项目合同吗？
远光股份服务（标的类型）项目合同
与远光股份签订合同的企业（有哪些）
远光股份有限公司有跟中国水利电力物资集团有限公司有签订合同吗？
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
法人或者联系人相同的企业
联系人是张三的公司投标项目
联系人是张三的公司有中标施工类型的项目吗
"""


if __name__ == '__main__':
    wordpostag = WordPosttag()
    while (True):
        print("--------------------------------------------")
        input_text = input("请输入用户的问题:>>>>>>>>")
        manageProcess(wordpostag,input_text)
