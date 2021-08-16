def degreeWord(word):
    degree_word = ["超过", "大于", "越过", "少于", "小于", "为", "等于", "是", "最高", "最大", "第一", "最少", "最小", "最后"]
    if word in degree_word:
        return True
    else:
        return False


# 解析程度副词
def degreeSymbol(word):
    big = ["超过", "大于", "越过"]
    small = ["少于", "小于"]
    equal = ["为", "等于", "是"]
    biggest = ["最高", "最大", "第一"]
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

# def countWord(word):
#     countwords = ['次数']
#     if word in countwords:
