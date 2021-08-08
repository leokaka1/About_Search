
class SemanticGraphVertex:
    def __init__(self,sematicList):
        self.head = 0
        self.deprel = ""
        self.pos = ""
        self.word = ""
        self.headID = ""
        self.word_list= sematicList[0]["word"]
        self.pos_list = sematicList[0]["pos"]
        self.deprel_list = sematicList[0]["deprel"]
        self.head_list = [index - 1 for index in sematicList[0]["head"]]
        self.wordLength = len(self.word_list)

        # 取出HED对应的index
        for deprel in self.deprel_list:
            if deprel == "HED":
                self.headID = self.deprel_list.index(deprel)

    def sematicResponse(self,word):
        for index,item in enumerate(self.word_list):
            if word == item:
                self.head = self.head_list[index]
                self.pos = self.pos_list[index]
                self.deprel = self.deprel_list[index]

    def wordForHead(self,word):
        word_index = self.word_list.index(word)
        return self.head_list[word_index]

    def wordForDeprel(self,word):
        word_index = self.word_list.index(word)
        return self.deprel_list[word_index]

    def wordForPos(self,word):
        word_index = self.word_list.index(word)
        return self.pos_list[word_index]
