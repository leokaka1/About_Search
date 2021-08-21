# 是否包含程度词
def degreeWord(word):
    degree_word = ["超过", "大于", "越过", "少于", "小于", "为", "等于", "是", "最高", "最大", "第一", "最少", "最小", "最后", "最多", "相同", "仅次于"]
    if word in degree_word:
        return True

    return False


# 解析程度副词
def degreeSymbol(word):
    big = ["超过", "大于", "越过"]
    small = ["少于", "小于"]
    equal = ["为", "等于", "是"]
    biggest = ["最高", "最大", "第一", "最多"]
    smallest = ["最少", "最小", "最后"]

    if word in big:
        chargeSymbol = ">"
    elif word in small:
        chargeSymbol = "<"
    elif word in equal:
        chargeSymbol = "="
    elif word in biggest:
        chargeSymbol = "desc limit 1"
    elif word in smallest:
        chargeSymbol = "limit 1"
    else:
        chargeSymbol = ""
    return chargeSymbol


# 判断是否是表示值的词
def valueWord(word4pos):
    value_list = ["TIME", "m", "LOC", "PER"]
    if word4pos:
        if word4pos in value_list:
            return True
        else:
            return False


# 判断是否是名词词性的词
def isNounWord(pos):
    nounList = ["n", "nr", "nz", "nw", "ORG", "LOC", "PER", "TIME", "m", "r"]

    if pos in nounList:
        return True
    else:
        return False


# 判断是否是动词词性的词
def isVerbWord(pos):
    verbList = ["v", "vd", "vn"]
    if pos in verbList:
        return True
    else:
        return False


# 判断一些程度描述性形容词，如"最多"等
def isAdjWord(pos):
    if pos == "a":
        return True
    else:
        return False


def isTimeWord(pos):
    if pos == "TIME":
        return True
    else:
        return False


# 是否包含一些HED的虚拟动词
def isVerbContainedSkipHEDwords(word):
    hed_ver_list = ["有", "是", "包含", "为"]
    if word in hed_ver_list:
        return True
    else:
        return False


def countWord(word):
    countwords = ['次数', "排"]
    if word in countwords:
        return True
    return False


# 疑问词结尾
def isQuestionWord(word):
    question_word = ["哪些", "什么", "那里", "那些", "哪", "那"]
    if word in question_word:
        return True

    return False
