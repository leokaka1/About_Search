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
            last_noun_word = self.nouns[-1]
            last_noun_deprel = self.vertexModel.wordForDeprel(last_noun_word)
            return last_noun_deprel

    # 分析动词数组中最后一个词的词性
    def analysisVerbsLastWord(self):
        if self.verbsHasWords:
            last_verb_word = self.verbs[-1]
            last_verb_deprel = self.vertexModel.wordForDeprel(last_verb_word)
            # print("lastNoun的词性", last_verb_deprel)
            return last_verb_deprel

    def isLastNounObject(self):
        if self.analysisNounsLastWord() == "HED":
            return True
        else:
            return False

    def isLastVerbObject(self):
        if self.analysisVerbsLastWord() == "HED":
            return True
        else:
            return False

    def isHedWord(self, word):
        deprel = self.vertexModel.wordForDeprel(word)
        if deprel == "HED":
            return True
        else:
            return False

    def isLastNounAndVerbObject(self):
        if self.isLastNounObject() or self.isLastVerbObject():
            return True
        else:
            return False

    def isSBVword(self):
        for index, deprel in enumerate(self.vertexModel.deprel_list):
            if deprel == "SBV":
                word = self.vertexModel.word_list[index]
            else:
                word = ""

        return word

    def isValueWord(self, word):
        posWord = self.vertexModel.wordForPos(word)
        if posWord == "TIME" or posWord == "m" or posWord == "PER":
            return True
        else:
            return False

    def isSkipWord(self, word):
        posWord = self.vertexModel.wordForPos(word)
        if posWord == "MT":
            return True
        else:
            return False

    def isValueSituation(self):
        if self.attributesHasWords or self.valuesHasWords:
            return True
        else:
            return False

    def verbForSBV(self,verb):
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