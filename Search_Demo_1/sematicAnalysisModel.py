from Search_Demo_1.semanticVertexModel import SemanticGraphVertexModel
from Search_Demo_1.sematicPosModel import SematicPosModel

"""
词性语义分析模型
"""

class SematicAnalysisModel:
    def __init__(self, vertexModel: SemanticGraphVertexModel, posModel: SematicPosModel):
        self.posModel = posModel
        self.vertexModel = vertexModel

    # 分析名词数组中最后一个词的词性
    def analysisNounsLastWord(self):
        if self.posModel.nounsHasWords:
            last_noun_word = self.posModel.nouns[-1]
            last_noun_deprel = self.vertexModel.wordForDeprel(last_noun_word)
            # print("lastNoun的词性", last_noun_deprel)
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
