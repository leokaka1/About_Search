from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils import *

lexicon = Lexicon()


class Template:
    def __init__(self, model: SematicAnalysisModel):
        self.model = model
        self.final_action_dict = {"entities": [], "sequences": [], "count": False, "count_num": ""}
        self.sequence = []
        self.degrees = ""
        self.values_str = ""
        self.nouns = self.model.nouns
        self.verbs = self.model.verbs
        self.adjs = self.model.adjs
        self.attribute = self.model.attribute
        self.head_list = self.model.vertexModel.head_list
        self.word_list = self.model.vertexModel.word_list

        # 把找出来的实例给终极字典
        self.entities = self.findEntityWords()
        for entities in self.entities:
            index = self.model.vertexModel.word_list.index(entities)
            self.final_action_dict["entities"].append(index)
        self.entities = self.final_action_dict["entities"]

        # # 是否有次数,count
        # for word in self.model.vertexModel.word_list:
        #     if countWord(word):
        #         self.final_action_dict["count"] = True
        #         if self.values:
        #             for value in self.values:
        #                 value, _ = wordAndIndex(value)
        #                 self.final_action_dict["count_num"] = value

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
                    if hed and hed not in self.sequence and not isVerbContainedSkipHEDwords(hed):
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
        # 没有属性值的情况
        if not self.attribute:
            # step 1 遍历动词
            for verb in self.verbs:
                verb, position = wordAndIndex(verb)
                # 修饰动词的词
                modified_word_index = self.model.vertexModel.modifiedWordIndex(position)
                # 被动词修饰的词
                target_word_index = self.model.vertexModel.targetWordIndex(position)
                # print(target_word_index)
                # step 1.1 判断是否是HED动词
                # 不是HED动词
                if not self.model.isHedWord(verb):
                    # 如果target_word是entity，就不添加,并且将动词插入到第一位
                    if target_word_index not in self.entities:
                        self.sequence.append(position)
                        if target_word_index not in self.sequence \
                                and not self.model.isSkipWordsIndex(target_word_index):
                            self.sequence.append(target_word_index)
                    else:
                        self.sequence.insert(0, position)
                else:
                    # 是HED动词
                    # 如果是HED词，修饰的target不是vob修饰词，如哪些，什么之类的就添加
                    for modi_index in modified_word_index:
                        # 条件，如果修饰动词的词不是疑问词或者不是实体词，就添加进去
                        if modi_index not in self.entities \
                                and not self.model.isSkipWordsIndex(modi_index) \
                                and modi_index not in self.sequence:
                            self.sequence.append(modi_index)

                    # 如果中心词不是有，是，这种词，就添加
                    if not isVerbContainedSkipHEDwords(verb):
                        self.sequence.append(position)
            print("sequence>>>>>>>", self.sequence)
            # FIXME:有可能出现的情况，还有名词修饰名词的时候，必须把名词遍历统计完
            for noun in self.nouns:
                noun, position = wordAndIndex(noun)
                noun_target_index = self.model.vertexModel.targetWordIndex(position)
                print("target word", noun_target_index)
                if position not in self.sequence and position not in self.entities:
                    # 如果是目标的sbv就插入目标词之前
                    if self.model.vertexModel.wordForDeprel(noun) == "SBV":
                        self.sequence.insert(self.sequence.index(noun_target_index), position)
                    # 如果是目标的VOB就插到目标词后面
                    elif self.model.vertexModel.wordForDeprel(noun) == "VOB":
                        if position not in self.sequence:
                            self.sequence.insert(self.sequence.index(noun_target_index) + 1, position)
                    # 如果啥都不是就直接拼接
                    else:
                        if position not in self.sequence:
                            if noun_target_index in self.entities:
                                self.sequence.insert(0, position)
                            else:
                                # 插入到修饰词前面 / 如果不是时间词(时间词放最后)
                                if not isTimeWord(self.model.vertexModel.wordForPos(noun)):
                                    self.sequence.insert(self.sequence.index(noun_target_index),position)
                                else:
                                    self.sequence.append(position)
        else:
            # 有属性值的情况
            # 遍历动词
            for verb in self.verbs:
                verb, position = wordAndIndex(verb)
                # 目标词序号
                target_word = self.model.vertexModel.targetWordIndex(position)
                # 被修饰词序号
                modified_word_index = self.model.vertexModel.modifiedWordIndex(position)

                # 判断是不是程度词，比如有大于，等于，为之类的
                if degreeWord(verb):
                    print("position>>>>", position, target_word)
                    # step 1 找出targetword并且添加到sequence
                    if target_word \
                            and not self.model.isSkipWordsIndex(target_word) \
                            and not isVerbContainedSkipHEDwords(verb):
                        self.sequence.append(target_word)

                    # step 2 找到修饰自己的词，一般来说是SBV和VOB的主谓语和宾语
                    # print(modified_word_index)
                    for index in modified_word_index:
                        word = self.model.vertexModel.indexForWord(index)
                        # print("deprel>>>>",self.model.vertexModel.wordForDeprel(word))
                        # print("attribute>>>>",lexicon.isAttributeWords(word))
                        if lexicon.isAttributeWords(word) \
                                and index not in self.sequence \
                                and self.model.vertexModel.wordForDeprel(word) == "SBV":
                            self.sequence.append(index)
                            self.sequence.append(position)
                        elif self.model.vertexModel.wordForDeprel(word) == "VOB":
                            self.sequence.append(index)
                else:
                    # 不是程度词则组合
                    # 如果是中心词
                    if self.model.isHedWord(verb):
                        # print("position>>>>", position, target_word)
                        if not not isVerbContainedSkipHEDwords(verb):
                            self.sequence.append(position)
                            self.sequence.append(target_word)

            # 补充名词
            for noun in self.nouns:
                noun, position = wordAndIndex(noun)
                if position not in self.sequence:
                    self.sequence.append(position)

            #         if target_word and self.model.vertexModel.wordForPos(target_word) != "u":
            #             self.sequence.append(target_word)
            #         else:
            #             self.sequence.append(verb)
            #
            #         # 判断modified_word中有没有sbv
            #         # step 2 找出修饰这个词的modified_word
            #         for modi_word in modified_words:
            #             # 说明修饰词是SBV主语，添加到最前
            #             if self.model.vertexModel.wordForDeprel(modi_word) == "SBV":
            #                 self.sequence.append(modi_word)
            #                 self.sequence.append(verb)
            #             if valueWord(self.model.vertexModel.wordForPos(modi_word)):
            #                 self.sequence.append(modi_word)
            #     else:
            #         # 如果不是中心词则直接添加动词
            #         if not self.model.isHedWord(verb):
            #             self.sequence.append(verb)
            #         else:
            #             # 如果是中心词，则找到修饰中心动词的词并且不是问句词和SBV的词添加
            #             for modi_word in modified_words:
            #                 if not isQuestionWord(modi_word) and self.model.vertexModel.wordForDeprel(
            #                         modi_word) == "SBV" and modi_word not in self.sequence:
            #                     self.sequence.append(modi_word)
            #         if target_word:
            #             self.sequence.append(target_word)
            #
            # # 判断有没有遗漏的value
            # for value in self.attribute:
            #     value, _ = wordAndIndex(value)
            #     if value not in self.sequence:
            #         self.sequence.append(value)

        # 判断有count的情况
        # FIXME: eg:中标次数排前十的单位
        # if self.final_action_dict["count"]:
        #     temp_clear_list = []
        #     # 先清除sequence
        #     if self.final_action_dict["count_num"]:
        #         self.sequence.remove(self.final_action_dict["count_num"])
        #     for index, word in enumerate(self.sequence):
        #         if countWord(word):
        #             temp_clear_list.append(index)
        #     for i in temp_clear_list[::-1]:
        #         del self.sequence[i]

        # 清理疑问词
        self.clearQuestionWord()
        # 清除重复词
        self.clearRepeatWord()
        # 将sequences赋值给最终字典
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
        for index in self.sequence:
            word = self.model.vertexModel.indexForWord(index)
            if isQuestionWord(word):
                self.sequence.remove(index)

    def clearRepeatWord(self):
        for index in self.sequence:
            # word = self.model.vertexModel.indexForWord(index)
            if index in self.entities:
                self.sequence.remove(index)


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
