from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils import *

lexion = Lexicon()
class RelationTranslation:
    def __init__(self, analysisModel: SematicAnalysisModel, res_dict):
        self.model = analysisModel
        self.res_dict = res_dict
        self.relationTranslate()

    def relationTranslate(self):
        print("Step:5 组成关系:>>>>>>\n")
        self.merge()
        self.indexToRealWord()
        print(self.res_dict)

    def merge(self):
        # entity组关系
        entities = self.res_dict["entities"].copy()
        temp_entities_list = []

        for index, entity_index in enumerate(entities):
            entity_word = self.model.vertexModel.indexForWord(entity_index)
            if len(entities) > 1:
                if index != len(entities)-1:
                    temp_str = entity_word + self.model.vertexModel.indexForWord(entities[index+1])
                    if lexion.wordInTypes(temp_str):
                        temp_entities_list.append(temp_str)
                    else:
                        temp_entities_list.append(entity_word)
                    self.res_dict["entities"] = temp_entities_list
            else:
                if lexion.wordInTypes(entity_word):
                    temp_entities_list.append(entity_word)
                    self.res_dict["entities"] = temp_entities_list

        # sequence组关系
        sequences = self.res_dict["sequences"].copy()
        temp_sequence_list = []
        if len(sequences) > 1:
            for index,sequence_index in enumerate(sequences):
                sequence_word = self.model.vertexModel.indexForWord(sequence_index)
                # print(sequence_word)
                if index % 2 == 0 and index != len(sequences)-1:
                    # print(sequence_index)
                    temp_str = sequence_word + self.model.vertexModel.indexForWord(sequences[index + 1])
                    # print(temp_str)
                    if lexion.wordInTypes(temp_str):
                        # print("final>>>>",temp_str)
                        temp_sequence_list.append(temp_str)
                    else:
                        temp_sequence_list.append(sequence_word)
                        temp_sequence_list.append(self.model.vertexModel.indexForWord(sequences[index+1]))

            self.res_dict["sequences"] = temp_sequence_list
        else:
            for sequence_index in sequences:
                sequence_word = self.model.vertexModel.indexForWord(sequence_index)
                temp_sequence_list.append(sequence_word)
            self.res_dict["sequences"] = temp_sequence_list

    def indexToRealWord(self):
        if self.res_dict:
            instances = self.res_dict["instances"].copy()
            # entities = self.res_dict["entities"].copy()
            # sequences = self.res_dict["sequences"].copy()
            attributes = self.res_dict["attributes"].copy()

            temp_instance_list = []
            for instance_index in instances:
                instance_word = self.model.vertexModel.indexForWord(instance_index)
                temp_instance_list.append(instance_word)

            # temp_entities_list = []
            # for entity_index in entities:
            #     entity_word = self.model.vertexModel.indexForWord(entity_index)
            #     temp_entities_list.append(entity_word)



            final_attributes_list = []
            if attributes:
                for attris in attributes:
                    temp_attributes_list = []
                    for attributes_index in attris:
                        attribute_word = self.model.vertexModel.indexForWord(attributes_index)
                        temp_attributes_list.append(attribute_word)
                    final_attributes_list.append(temp_attributes_list)

            # self.res_dict["entities"] = temp_entities_list
            # self.res_dict["sequences"] = temp_sequence_list
            self.res_dict["instances"] = temp_instance_list
            self.res_dict["attributes"] = final_attributes_list
