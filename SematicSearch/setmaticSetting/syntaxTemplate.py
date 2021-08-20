from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils import *

lexicon = Lexicon()


class Template:
    def __init__(self, model: SematicAnalysisModel):
        self.model = model
        self.final_action_dict = {"entities": [], "sequences": [], "values": False, "count": False,"count_num":""}
        self.sequence = []
        self.degrees = ""
        self.values_str = ""
        self.nouns = self.model.nouns
        self.verbs = self.model.verbs
        self.adjs = self.model.adjs
        # self.values = self.model.values
        self.head_list = self.model.vertexModel.head_list
        self.word_list = self.model.vertexModel.word_list

        # 把找出来的实例给终极字典
        self.entities = self.findEntityWords()
        self.final_action_dict["entities"] = self.entities

        # # 是否有次数,count
        for word in self.model.vertexModel.word_list:
            if countWord(word):
                self.final_action_dict["count"] = True
                if self.values:
                    for value in self.values:
                        value, _ = wordAndIndex(value)
                        self.final_action_dict["count_num"] = value

        # 时间赋值
        # if self.values:
        #     for value in self.values:
        #         value, _ = wordAndIndex(value)
        #         if self.model.vertexModel.wordForPos(value) == "TIME":
        #             self.final_action_dict["time"] = value

        # 如果形容词和动词都修饰HED，那么就把adj给v
        # if self.adjs:
        #     for word in self.adjs:
        #         word, _ = wordAndIndex(word)
        #         if degreeWord(word) and word not in self.degrees:
        #             self.degrees = word
        #         self.final_action_dict["count"] = True
        #         self.final_action_dict["count_num"] = word

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
                    if target_word:
                        self.sequence.append(target_word)
                    self.sequence = modified_word + self.sequence

                    # 判断HED在不在句子中，如果不在就添加到末尾
                    hed = self.model.getHEDWord()
                    if hed and hed not in self.sequence and not isVerbContainedHEDwords(hed):
                        self.sequence.append(hed)
                else:
                    # 如果是HED词
                    sbv_word = self.model.getverbSBV(verb)
                    if sbv_word:
                        for sbv in sbv_word:
                            if sbv not in self.sequence:
                                self.sequence.append(sbv)
        else:
            for verb in self.verbs:
                word, position = wordAndIndex(verb)
                head = self.head_list[position]
                if head != -1:
                    targetword = self.word_list[head]
                modified_word = self.model.vertexModel.modifiedWord(verb)
                # 如果动词对应的词是HED，则是独立的，直接添加
                if self.model.isHedWord(targetword):
                    self.sequence.append(targetword)
                    self.sequence.append(word)
                else:
                    self.sequence.append(word)
                    self.sequence = modified_word + self.sequence

        self.final_action_dict["sequences"] = self.sequence
        return self.final_action_dict

    # 如果有谓宾三个
    # 第③种情况
    def has_HED_VOB_Words(self):
        # 判断有没有属性值词
        # 有超过一千万的合同吗？
        # 中标次数排前十的单位？
        if self.values:
            vob_word = self.model.getVOBWord()
            for vobs in vob_word:
                if self.model.vertexModel.wordForPos(vobs) != "m":
                    self.sequence.append(vobs)

            # 遍历动词
            for verb in self.verbs:
                verb, position = wordAndIndex(verb)
                if not self.model.isHedWord(verb):
                    target_word = self.model.vertexModel.wordForTargetIndexWord(position)
                    if degreeWord(verb):
                        symobl = degreeSymbol(verb)
                        self.sequence.append(symobl)
                    else:
                        self.sequence.append(verb)
                    if not countWord(target_word) and target_word not in self.sequence:
                        self.sequence.append(target_word)

            if not self.final_action_dict["count"]:
                for value in self.values:
                    value, _ = wordAndIndex(value)
                    self.sequence.append(value)

            self.final_action_dict["values"] = True
        else:
            for verb in self.verbs:
                verb, position = wordAndIndex(verb)
                if not self.model.isHedWord(verb):
                    target_word = self.model.vertexModel.wordForTargetIndexWord(position)
                    self.sequence.append(verb)
                    if target_word not in self.sequence:
                        self.sequence.append(target_word)

            for noun in self.nouns:
                noun, position = wordAndIndex(noun)
                target_word = self.model.vertexModel.wordForTargetIndexWord(position)
                if self.model.isHedWord(target_word):
                    if target_word not in self.sequence:
                        self.sequence.append(target_word)

        self.final_action_dict["sequences"] = self.sequence
        return self.final_action_dict

    # 如果有主谓宾三个
    # 第④种情况 - （important）
    def has_SBV_HED_VOB_Words(self):
        # step 1 遍历动词
        for verb in self.verbs:
            verb, position = wordAndIndex(verb)
            # 修饰动词的词
            modified_words = self.model.vertexModel.modifiedWord(verb)
            # 被动词修饰的词
            target_word = self.model.vertexModel.wordForTargetIndexWord(position)

            # step 1.1 判断是否是HED动词
            # 不是HED动词
            if not self.model.isHedWord(verb):
                # 如果target_word是entity，就不添加,并且将动词插入到第一位
                if target_word not in self.entities:
                    self.sequence.append(verb)
                    if target_word not in self.sequence:
                        self.sequence.append(target_word)
                else:
                    self.sequence.insert(0, verb)
            else:
                # 是HED动词
                # 如果是HED词，修饰的target不是vob修饰词，如哪些，什么之类的就添加
                for modi_word in modified_words:
                    # 条件，如果修饰动词的词不是疑问词或者不是实体词，就添加进去
                    if modi_word not in self.entities \
                            and modi_word not in self.sequence \
                            and self.model.vertexModel.wordForPos(modi_word) != "xc":
                        self.sequence.append(modi_word)


        # 没有属性值的情况
        # if not self.values:
        #     # step 1 遍历动词
        #     for verb in self.verbs:
        #         verb, position = wordAndIndex(verb)
        #         # 修饰动词的词
        #         modified_words = self.model.vertexModel.modifiedWord(verb)
        #         # 被动词修饰的词
        #         target_word = self.model.vertexModel.wordForTargetIndexWord(position)
        #
        #         # step 1.1 判断是否是HED动词
        #         # 不是HED动词
        #         if not self.model.isHedWord(verb):
        #             # 如果target_word是entity，就不添加,并且将动词插入到第一位
        #             if target_word not in self.entities:
        #                 self.sequence.append(verb)
        #                 if target_word not in self.sequence:
        #                     self.sequence.append(target_word)
        #             else:
        #                 self.sequence.insert(0, verb)
        #         else:
        #             # 是HED动词
        #             # 如果是HED词，修饰的target不是vob修饰词，如哪些，什么之类的就添加
        #             for modi_word in modified_words:
        #                 # 条件，如果修饰动词的词不是疑问词或者不是实体词，就添加进去
        #                 if modi_word not in self.entities \
        #                         and modi_word not in self.sequence \
        #                         and self.model.vertexModel.wordForPos(modi_word) != "xc":
        #                     self.sequence.append(modi_word)
        # else:
        #     # 将final中value置为True
        #     self.hasValues(True)
        #     # 有属性值的情况
        #     # 遍历动词
        #     for verb in self.verbs:
        #         verb, position = wordAndIndex(verb)
        #         target_word = self.model.vertexModel.wordForTargetIndexWord(position)
        #         modified_words = self.model.vertexModel.modifiedWord(verb)
        #
        #         # 判断是不是程度词，比如有大于，等于，为之类的
        #         # 如果是degree word
        #         if degreeWord(verb):
        #             # step 1 找出targetword并且添加到sequence
        #             if target_word and self.model.vertexModel.wordForPos(target_word) != "u":
        #                 self.sequence.append(target_word)
        #             else:
        #                 self.sequence.append(verb)
        #
        #             # 判断modified_word中有没有sbv
        #             # step 2 找出修饰这个词的modified_word
        #             for modi_word in modified_words:
        #                 # 说明修饰词是SBV主语，添加到最前
        #                 if self.model.vertexModel.wordForDeprel(modi_word) == "SBV":
        #                     self.sequence.append(modi_word)
        #                     self.sequence.append(verb)
        #                 if valueWord(self.model.vertexModel.wordForPos(modi_word)):
        #                     self.sequence.append(modi_word)
        #         else:
        #             # 如果不是中心词则直接添加动词
        #             if not self.model.isHedWord(verb):
        #                 self.sequence.append(verb)
        #             else:
        #                 # 如果是中心词，则找到修饰中心动词的词并且不是问句词和SBV的词添加
        #                 for modi_word in modified_words:
        #                     if not isQuestionWord(modi_word) and self.model.vertexModel.wordForDeprel(
        #                             modi_word) == "SBV" and modi_word not in self.sequence:
        #                         self.sequence.append(modi_word)
        #             if target_word:
        #                 self.sequence.append(target_word)
        #
        #     # 判断有没有遗漏的value
        #     for value in self.values:
        #         value, _ = wordAndIndex(value)
        #         if value not in self.sequence:
        #             self.sequence.append(value)

        # 判断有count的情况
        # FIXME: eg:中标次数排前十的单位
        if self.final_action_dict["count"]:
            temp_clear_list = []
            # 先清除sequence
            if self.final_action_dict["count_num"]:
                self.sequence.remove(self.final_action_dict["count_num"])
            for index, word in enumerate(self.sequence):
                if countWord(word):
                    temp_clear_list.append(index)
            for i in temp_clear_list[::-1]:
                del self.sequence[i]

        # 清理疑问词
        self.clearQuestionWord()
        self.final_action_dict["sequences"] = self.sequence
        return self.final_action_dict

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
        coos = self.model.coos
        entities, entities_type = lexicon.receiveEntitiesInfo()
        entity_list = []

        for noun in nouns:
            noun = noun.split("-")[0]
            if noun in entities:
                # word = lexicon.receiveEntitiesWordAndType(noun)
                entity_list.append(noun)

        if not len(entity_list):
            for coo in coos:
                coo = coo.split("-")[0]
                if coo in entities:
                    entity_list.append(coo)

        print("1.搜索实例词>>>>>>>", entity_list)
        return entity_list

    # 是否含有属性值
    def hasValues(self, charge):
        self.final_action_dict["values"] = charge

    # 清理疑问词
    def clearQuestionWord(self):
        for word in self.sequence:
            if isQuestionWord(word):
                self.sequence.remove(word)


def wordAndIndex(word):
    words = word.split("-")[0]
    index = int(word.split("-")[1])
    return words, index


def wordListwithoutIndex(wordList):
    word_list = []
    for word in wordList:
        word, _ = wordAndIndex(word)
        word_list.append(word)
    return word_list
