from SematicSearch.config import *


class Lexicon:
    def __init__(self):
        self.entities_lines = open(entities_path, encoding="utf-8").readlines()
        self.relations_lines = open(relations_path, encoding="utf-8").readlines()
        self.attribute_lines = open(attribute_path, encoding="utf-8").readlines()
        self.types_lines = open(types_path, encoding="utf-8").readlines()

    # 是否是属性词
    def isAttributeWords(self, word):
        for line in self.types_lines:
            if word == line.split("-")[0].strip() and line.split("-")[1].strip() == "attribute":
                return True
            else:
                return False

    # def entitiesList(self,type_flag):
    #     word_list = []
    #     type_list = []
    #     relation_list = []
    #     if type_flag == "t":
    #         for line in self.entities_lines:
    #             word_list.append(line.split("-")[0].strip())
    #             type_list.append(line.split("-")[1].strip())
