class SemanticModel:
    def __init__(self, sematicList):
        self.head = 0
        self.deprel = ""
        self.wordID = 0
        self.pos = ""
        self.word = ""
        self.headID = ""
        self.word_list = sematicList["word"]
        self.pos_list = sematicList["pos"]
        self.deprel_list = sematicList["deprel"]
        self.head_list = [index - 1 for index in sematicList["head"]]
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
        target_word_index = self.word_list.index(word)
        return self.word_list[self.head_list[target_word_index]]

    def wordForTargetIndexWord(self,pos):
        target_word_index = self.head_list[pos]
        if target_word_index != -1:
            word = self.word_list[target_word_index]
        else:
            word = ""
        return word

    def posForWord(self, pos):
        index = self.pos_list.index(pos)
        return self.word_list[index]

    def removeVerbWordList(self, word):
        self.word_list.remove(word)

    def headIndexForWord(self, index):
        index = self.head_list[index]
        if index != 0:
            word = self.word_list[index]
        else:
            word = ""
        return word

    # 找出修饰这个词的词
    def modifiedWord(self,word):
        word_index = self.word_list.index(word.split("-")[0])
        res = []
        for index,head in enumerate(self.head_list):
            if head == word_index:
                # print(self.word_list[index].split("-")[0])
                res.append(self.word_list[index].split("-")[0])

        return res

    # 找到修饰词的index
    def modifiedWordIndex(self,position):
        position_list = []
        for index,head in enumerate(self.head_list):
            if head == position:
                position_list.append(index)
        return position_list

    # 找到target_word的index
    def targetWordIndex(self,position):
        return self.head_list[position]

    def indexForWord(self,index):
        return self.word_list[index]