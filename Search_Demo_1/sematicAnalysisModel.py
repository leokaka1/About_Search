from Search_Demo_1.semanticVertexModel import SemanticGraphVertexModel
from Search_Demo_1.sematicPosModel import SematicPosModel

class SematicAnalysisModel:
    def __init__(self,vertexModel:SemanticGraphVertexModel,posModel:SematicPosModel):
        self.posModel = posModel
        self.vertextModel = vertexModel

    def analysisNounsLastWord(self):
        last_noun_word = self.posModel.nouns[-1]
        last_noun_pos = self.vertextModel.wordForPos(last_noun_word)
        print(last_noun_pos)



