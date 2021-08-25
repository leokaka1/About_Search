from SematicSearch.model.analysisModel import SematicAnalysisModel

class CypherCreate:
    def __init__(self,sequence_dict,model:SematicAnalysisModel):
        self.sequence_dict = sequence_dict
        self.model = model
        pass