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
        last_noun_word = self.posModel.nouns[-1]
        last_noun_deprel = self.vertexModel.wordForDeprel(last_noun_word)
        # print("lastNoun的词性", last_noun_deprel)
        return last_noun_deprel

