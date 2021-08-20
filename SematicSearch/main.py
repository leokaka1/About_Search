from SematicSearch.manageProcess import manageProcess
from SematicSearch.postag.wordPostag import WordPosttag
#  远光软件股份有限公司的交付时间是什么时候

"""
sentence type validated
基于NLP的商务数据清洗项目投标单位有哪些？  4   √
哪些单位有投标基于NLP的商务数据清洗项目？  4   √
远光软件股份有限公司的投标的项目的中标的单位的招标人的中标单位有哪些？ 4   √
北京通用类项目有哪些？    4    √
2020年招标文件   1   
2020年招标那些类型的项目  1
2020年投标公司有哪些？    4  √
2020年公司投标有哪些项目  无
2020年远光股份有限公司有投标服务类项目吗？ 6
合同金额大于100万的项目   4   √
有超过一千万的合同吗？  3   
服务类有超过一千万的项目吗   4   ×
服务类项目有超过一千万的吗   4   √
基于NLP的商务数据清洗项目中标单位资质文件有哪些？  4   √
施工标的类项目都有哪些公司中标？    6
施工标的类合同有哪些？ 4   √
远光软件股份有限公司有投标施工类项目吗？  4 √
远光股份有限公司中标项目的类型 1   
远光软件股份有限公司有签服务标的类项目合同吗？   4 √
远光软件股份有限公司服务标的类项目合同 1   
与远光软件股份有限公司签订合同的企业有哪些   7
远光股份有限公司有跟中国水利电力物资集团有限公司有签订合同吗？ 7
那家招标代理机构招标次数最多？    2    
中标最多的单位？    2
中标次数最多的单位？  2
远光股份有限公司是中标最多的公司吗？  4   ×
仅次于远光股份有限公司中标次数的公司？ 3
远光股份有限公司中标次数排第几 4   √
中标次数排前十的单位？  4  √
不同类型项目哪家单位中标最多？ 6
投标次数和中标次数最多的企业  2
投标最多的企业中标次数是最多的吗？   4   ×
北京施工类项目金额最高的是?金额是多少？ 4  ×
去年那种类型项目投资最多    6
法人或者联系人相同的企业    无
联系人是张三的公司投标项目   4   
联系人是张三的公司有中标施工类型的项目吗    4   
投标金额大于100万的项目   4 
"""


if __name__ == '__main__':
    wordpostag = WordPosttag()
    while (True):
        print("--------------------------------------------")
        input_text = input("请输入用户的问题:>>>>>>>>")
        manageProcess(wordpostag,input_text)
