import re


def getNonRepeatList5(data):
    import pandas as pd
    return pd.unique(data).tolist()


# 去掉所有的标点
def removePunctuation(text):
    punctuation = '!,;:?"\'、，；？。'
    text = re.sub(r'[{}]+'.format(punctuation), ' ', text)
    return text.strip()
