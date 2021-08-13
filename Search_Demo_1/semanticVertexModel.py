import re
class SemanticGraphVertexModel:
    def __init__(self, sematicList):
        self.head = 0
        self.deprel = ""
        self.wordID = 0
        self.pos = ""
        self.word = ""
        self.headID = ""
        self.word_list = sematicList[0]["word"]
        self.pos_list = sematicList[0]["pos"]
        self.deprel_list = sematicList[0]["deprel"]
        self.head_list = [index - 1 for index in sematicList[0]["head"]]
        self.wordLength = len(self.word_list)
        self.isHasCOO = False

        # 取出HED对应的index
        for deprel in self.deprel_list:
            if deprel == "HED":
                self.headID = self.deprel_list.index(deprel)
            elif deprel == "COO":
                # 判断有没有并列关系
                self.isHasCOO = True

        # 判断hed是否在最后一位上
        self.hedLast = True if self.headID == len(self.word_list) - 1 else False

    def sematicResponse(self, word):
        for index, item in enumerate(self.word_list):
            if word == item:
                self.head = self.head_list[index]
                self.pos = self.pos_list[index]
                self.deprel = self.deprel_list[index]

    def wordForHead(self, word):
        word_index = self.word_list.index(word)
        return self.head_list[word_index]

    def wordForDeprel(self, word):
        word_index = self.word_list.index(word)
        return self.deprel_list[word_index]

    def wordForPos(self, word):
        word_index = self.word_list.index(word)
        return self.pos_list[word_index]

    def wordForId(self, word):
        return self.word_list.index(word)

    def wordForTargetWord(self, word):
        target_word_index = self.wordForHead(word)
        return self.word_list[target_word_index]

    def posForWord(self,pos):
        index = self.pos_list.index(pos)
        return self.word_list[index]

    def removeVerbWordList(self,word):
        self.word_list.remove(word)

    # 判断是否是表示值的词
    def wordisValue(self,word):
        value_list = ["TIME","m","LOC","PER"]
        word_pos = self.wordForPos(word)
        if word_pos in value_list:
            return True
        else:
            return False

    # 解析程度副词
    def wordForDegreeSymbol(self,word):
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


