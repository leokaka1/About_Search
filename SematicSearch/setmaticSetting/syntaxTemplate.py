from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils import *

lexicon = Lexicon()


class Template:
    def __init__(self, model: SematicAnalysisModel):
        self.model = model
        self.final_action_dict = {"entities": [], "sequences": [], "degree": [], "time": []}
        self.sequence = []
        self.degrees = []
        self.nouns = self.model.nouns
        self.verbs = self.model.verbs
        self.adjs = self.model.adjs
        self.values = self.model.values
        self.head_list = self.model.vertexModel.head_list
        self.word_list = self.model.vertexModel.word_list

        # 把找出来的实例给终极字典
        self.entities = self.findEntityWords()
        self.final_action_dict["entities"] = self.entities

        # 时间赋值
        if self.values:
            for value in self.values:
                value, _ = wordAndIndex(value)
                if self.model.vertexModel.wordForPos(value) == "TIME":
                    self.final_action_dict["time"] = value

        # 如果形容词和动词都修饰HED，那么就把adj给v
        for word in self.adjs:
            word, _ = wordAndIndex(word)
            if degreeWord(word) and word not in self.degrees:
                self.degrees.append(word)
        self.final_action_dict["degree"] = self.degrees

    # 如果只有ATT修饰HED
    # 第①种情况
    def has_HED_Words(self):
        # 没有形容词修饰，比如有形容词修饰：最多-最少之类的
        if not self.adjs:
            # 有verb的时候
            if self.verbs:
                for index, verb in enumerate(self.verbs):
                    word, position = wordAndIndex(verb)
                    head = self.head_list[position]
                    target_word = self.word_list[head]
                    self.sequence.append(word)
                    self.sequence.append(target_word)

                # 判断HED在不在句子中，如果不在就添加到末尾
                hed = self.model.getHEDWord()
                if hed and hed not in self.sequence:
                    self.sequence.append(hed)
            else:
                for noun in self.nouns:
                    noun, position = wordAndIndex(noun)
                    if not lexicon.isInstanceWords(noun):
                        self.sequence.append(noun)
        else:
            # 如果有动词
            if self.verbs:
                # 再处理动词
                for word in self.verbs:
                    word, position = wordAndIndex(word)
                    head = self.head_list[position]
                    targetword = self.word_list[head]
                    # 如果动词对应的词是HED，则是独立的，直接添加
                    if self.model.isHedWord(targetword):
                        self.sequence.append(targetword)
                        self.sequence.append(word)
                    else:
                        # 如果对应的词不是独立的就拼接
                        actionword = word + targetword
                        self.sequence.append(actionword)
                # 判断HED在不在句子中，如果不在就添加到末尾
                hed = self.model.getHEDWord()
                if hed and hed not in self.sequence:
                    self.sequence.append(hed)
            else:
                for noun in self.nouns:
                    noun, position = wordAndIndex(noun)
                    self.sequence.append(noun)
        self.final_action_dict["sequences"] = self.sequence

        return self.final_action_dict

    # 如果只有主语和中心词
    # 第②种情况
    def has_SBV_HED_Words(self):
        if not self.adjs:
            for verb in self.verbs:
                verb, position = wordAndIndex(verb)
                if not self.model.isHedWord(verb):
                    target_word = self.model.vertexModel.headIndexForWord(position)
                    modified_word = self.model.vertexModel.modifiedWord(verb)
                    self.sequence.append(verb)
                    self.sequence.append(target_word)
                    self.sequence = modified_word + self.sequence

                    # 判断HED在不在句子中，如果不在就添加到末尾
                    hed = self.model.getHEDWord()
                    if hed and hed not in self.sequence:
                        self.sequence.append(hed)
                else:
                    # 如果是HED词
                    sbv_word = self.model.getverbSBV(verb)
                    self.sequence.append(sbv_word)
        else:
            for verb in self.verbs:
                word, position = wordAndIndex(verb)
                head = self.head_list[position]
                targetword = self.word_list[head]
                modified_word = self.model.vertexModel.modifiedWord(verb)
                # 如果动词对应的词是HED，则是独立的，直接添加
                if self.model.isHedWord(targetword):
                    self.sequence.append(targetword)
                    self.sequence.append(word)

                else:
                    # 如果对应的词不是独立的就拼接
                    actionword = word + targetword
                    self.sequence.append(actionword)
                    self.sequence = modified_word + self.sequence

        self.final_action_dict["sequences"] = self.sequence
        return self.final_action_dict

    # 如果有谓宾三个
    # 第③种情况
    def has_HED_VOB_Words(self):
        # 判断有没有属性值词
        if self.values:
            for noun in self.nouns:
                noun, position = wordAndIndex(noun)
                if self.model.vertexModel.wordForDeprel(noun) == "VOB" or self.model.vertexModel.wordForDeprel(noun) == "HED":
                    self.sequence.append(noun)
            # 属性值词结合
            values = []
            for value in self.values:
                value, _ = wordAndIndex(value)
                target_value_word = self.model.vertexModel.wordForTargetWord(value)
                symbol = degreeSymbol(target_value_word)
                if symbol:
                    value_str = symbol + value
                    values.append(value_str)

            self.final_action_dict["degree"] = values
        self.final_action_dict["sequences"] = self.sequence
        return self.final_action_dict


    # 如果有主谓宾三个
    # 第④种情况
    def has_SBV_HED_VOB_Words(self):
        pass

    # 如果只有宾
    # 第⑤种情况
    def has_VOB_HED_Words(self):
        pass

    # 如果有状语，介宾和动宾
    # 第⑥种情况
    def has_ADV_POB_VOB_SBV_HED_Words(self):
        pass

    # 只有状中，介宾，
    # 第⑦种情况
    def has_ADV_POB_VOB_HED_Words(self):
        pass

    # 查找句子中的实例
    def findEntityWords(self):
        nouns = self.model.nouns
        entities, entities_type = lexicon.receiveEntitiesInfo()
        entity_list = []

        for noun in nouns:
            noun = noun.split("-")[0]
            if noun in entities:
                word = lexicon.receiveEntitiesWordAndType(noun)
                entity_list.append(word)

        print("1.搜索实例词>>>>>>>", entity_list)
        return entity_list


def wordAndIndex(word):
    words = word.split("-")[0]
    index = int(word.split("-")[1])
    return words, index
