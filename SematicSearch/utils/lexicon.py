from SematicSearch.config import *


class Lexicon:
    def __init__(self):
        self.instances_lines = open(instance_path, encoding="utf-8").readlines()
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

    def wordInTypes(self,word):
        temp_word_list = []
        for line in self.types_lines:
            type_word = line.split("-")[0].strip()
            word_type = line.split("-")[1].strip()
            temp_word_list.append(type_word)
        if word in temp_word_list:
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
        for line in self.instances_lines:
            if word == line.split("-")[0].strip():
                return True

        return False

    def listContainInstance(self, wordlist):
        for word in wordlist:
            if self.isInstanceWords(word):
                return True

        return False

    # 获取实例的名称和type列表
    def receiveInstanceInfo(self):
        instances = []
        instances_type = []
        for item in self.instances_lines:
            item = item.strip().split("-")
            # 用"-"分割
            instance = item[0]
            instance_type = item[1]
            # 将类型和type组装成词典
            instances.append(instance)
            instances_type.append(instance_type)
        return instances, instances_type

    def getInstanceType(self, word):
        for instance_word in self.instances_lines:
            instance = instance_word.split("-")[0].strip()
            instance_type = instance_word.split("-")[1].strip()
            if word == instance:
                return instance_type
        return ""

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
    def receiveInstancesWordAndType(self, word):
        final_word = ""
        instances, instances_type = self.receiveInstanceInfo()
        if word in instances:
            index = instances.index(word)
            e_type = instances_type[index]
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

