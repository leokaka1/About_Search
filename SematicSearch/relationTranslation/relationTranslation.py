from SematicSearch.model.analysisModel import SematicAnalysisModel

class RelationTranslation:
    def __init__(self,analysisModel: SematicAnalysisModel,res_dict):
        self.model = analysisModel
        self.res_dict = res_dict
        self.relationTranslate()

    def relationTranslate(self):
        print("Step:5 组成关系:>>>>>>\n")
        self.indexToRealWord()
        print(self.res_dict)

    def indexToRealWord(self):
        if self.res_dict:

            instances = self.res_dict["instances"].copy()
            entities = self.res_dict["entities"].copy()
            sequences = self.res_dict["sequences"].copy()

            temp_instance_list=[]
            for instance_index in instances:
                instance_word = self.model.vertexModel.indexForWord(instance_index)
                temp_instance_list.append(instance_word)

            temp_entities_list = []
            for entity_index in entities:
                entity_word = self.model.vertexModel.indexForWord(entity_index)
                temp_entities_list.append(entity_word)

            temp_sequence_list = []
            for sequence_index in sequences:
                sequence_word = self.model.vertexModel.indexForWord(sequence_index)
                temp_sequence_list.append(sequence_word)

            self.res_dict["entities"] = temp_entities_list
            self.res_dict["sequences"] = temp_sequence_list
            self.res_dict["instances"] = temp_instance_list