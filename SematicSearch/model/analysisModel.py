from SematicSearch.model.sematicModel import SemanticModel

"""
词性语义分析模型
"""


class SematicAnalysisModel:
    def __init__(self, vertexModel: SemanticModel, nouns, coos, verbs, adjs, attributes, values):
        self.vertexModel = vertexModel
        self.nouns = nouns
        self.coos = coos
        self.verbs = verbs
        self.adjs = adjs
        self.attributes = attributes
        self.values = values

        self.nounsHasWords = True if len(nouns) > 0 else False
        self.coosHasWords = True if len(coos) > 0 else False
        self.verbsHasWords = True if len(verbs) > 0 else False
        self.adjsHasWords = True if len(adjs) > 0 else False
        self.attributesHasWords = True if len(attributes) > 0 else False
        self.valuesHasWords = True if len(values) > 0 else False

    # 分析名词数组中最后一个词的词性
    def analysisNounsLastWord(self):
        if self.nounsHasWords:
            last_noun_word = self.nouns[-1].split("-")[0]
            last_noun_deprel = self.vertexModel.wordForDeprel(last_noun_word)
            return last_noun_deprel

    # 分析动词数组中最后一个词的词性
    def analysisVerbsLastWord(self):
        if self.verbsHasWords:
            last_verb_word = self.verbs[-1].split("-")[0]
            last_verb_deprel = self.vertexModel.wordForDeprel(last_verb_word)
            # print("lastNoun的词性", last_verb_deprel)
            return last_verb_deprel

    # 最后一个名词是HED
    def isLastNounObject(self):
        if self.analysisNounsLastWord() == "HED":
            return True
        else:
            return False

    # 最后一个动词是HED
    def isLastVerbObject(self):
        if self.analysisVerbsLastWord() == "HED":
            return True
        else:
            return False

    # 最后一个名词或者动词是HED
    def isLastNounAndVerbObject(self):
        if self.isLastNounObject() or self.isLastVerbObject():
            return True
        else:
            return False

    # 本词是否是HED
    def isHedWord(self, word):
        deprel = self.vertexModel.wordForDeprel(word)
        if deprel == "HED":
            return True
        else:
            return False

    # 判断一个词组里面有没有HED词
    def islistContainHEDword(self, wordlist):
        for word in wordlist:
            if self.isHedWord(word):
                return True
        return False

    # 是否是SBV word
    def isSBVword(self):
        for index, deprel in enumerate(self.vertexModel.deprel_list):
            if deprel == "SBV":
                word = self.vertexModel.word_list[index]
            else:
                word = ""
        return word

    # 是否是属性值词
    def isValueWord(self, word):
        posWord = self.vertexModel.wordForPos(word)
        if posWord == "TIME" or posWord == "m" or posWord == "PER":
            return True
        else:
            return False

    # 是否是虚词，可以过滤
    def isSkipWord(self, word):
        posWord = self.vertexModel.wordForPos(word)
        if posWord == "MT":
            return True
        else:
            return False

    # 有属性值词或者有属性词
    def isValueSituation(self):
        if self.attributesHasWords or self.valuesHasWords:
            return True
        else:
            return False

    # 获取动词的SBV主语
    def getverbSBV(self, verb):
        list = []
        # verb_id = self.vertexModel.wordForId(verb)
        for word in self.vertexModel.word_list:
            if self.vertexModel.wordForTargetWord(word) == verb:
                list.append(word)

        for i in list:
            if self.vertexModel.wordForDeprel(i) == "SBV":
                return i
            else:
                return ""

    # 获取句子中的HED词
    def getHEDWord(self):
        for word in self.vertexModel.word_list:
            if self.vertexModel.wordForDeprel(word) == "HED":
                return word


    def deprelNotEqualOtherDeprel(self,deprel,deprelList):
        for i in deprelList:
            if i != deprel:
                return True

        return False

    #FIXME: 这里是判断句子中有没有包含一些类别的词
    # def contain_ATT_HED(self):
    #     for word in wordList:
    #         deprel = self.vertexModel.wordForDeprel(word)
    #         if deprel == "ATT":
    #             pass