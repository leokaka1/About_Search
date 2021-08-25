from SematicSearch.config import *


class Lexicon:
    def __init__(self):
        self.entities_lines = open(entities_path, encoding="utf-8").readlines()
        self.relations_lines = open(relations_path, encoding="utf-8").readlines()
        self.attribute_lines = open(attribute_path, encoding="utf-8").readlines()
        self.types_lines = open(types_path, encoding="utf-8").readlines()
        self.disambiguation_lines = open(disambiguation_path, encoding="utf-8").readlines()

    # 是否是属性词
    def isAttributeWords(self, word):
        for line in self.types_lines:
            if word == line.split("-")[0].strip() and line.split("-")[1].strip() == "attribute":
                return True
        return False

    def isEntityWords(self, word):
        for line in self.types_lines:
            if word == line.split("-")[0].strip() and line.split("-")[1].strip() == "entity":
                return True
        return False

    def findWordAndType(self, word, type):
        for line in self.types_lines:
            target = line.split("-")[0].strip()
            target_type = line.split("-")[1].strip()

            # print("target",target)
            # print("target_type",target_type)
            # print("word",word)
            # print("type",type)
            if word == target and type == target_type:
                return True
        return False

    def findDisWord(self):
        word_list = []
        type_list = []
        for dis_word in self.disambiguation_lines:
            # print(dis_word)
            word = dis_word.split(",")[0].strip()
            type = dis_word.split(",")[1].strip()
            word_list.append(word)
            type_list.append(type)

        return word_list, type_list

    def isInstanceWords(self, word):
        for line in self.entities_lines:
            if word == line.split("-")[0].strip():
                return True

        return False

    def listContainInstance(self, wordlist):
        for word in wordlist:
            if self.isInstanceWords(word):
                return True

        return False

    # 获取实例的名称和type列表
    def receiveEntitiesInfo(self):
        entities = []
        entities_type = []
        for item in self.entities_lines:
            item = item.strip().split("-")
            # 用"-"分割
            entity = item[0]
            entity_type = item[1]
            # 将类型和type组装成词典
            entities.append(entity)
            entities_type.append(entity_type)
        return entities, entities_type

    # 获取实例的名称和type列表
    def receiveAttributeInfo(self):
        attributes = []
        attributes_type = []
        for item in self.attribute_lines:
            item = item.strip().split("-")
            # 用"-"分割
            attribute = item[0]
            attribute_type = item[1]
            # 将类型和type组装成词典
            attributes.append(attribute)
            attributes_type.append(attribute_type)
        return attributes, attributes_type

    # 获取实例的词
    def receiveEntitiesWordAndType(self, word):
        entities, entities_type = self.receiveEntitiesInfo()
        if word in entities:
            index = entities.index(word)
            e_type = entities_type[index]
            final_word = word + "/" + e_type

        return final_word

    # 判断是否含有属性词
    def isContainAtrributeWord(self, word):
        for type in self.types_lines:
            type_word = type.split("-")[0].strip()
            type = type.split("-")[1].strip()
            if word == type_word and type == "attribute":
                return True

        return False
