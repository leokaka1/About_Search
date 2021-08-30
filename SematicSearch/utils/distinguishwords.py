# 是否包含程度词
def degreeWord(word):
    # print("进来的词是i>>>>>",word)
    degree_word = ["超过", "大于", "越过", "少于", "小于", "等于", "第一", "最后", "相同", "仅次于", "最多", "最少", "最大", "最小"]
    if word in degree_word:
        return True

    return False


# 解析程度副词
def degreeSymbol(word):
    big = ["超过", "大于", "越过"]
    small = ["少于", "小于"]
    biggest = ["最高", "最大", "第一", "最多"]
    smallest = ["最少", "最小", "最后"]

    if word in big:
        chargeSymbol = ">"
    elif word in small:
        chargeSymbol = "<"
    elif word in biggest:
        chargeSymbol = "max"
    elif word in smallest:
        chargeSymbol = "min"
    else:
        chargeSymbol = ""
    return chargeSymbol


# 判断是否是表示值的词
def valueWord(word4pos):
    value_list = ["TIME", "m", "LOC", "PER"]
    if word4pos:
        if word4pos in value_list:
            return True
    return False


# 判断是否是名词词性的词
def isNounWord(pos):
    nounList = ["n", "nr", "nz", "nw", "ORG", "LOC", "PER", "TIME", "m", "r"]

    if pos in nounList:
        return True

    return False


# 判断是否是动词词性的词
def isVerbWord(pos):
    verbList = ["v", "vd", "vn", "p"]
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


# def isTimeWord(pos):
#     if pos == "TIME":
#         return True
#     else:
#         return False


# 是否包含一些HED的虚拟动词
def isVerbContainedSkipHEDwords(word):
    hed_ver_list = ["有", "是", "包含", "为", "与", "跟", "和", "都", "是不是", "要", "开", "的", "并且", "有没有", "被", "叫"]
    if word in hed_ver_list:
        return True
    else:
        return False


def isSkipNounWord(word):
    skip_word_list = ["哪家", "那家", "什么", "那种","在哪里"]
    if word in skip_word_list:
        return True
    else:
        return False


def countWord(word):
    countwords = ['次数', "数量","最多","最少"]
    if word in countwords:
        return True
    return False


def rankingWord(word):
    rankingwords = ["排", "列", "名列", "排名"]
    if word in rankingwords:
        return True
    return False

def queryRanking(word):
    queryrankingWord = ["第几", "第几位", "哪一名"]
    if word in queryrankingWord:
        return True
    return False

# 疑问词结尾
def isQuestionWord(word):
    # print(word)
    question_word = ["哪些", "什么", "那些", "哪", "那", "吗", "么", "呢", "哪个", "那个", "哪类", "那类"]
    if word in question_word:
        return True

    return False
