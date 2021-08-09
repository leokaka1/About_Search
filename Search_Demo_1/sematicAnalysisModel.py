from Search_Demo_1.semanticVertexModel import SemanticGraphVertexModel
from Search_Demo_1.sematicPosModel import SematicPosModel

class SematicAnalysisModel:
    def __init__(self,vertexModel:SemanticGraphVertexModel,posModel:SematicPosModel):
        self.posModel = posModel
        self.vertexModel = vertexModel

    def analysisNounsLastWord(self):
        last_noun_word = self.posModel.nouns[-1]
        last_noun_deprel = self.vertexModel.wordForDeprel(last_noun_word)
        return last_noun_deprel
        # print("lastNoun的词性",last_noun_deprel)



