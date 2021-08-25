import re
import pandas as pd
from SematicSearch.utils.lexicon import *

def getNonRepeatList5(data):
    import pandas as pd
    return pd.unique(data).tolist()


# 去掉所有的标点
def removePunctuation(text):
    punctuation = '!,;:?"\'、，；？。'
    text = re.sub(r'[{}]+'.format(punctuation), ' ', text)
    return text.strip()

# 读取csv文件
def readCsv():
    csv_data = pd.read_csv(r'G:\About_Search\SematicSearch\resources\types.csv',encoding="gbk")
    print(csv_data.shape)
    csv_batch_data = csv_data.tail(3)
    # print(csv_batch_data)
    train_batch_data = csv_data["word"]
    print(train_batch_data)

if __name__ == '__main__':
    readCsv()