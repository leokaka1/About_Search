from Search_Demo_1.semanticVertexModel import SemanticGraphVertexModel
from Search_Demo_1.sematicPosModel import SematicPosModel

class SematicAnalysisModel:
    def __init__(self,vertexModel:SemanticGraphVertexModel,posModel:SematicPosModel):
        self.posModel = posModel
        self.vertextModel = vertexModel

