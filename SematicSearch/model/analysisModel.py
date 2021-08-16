from SematicSearch.model.vertexModel import SemanticModel

"""
词性语义分析模型
"""


class SematicAnalysisModel:
    def __init__(self, vertexModel: SemanticModel,nouns,coos,verbs,adjs,attri):
        self.vertexModel = vertexModel
        self.nouns = nouns
        self.coos = coos
        self.verbs = verbs
        self.adjs = adjs
        self.attri = attri

        self.nounsHasWords = True if len(nouns) else False
        self.coosHasWords = False if len(coos) else True
        self.verbsHasWords = True if len(verbs) else False
        self.adjsHasWords = True if len(adjs) else False
        self.attriHasWords = True if len(attri) else False

    # 分析名词数组中最后一个词的词性
    def analysisNounsLastWord(self):
        if self.posModel.nounsHasWords:
            last_noun_word = self.posModel.nouns[-1]
            last_noun_deprel = self.vertexModel.wordForDeprel(last_noun_word)
            return last_noun_deprel

    # 分析动词数组中最后一个词的词性
    def analysisVerbsLastWord(self):
        if self.posModel.verbsHasWords:
            last_verb_word = self.posModel.verbs[-1]
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

    def isValueWord(self,word):
        posWord = self.vertexModel.wordForPos(word)
        if posWord == "TIME" or posWord == "m" or posWord == "PER":
            return True
        else:
            return False



