from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils import *

lexicon = Lexicon()

"""
崩溃的句子
2020年项目的投标的单位是
"""


class Template:
    def __init__(self, model: SematicAnalysisModel):
        self.model = model
        self.final_action_dict = {"instances": [], "entities": [], "sequences": [], "attributes": [], "count": False,
                                  "ranking": "", "isContainValue": False}

        self.degrees = ""
        self.values_str = ""
        self.nouns = self.model.nouns
        self.verbs = self.model.verbs
        self.adjs = self.model.adjs
        self.coos = self.model.coos
        self.attribute = self.model.attribute
        self.head_list = self.model.vertexModel.head_list
        self.word_list = self.model.vertexModel.word_list

        self.preprocess()
        self.sequence = self.final_action_dict["sequences"]
        self.entities = self.final_action_dict["entities"]
        self.attributes = self.final_action_dict["attributes"]
        self.instances = self.final_action_dict["instances"]
        self.containValue = self.final_action_dict["isContainValue"]
        self.count = self.final_action_dict["count"]
        self.ranking = self.final_action_dict["ranking"]

    # 预处理
    def preprocess(self):
        # 是否有次数,count
        for word in self.model.vertexModel.word_list:
            if degreeWord(word):
                self.final_action_dict["count"] = True

        # 判断句子中是否含有属性词，如果含有就把isContainValue置为True
        for word in self.model.vertexModel.word_list:
            # 如果一句话里面含有属性词或者含有一些金额，日期等词，就判断包含属性
            if lexicon.isContainAtrributeWord(word) or self.model.isValueWord(word):
                self.final_action_dict["isContainValue"] = True

        # 把找出来的实例给终极字典
        instances_list = self.findInstanceWords()
        for instances in instances_list:
            # print("instances===>",instances)
            index = self.model.vertexModel.word_list.index(instances)
            self.final_action_dict["instances"].append(index)

        # 判断句子中是否有属性或者属性值的存在，如果有就必须要处理实例或者实体
        if self.final_action_dict["isContainValue"]:
            # entities = self.final_action_dict["entities"]
            # 如果属性值修饰的词是entitiy或者修饰词的target是entitiy，那么就存入entity中
            r_list = self.model.findAmountOrTimeWordIndex()
            for attribute_value_index in r_list:
                target_word_index = self.model.vertexModel.wordForTargetIndex(attribute_value_index)
                target_plus_word_index = self.model.vertexModel.wordForTargetIndex(target_word_index)

                if self.model.isWordInEntitiesList(target_word_index) \
                        and target_word_index not in self.final_action_dict["entities"]:
                    self.final_action_dict["entities"].append(target_word_index)

                if self.model.isWordInEntitiesList(target_plus_word_index) \
                        and target_plus_word_index not in self.final_action_dict["entities"]:
                    self.final_action_dict["entities"].append(target_plus_word_index)

        # 判断句子中是否有ranking的词，如果有，那么就显示排名第几
        # 找最多，最少等程度词
        temp_degree_str = ""
        for index, word in enumerate(self.model.vertexModel.word_list):
            if degreeWord(word):
                symbol = degreeSymbol(word)
                if symbol:
                    temp_degree_str += symbol
                    self.final_action_dict["ranking"] = temp_degree_str

            elif rankingWord(word):
                if self.word_list[index + 1]:
                    next_count_word = self.word_list[index + 1]
                    if queryRanking(next_count_word):
                        temp_degree_str += "query"
                        self.final_action_dict["ranking"] = temp_degree_str
                    else:
                        if self.model.vertexModel.wordForPos(next_count_word) == "m":
                            temp_degree_str += next_count_word
                        elif self.model.vertexModel.wordForPos(self.word_list[index + 2]) and self.word_list[index + 2]:
                            temp_degree_str += self.word_list[index + 2]
                        self.final_action_dict["ranking"] = temp_degree_str

        # FIXME: 执行属性
        self.isAttributeSequence()

    # 如果只有ATT修饰HED
    # 第①种情况
    def has_HED_Words(self):
        # FIXME: situation 1.1：只有ATT和HED，一般最后是HED结尾，结尾的词是名词
        #   eg:远光软件股份有限公司投标项目的中标人。
        # 有verb的时候
        if self.verbs:
            for index, verb in enumerate(self.verbs):
                verb, position = wordAndIndex(verb)
                # 找到这个verb对应的target_word的index然后拼接到sequence中
                targetWord_index = self.model.vertexModel.wordForTargetIndex(position)
                if not isVerbContainedSkipHEDwords(verb):
                    self.sequence.append(position)
                if targetWord_index not in self.sequence and targetWord_index not in self.entities:
                    self.sequence.append(targetWord_index)

            # 判断HED在不在句子中，如果不在就添加到末尾targetWordIndex
            # hed_word, hed_index = self.model.getHEDWord()
            # if hed_index and hed_index not in self.sequence:
            #     self.sequence.append(hed_index)

        # self.dealWithNouns()
        # # 处理剩余的名词(如果词不在序列中并且不是问句词就添加)
        # for noun in self.nouns:
        #     noun, position = wordAndIndex(noun)
        #     # targetWord_index = self.model.vertexModel.wordForTargetIndex(position)
        #     if position not in self.sequence \
        #             and not isQuestionWord(noun) \
        #             and position not in self.entities \
        #             and position not in self.instances:
        #         self.sequence.append(position)

        self.dealWithEnd()
        return self.final_action_dict

    # 如果只有主语和中心词
    # 第②种情况
    def has_SBV_HED_Words(self):
        # FIXME: situation 2.1：有ATT，SBV和HED
        #   eg:中标最多的单位？ - 刘德华老婆出生于 中标最多的单位？
        # 中标最多的单位？
        # 没有形容词的时候
        if not self.adjs:
            # 遍历动词
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
                    # 如果是HED词 (刘德华老婆出生于)
                    modified_word_index = self.model.vertexModel.modifiedWordIndex(position)
                    for modi_index in modified_word_index:
                        if modi_index not in self.entities and modi_index not in self.sequence:
                            self.sequence.append(modi_index)
                        if not isVerbContainedSkipHEDwords(verb):
                            self.sequence.append(position)

            # # 处理剩余名词
            for noun in self.nouns:
                noun, position = wordAndIndex(noun)
                target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                # print(noun,position,target_word_index)
                if position not in self.sequence and position not in self.entities:
                    # 如果在实例库中就添加到第一个位置
                    if target_word_index in self.entities:
                        self.sequence.insert(0, position)
                    elif target_word_index in self.sequence:
                        # 如果目标词不在实例对象中，就添加到对应修饰的词后面 -（张学友老婆出生于）
                        self.sequence.insert(self.sequence.index(target_word_index), position)
                    elif target_word_index not in self.sequence:
                        # 如果没有动词的情况
                        # eg:小王的笔记本在哪里
                        self.sequence.append(position)
                        self.sequence.append(target_word_index)
        else:
            # FIXME: 2.2 有形容词，比如最多，一般用于排序
            # 中标最多的单位？
            # 遍历动词
            for verb in self.verbs:
                verb, position = wordAndIndex(verb)
                target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                target_word = self.model.vertexModel.wordForTargetIndexWord(position)
                if position not in self.sequence:
                    if not isVerbContainedSkipHEDwords(verb):
                        self.sequence.append(position)
                    if target_word_index not in self.sequence \
                            and not countWord(target_word):
                        self.sequence.append(target_word_index)

            # 处理形容词
            for adj in self.adjs:
                adj, position = wordAndIndex(adj)
                modified_word_index = self.model.vertexModel.modifiedWordIndex(position)
                # 如果形容词是HED - （那家招标代理机构招标次数最多？）一般句尾是形容词
                if self.model.isHedIndex(position):
                    for modi_index in modified_word_index:
                        modi_word = self.model.vertexModel.indexForWord(modi_index)
                        if modi_index not in self.sequence and not countWord(modi_word):
                            self.sequence.append(modi_index)
                    self.sequence.append(position)
                else:
                    self.sequence.append(position)

            # 处理剩下的名词
            for noun in self.nouns:
                noun, position = wordAndIndex(noun)
                noun_deprel = self.model.vertexModel.wordForDeprel(noun)
                # target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                if position not in self.sequence \
                        and position not in self.entities \
                        and not countWord(noun):
                    if self.makeEntityWord(noun_deprel, word=noun):
                        self.dealWithEntities(position)

            # 处理剩下的属性词
            if self.attribute:
                for attribute in self.attribute:
                    attribute_word, position = wordAndIndex(attribute)
                    target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                    if position not in self.sequence \
                            and target_word_index in self.sequence:
                        self.sequence.insert(self.sequence.index(target_word_index), position)

        self.dealWithEnd()
        return self.final_action_dict

    # 如果有谓宾三个
    # 第③种情况
    def has_HED_VOB_Words(self):
        # 判断有没有属性值词
        # 有超过一千万的合同吗？
        # 处理动词
        # FIXME: situation 3.1：有ATT，HED和VOB
        #   eg:有超过一千万的合同吗？
        for verb in self.verbs:
            verb, position = wordAndIndex(verb)
            target_word_index = self.model.vertexModel.wordForTargetIndex(position)
            modified_word_index = self.model.vertexModel.modifiedWordIndex(position)
            if self.model.isHedIndex(position):
                if not isVerbContainedSkipHEDwords(verb):
                    self.sequence.append(position)
                else:
                    # 遍历所有的modified_word
                    for modi_word_index in modified_word_index:
                        word = self.model.vertexModel.indexForWord(modi_word_index)
                        if not isQuestionWord(word):
                            self.sequence.append(modi_word_index)

            else:
                # 不是HED词
                self.sequence.append(position)

        # 处理后续的名词
        for noun in self.nouns:
            noun, position = wordAndIndex(noun)
            target_word_index = self.model.vertexModel.wordForTargetIndex(position)
            target_word = self.model.vertexModel.indexForWord(target_word_index)
            if position not in self.sequence \
                    and not countWord(noun) \
                    and position not in self.entities:
                self.sequence.append(position)
            if not countWord(target_word) \
                    and target_word in self.sequence:
                self.sequence.insert(self.sequence.index(target_word_index), position)
        self.dealWithEnd()
        return self.final_action_dict

    # 如果有主谓宾三个
    # 第④种情况 - （important）
    def has_SBV_HED_VOB_Words(self):
        # 没有属性值的情况
        if not self.attributes:
            # step 1 遍历动词
            for verb in self.verbs:
                verb, position = wordAndIndex(verb)
                # 修饰动词的词
                modified_word_index = self.model.vertexModel.modifiedWordIndex(position)
                # 被动词修饰的词
                target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                # print("target_word_index",target_word_index)
                # step 1.1 判断是否是HED动词
                # 不是HED动词
                if not self.model.isHedWord(verb):
                    # 如果target_word是entity，就不添加,并且将动词插入到第一位
                    if target_word_index not in self.instances:
                        self.sequence.append(position)
                        if target_word_index not in self.entities \
                                and target_word_index not in self.sequence \
                                and not self.model.isSkipWordsIndex(target_word_index) \
                                and not isVerbContainedSkipHEDwords(verb) \
                                and not degreeWord(self.model.vertexModel.indexForWord(target_word_index)):
                            self.sequence.append(target_word_index)
                    elif not isVerbContainedSkipHEDwords(verb):
                        self.sequence.insert(0, position)

                    # print("self.sequence", self.sequence)
                else:
                    # print(self.instances)
                    # 是HED动词
                    # 如果是HED词，修饰的target不是vob修饰词，如哪些，什么之类的就添加
                    for modi_index in modified_word_index:
                        modi_word = self.model.vertexModel.indexForWord(modi_index)
                        # 条件，如果修饰动词的词不是疑问词或者不是实体词，就添加进去
                        if modi_index not in self.entities \
                                and not self.model.isSkipWordsIndex(modi_index) \
                                and modi_index not in self.sequence \
                                and modi_index not in self.instances:
                            # iscontainValue = True情况，并且modi_word = sbv
                            # print(modi_index)
                            if self.instances:
                                for instance in self.instances:
                                    instance_type = lexicon.getInstanceType(
                                        self.model.vertexModel.indexForWord(instance))
                                    if not instance_type == modi_word:
                                        self.sequence.append(modi_index)

                    # 如果中心词不是有，是，这种词，就添加
                    if not isVerbContainedSkipHEDwords(verb):
                        self.sequence.append(position)
            # print("sequence>>>>>>>", self.sequence)
            # FIXME:有可能出现的情况，还有名词修饰名词的时候，必须把名词遍历统计完
            for noun in self.nouns:
                noun, position = wordAndIndex(noun)
                noun_target_index = self.model.vertexModel.wordForTargetIndex(position)
                # print("target word", noun_target_index)
                if position not in self.sequence \
                        and position not in self.entities \
                        and position not in self.instances:
                    # 如果是目标的sbv就插入目标词之前
                    if self.model.vertexModel.wordForDeprel(noun) == "SBV" \
                            and noun_target_index in self.sequence:
                        self.sequence.insert(self.sequence.index(noun_target_index), position)
                    # 如果是目标的VOB就插到目标词后面
                    elif self.model.vertexModel.wordForDeprel(noun) == "VOB" \
                            and noun_target_index in self.sequence:
                        self.sequence.insert(self.sequence.index(noun_target_index) + 1, position)
                    # 如果啥都不是就直接拼接
                    else:
                        if position not in self.sequence:
                            if noun_target_index in self.instances \
                                    and self.model.indexOfTimeWord(position) \
                                    and not self.model.indexOfTimeWord(position):
                                self.sequence.insert(0, position)
                            else:
                                # 插入到修饰词前面 / 如果不是时间词(时间词放最后)
                                if not self.model.indexOfTimeWord(position) \
                                        and noun_target_index in self.sequence:
                                    self.sequence.insert(self.sequence.index(noun_target_index), position)
                                else:
                                    self.sequence.append(position)
        else:
            # 有属性值的情况
            # 遍历动词
            for verb in self.verbs:
                verb, position = wordAndIndex(verb)
                # 目标词序号
                target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                # 被修饰词序号
                modified_word_index = self.model.vertexModel.modifiedWordIndex(position)
                # 被修饰词的deprel
                target_word_deprel = self.model.vertexModel.indexForDeprel(target_word_index)

                # print(degreeWord(verb))
                # 判断是不是程度词，比如有大于，等于，为之类的
                if degreeWord(verb):
                    # print("position>>>>", position, target_word_index)
                    # step 1 找出targetword并且添加到sequence
                    if target_word_index \
                            and not self.model.isSkipWordsIndex(target_word_index) \
                            and not isVerbContainedSkipHEDwords(verb):
                        # 如果这个target_word是HED，SBV或者Att并且在entities中
                        if self.makeEntityWord(target_word_deprel, target_word_index):
                            self.dealWithEntities(target_word_index)
                        else:
                            self.sequence.append(target_word_index)

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
                            if not self.model.isSkipWordsIndex(position):
                                self.sequence.append(index)
                else:
                    # 不是程度词则组合
                    # 如果是中心词
                    # print("word is",verb)
                    if self.model.isHedWord(verb):
                        # print("position>>>>", position, target_word_index,verb)
                        if not isVerbContainedSkipHEDwords(verb):
                            self.sequence.append(position)
                            self.sequence.append(target_word_index)
                    else:
                        if not isVerbContainedSkipHEDwords(verb):
                            self.sequence.append(position)

            # print(self.sequence)
            # # 补充名词
            # for noun in self.nouns:
            #     noun, position = wordAndIndex(noun)
            #     noun_deprel = self.model.vertexModel.wordForDeprel(noun)
            #     # print(lexicon.isEntityWords(noun))
            #     if position not in self.sequence \
            #             and position not in self.entities \
            #             and position not in self.instances:
            #
            #         if self.makeEntityWord(noun_deprel, word=noun):
            #             self.dealWithEntities(position)
            #         else:
            #             if not self.model.isSkipWordsIndex(position):
            #                 # 有一种情况是实体词和形容词分离（服务类有超过一千万的项目吗）
            #                 # 做一个拼接然后判断拼接了的词是否在实体词中，如果在就保存，如果不在就放弃直接添加
            #                 if position not in self.sequence \
            #                         and position not in self.entities:
            #                     self.sequence.append(position)

        self.dealWithEnd()
        return self.final_action_dict

    # 如果只有宾
    # 第⑤种情况
    def has_VOB_HED_Words(self):
        pass

    # 如果有状语，介宾和动宾
    # 第⑥种情况
    def has_ADV_SBV_VOB_HED_Words(self):
        # 2020年远光软件股份有限公司投标的项目
        # 施工标的类项目都有哪些公司中标？
        # 遍历动词
        if self.count:
            pass
            for attribute_word in self.adjs:
                adj, position = wordAndIndex(attribute_word)
                # print(position)
                attribute_word = self.model.vertexModel.indexForWord(position)
                modi_word_index = self.model.vertexModel.modifiedWordIndex(position)
                if countWord(attribute_word):
                    for modi_index in modi_word_index:
                        if modi_index not in self.entities and modi_index not in self.instances:
                            self.sequence.append(modi_index)

        else:
            for verb in self.verbs:
                verb, position = wordAndIndex(verb)
                # print("test in ")
                modified_word_index = self.model.vertexModel.modifiedWordIndex(position)
                verb_target_index = self.model.vertexModel.wordForTargetIndex(position)

                # 有时间状语的句子 ，因为时间一般self.containValue = true的情况
                if self.containValue:
                    for modi_index in modified_word_index:
                        modi_pos = self.model.vertexModel.indexForPos(modi_index)
                        modi_deprel = self.model.vertexModel.indexForDeprel(modi_index)

                        if modi_pos == "n" and (modi_deprel == "SBV" or modi_deprel == "VOB"):
                            print("modi_pos", modi_index)
                            self.dealWithEntities(modi_index)
                        else:
                            self.sequence.append(modi_index)
                # 处理动词
                if not self.model.isHedIndex(position):
                    if self.entities:
                        for entity in self.entities:
                            entity_target_word_index = self.model.vertexModel.wordForTargetIndex(entity)
                            # print("entity target")
                            if entity_target_word_index == verb_target_index:
                                self.entities.append(position)

                    self.sequence.append(position)

            # 找到序列中有没有词跟entity有关系
            temp = 0
            if self.containValue:
                for index in self.sequence:
                    target_word_index = self.model.vertexModel.wordForTargetIndex(index)
                    for entity_index in self.entities:
                        entity_target_word_index = self.model.vertexModel.wordForTargetIndex(entity_index)
                        if target_word_index == entity_target_word_index:
                            temp = index
                # print("temp===",temp)
                self.sequence.insert(0, temp)
                # print(self.sequence)

        self.dealWithEnd()
        return self.final_action_dict

    # 只有状中，介宾，
    # 第⑦种情况
    def has_HED_ADV_SBV_VOB_POB_Words(self):
        # FIXME： 主谓宾状介，
        #   eg:与远光软件股份有限公司签订合同的企业有哪些
        # 遍历动词
        for verb in self.verbs:
            verb, position = wordAndIndex(verb)
            modified_word_index = self.model.vertexModel.modifiedWordIndex(position)

            if not isVerbContainedSkipHEDwords(verb):
                self.sequence.append(position)

            for modi_index in modified_word_index:
                modi_word = self.model.vertexModel.indexForWord(modi_index)
                if modi_index not in self.sequence \
                        and modi_index not in self.entities \
                        and not self.model.isSkipWordsIndex(modi_index) \
                        and not isVerbContainedSkipHEDwords(modi_word):
                    self.sequence.append(modi_index)

        # 处理属性词
        # 合同总价和招标总价相同的项目
        if self.attribute:
            for attribute_word in self.attribute:
                attribute_word, position = wordAndIndex(attribute_word)
                target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                target_word_pos = self.model.vertexModel.wordForPos(
                    self.model.vertexModel.indexForWord(target_word_index))
                # print(target_word_pos)
                # 法人与联系人相同的企业
                if target_word_pos == "c" or target_word_pos == "p":
                    target_word_index = self.model.vertexModel.wordForTargetIndex(target_word_index)
                else:
                    self.sequence.append(target_word_index)
                self.sequence.insert(self.sequence.index(target_word_index), position)

        # 处理名词
        for noun in self.nouns:
            noun, position = wordAndIndex(noun)
            noun_deprel = self.model.vertexModel.wordForDeprel(noun)
            if self.makeEntityWord(noun_deprel, word=noun):
                self.dealWithEntities(position)

        # 处理形容词
        for adj in self.adjs:
            adj, position = wordAndIndex(adj)
            modified_word_index = self.model.vertexModel.modifiedWordIndex(position)
            # 如果形容词是HED - （那家招标代理机构招标次数最多？）一般句尾是形容词
            if self.model.isHedIndex(position):
                for modi_index in modified_word_index:
                    modi_word = self.model.vertexModel.indexForWord(modi_index)
                    if modi_index not in self.sequence and not countWord(modi_word):
                        self.sequence.append(modi_index)
                self.sequence.append(position)
            else:
                self.sequence.append(position)

        self.dealWithEnd()
        return self.final_action_dict

    # 并列关系
    # 第⑧种情况
    def has_COO_HED(self):
        for verb in self.verbs:
            verb, position = wordAndIndex(verb)
            target_word_index = self.model.vertexModel.wordForTargetIndex(position)
            if not isVerbContainedSkipHEDwords(verb):
                self.sequence.append(position)
            if target_word_index not in self.entities:
                self.sequence.append(target_word_index)

        # 处理剩下的名词
        for noun in self.nouns:
            noun, position = wordAndIndex(noun)
            if position not in self.sequence:
                self.sequence.append(position)

        # 如果有属性的情况
        for attribute in self.attribute:
            attribute, position = wordAndIndex(attribute)
            if position not in self.sequence:
                self.sequence.append(position)

        self.dealWithEnd()
        return self.final_action_dict

    # 并列主谓宾
    # 第⑨种情况
    def has_COO_HED_SBV_VOB(self):
        for verb in self.verbs:
            verb, position = wordAndIndex(verb)
            target_word_index = self.model.vertexModel.wordForTargetIndex(position)
            target_word = self.model.vertexModel.indexForWord(target_word_index)
            modified_word_index = self.model.vertexModel.modifiedWordIndex(position)

            if not self.model.isHedIndex(position):
                if not isVerbContainedSkipHEDwords(verb):
                    self.sequence.append(position)
                if target_word_index not in self.entities and not countWord(target_word):
                    # print(target_word)
                    self.sequence.append(target_word_index)
            else:
                for modified_index in modified_word_index:

                    if modified_index not in self.sequence:
                        self.sequence.append(modified_index)
                    if position not in self.sequence and not isVerbContainedSkipHEDwords(verb):
                        self.sequence.append(position)

        # print(self.sequence)
        # # 如果有属性
        # for attribute_word in self.attribute:
        #     attribute, position = wordAndIndex(attribute_word)
        #     target_word_index = self.model.vertexModel.wordForTargetIndex(position)
        #
        #     if target_word_index not in self.sequence:
        #         self.sequence.append(position)
        #         self.sequence.append(target_word_index)
        #     else:
        #         self.sequence.insert(self.sequence.index(target_word_index) + 1, position)
        #
        # # 处理名词
        # for noun in self.nouns:
        #     noun, position = wordAndIndex(noun)
        #     target_word_index = self.model.vertexModel.wordForTargetIndex(position)
        #     if target_word_index and target_word_index in self.sequence:
        #         self.sequence.insert(self.sequence.index(target_word_index), position)
        #     elif self.model.isHedIndex(position) and not isVerbContainedSkipHEDwords(position):
        #         self.sequence.append(position)

        self.dealWithEnd()
        return self.final_action_dict

    # 有子句模式
    # 第⑩种情况
    def has_SBV_HED_VOB_IC(self):

        # 2020年公司投标有哪些项目
        for verb in self.verbs:
            verb, position = wordAndIndex(verb)
            modified_words_index = self.model.vertexModel.modifiedWordIndex(position)

            for modi_index in modified_words_index:
                modi_word = self.model.vertexModel.indexForWord(modi_index)
                if self.model.indexOfTimeWord(modi_index):
                    self.sequence.insert(len(self.sequence) - 1, modi_index)
                else:
                    if modi_index not in self.sequence \
                            and not isVerbContainedSkipHEDwords(modi_word):
                        self.sequence.append(modi_index)

            if not isVerbContainedSkipHEDwords(verb):
                self.sequence.append(position)

        self.dealWithEnd()
        return self.final_action_dict

    # 并列结构
    # 第⑪种情况
    def has_COO_SBV_HED_ADV_VOB(self):

        # 没有属性词的情况
        if not self.attribute:
            for verb in self.verbs:
                verb, position = wordAndIndex(verb)
                modified_word_index = self.model.vertexModel.modifiedWordIndex(position)
                for modi_index in modified_word_index:
                    modi_word = self.model.vertexModel.indexForWord(modi_index)
                    if not isVerbContainedSkipHEDwords(modi_word) \
                            and not self.model.isSkipWordsIndex(modi_index):
                        self.sequence.append(modi_index)
                        if position not in self.sequence:
                            self.sequence.append(position)

            # 处理剩下的名词
            for noun in self.nouns:
                noun, position = wordAndIndex(noun)
                target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                if position not in self.sequence:
                    if target_word_index in self.sequence and not self.model.isHedIndex(position):
                        self.sequence.insert(self.sequence.index(target_word_index) + 1, position)
                    else:
                        self.sequence.append(position)

        else:
            # 遍历属性词
            for attirbute in self.attribute:
                attirbute_word, position = wordAndIndex(attirbute)
                self.sequence.append(position)

            # 遍历动词
            for verb in self.verbs:
                verb, position = wordAndIndex(verb)
                modified_word_index = self.model.vertexModel.modifiedWordIndex(position)
                for modi_index in modified_word_index:
                    modi_word = self.model.vertexModel.indexForWord(modi_index)
                    if not isVerbContainedSkipHEDwords(modi_word) \
                            and not self.model.isSkipWordsIndex(modi_index):
                        self.sequence.append(modi_index)
                        if position not in self.sequence:
                            self.sequence.append(position)

            # 处理剩下的名词
            for noun in self.nouns:
                noun, position = wordAndIndex(noun)
                target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                if position not in self.sequence:
                    if target_word_index in self.sequence and not self.model.isHedIndex(position):
                        self.sequence.insert(self.sequence.index(target_word_index) + 1, position)
                    else:
                        self.sequence.append(position)

        self.dealWithEnd()
        return self.final_action_dict

    # 查找句子中的实例
    def findInstanceWords(self):
        nouns = self.model.nouns
        coos = self.model.coos
        instances, instances_type = lexicon.receiveInstanceInfo()
        entity_list = []

        for noun in nouns:
            noun = noun.split("-")[0]
            if noun in instances:
                entity_list.append(noun)

        if not len(entity_list):
            for coo in coos:
                coo = coo.split("-")[0]
                if coo in instances:
                    entity_list.append(coo)

        print("1.搜索实例词>>>>>>>", entity_list)
        return entity_list

    # 是否含有属性值
    def hasValues(self, charge):
        self.final_action_dict["values"] = charge

    # 处理实体
    def dealWithEntities(self, entity):
        if entity not in self.entities:
            self.entities.append(entity)

    # 处理剩下的的名词
    def dealWithNouns(self):

        # print("self.entities",self.entities)
        # print("self.instance",self.instances)
        # print("self sequence",self.sequence)

        # 补充名词
        for noun in self.nouns:
            noun, position = wordAndIndex(noun)
            noun_deprel = self.model.vertexModel.wordForDeprel(noun)
            # print(lexicon.isEntityWords(noun))
            if position not in self.sequence \
                    and position not in self.entities \
                    and position not in self.instances:
                # print("来这里没有")
                # print(self.containValue)
                if self.makeEntityWord(noun_deprel, word=noun) and self.containValue:
                    # print(noun)
                    self.dealWithEntities(position)
                else:
                    if not self.model.isSkipWordsIndex(position):
                        # 有一种情况是实体词和形容词分离（服务类有超过一千万的项目吗）
                        # 做一个拼接然后判断拼接了的词是否在实体词中，如果在就保存，如果不在就放弃直接添加
                        if position not in self.sequence \
                                and position not in self.entities \
                                and not countWord(noun):
                            target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                            if target_word_index in self.sequence:
                                self.sequence.insert(self.sequence.index(target_word_index) + 1, position)
                            elif target_word_index in self.entities:
                                self.entities.append(target_word_index)
                            else:
                                self.sequence.append(position)

        # 去年那种类型项目投资最多
        # 如果sequence中有名词在entities中，说明可能是修饰作用，例如，项目-类型
        for word_index in self.sequence:
            target_word_index = self.model.vertexModel.wordForTargetIndex(word_index)
            if target_word_index in self.entities:
                self.entities.insert(self.entities.index(target_word_index) + 1, word_index)
                self.sequence.remove(word_index)

    # 处理实体词
    def makeEntityWord(self, word_deprel, word_index=0, word=""):
        if word_deprel == "SBV" or word_deprel == "ATT" or word_deprel == "HED" or word_deprel == "COO":
            # print("12312312312")
            if word_index:
                if lexicon.isEntityWords(self.model.vertexModel.indexForWord(word_index)):
                    return True
            else:
                # print("12312312311312312312321")
                # print(word)
                if lexicon.isEntityWords(word):
                    return True
        return False

    # FIXME: eg:2020年合同总价为100万的项目的投标人是谁
    #      eg: 中标日期为2020年并且合同总价为100万的项目是
    #       eg:2020年合同总价为100万的项目    中标日期2020年的项目
    def isAttributeSequence(self):
        entities = self.final_action_dict["entities"]
        instances = self.final_action_dict["instances"]
        # 首先判断居中是否有时间或者金额
        if self.model.isContainAmountOrTime():
            r_list = self.model.findAmountOrTimeWordIndex()
            # print("time or amount list", self.model.findAmountOrTimeWordIndex())

            # print("self sequences>>>>>>", instances)
            # 找到对应的修饰词
            for index in r_list:
                temp_list = []
                target_word_index = self.model.vertexModel.wordForTargetIndex(index)
                target_word = self.model.vertexModel.indexForWord(target_word_index)
                # 找到modified_word
                modi_word_index = self.model.vertexModel.modifiedWordIndex(target_word_index)
                # print("modi_index",modi_word_index,target_word_index)

                # 如果有时间的状态
                if self.model.indexOfTimeWord(index):
                    # print("有时间的index>>>>",index)
                    # 有时间的情况
                    # 中标日期是2020年的项目有哪些
                    # 2020年公司投标有哪些项目
                    time_index_list = self.model.findTimeIndex()
                    for time in time_index_list:
                        # 判断word_list中有没有带日期的字段
                        time_word_index = self.model.findTimeWordIndexFromWordList()
                        if time_word_index != "":
                            time_word_target_index = self.model.vertexModel.wordForTargetIndex(
                                time_word_index)
                            time_word_target_word = self.model.vertexModel.indexForWord(time_word_target_index)
                            if time_word_index not in temp_list:
                                temp_list.append(time_word_index)
                                if degreeWord(time_word_target_word):
                                    temp_list.append(time_word_target_index)
                            if time not in temp_list:
                                temp_list.append(time)
                        else:
                            if time not in temp_list:
                                temp_list.append(time)
                else:
                    # 如果是没有时间的状态
                    # print("没有时间的index>>>>",index,modi_word_index)
                    if modi_word_index:
                        for modi_index in modi_word_index:
                            modi_word = self.model.vertexModel.indexForWord(modi_index)
                            if not isVerbContainedSkipHEDwords(self.model.vertexModel.indexForWord(modi_index)):
                                # 有time和么有time区分处理
                                if not self.model.indexOfTimeWord(modi_index):
                                    # print(modi_index)
                                    if degreeWord(modi_word) \
                                            or lexicon.isAttributeWords(modi_word) \
                                            or self.model.isValueWord(modi_word):
                                        temp_list.append(modi_index)
                                    if target_word_index not in temp_list \
                                            and target_word_index not in entities \
                                            and target_word_index not in instances \
                                            and not isVerbContainedSkipHEDwords(target_word):
                                        # FIXME: 如果实例的对象词不等于目标词，就加入
                                        #   eg: 2020年远光软件股份有限公司投标的项目
                                        #  2020年招标金额为100万的是 ※
                                        if instances:
                                            for instance in instances:
                                                if self.model.vertexModel.wordForTargetIndex(
                                                        instance) != target_word_index \
                                                        and not degreeWord(target_word):
                                                    temp_list.append(target_word_index)
                                        else:
                                            if not degreeWord(target_word):
                                                temp_list.append(target_word_index)

                self.final_action_dict["attributes"].append(temp_list)

    # 清理疑问词
    def clearQuestionWord(self):
        for index in self.sequence:
            # print(index)
            word = self.model.vertexModel.indexForWord(index)
            # print(word)
            if isQuestionWord(word):
                self.sequence.remove(index)

    # 清除重复的词
    def clearRepeatWord(self):
        # for x in self.sequence:
        #     while self.sequence.count(x) > 1:
        #         del self.sequence[self.sequence.index(x)]
        data = self.sequence
        new_data = []
        for i in range(len(data)):
            if data[i] not in new_data:
                new_data.append(data[i])
        # print(new_data)
        self.sequence = new_data

    # 清理sequence中与attribute中重复的词
    def clearSequenceRepeatWord(self):
        temp_all_attribute_word = []
        for atri in self.attributes:
            for word in atri:
                temp_all_attribute_word.append(word)

        # 遍历sequence
        temp_record_index = []
        for index, word in enumerate(self.sequence):
            if word in self.entities or word in temp_all_attribute_word or word in self.instances:
                temp_record_index.append(index)

        # print(temp_record_index)
        # print("self.sequence",self.sequence[::-1])
        # sequence 删除
        for index in temp_record_index[::-1]:
            del self.sequence[index]

    # 处理结尾
    def dealWithEnd(self):
        print("self entities", self.entities)
        # 清除重复词
        self.clearRepeatWord()
        # 清理疑问词
        self.clearQuestionWord()
        # 处理剩下的名词
        self.dealWithNouns()
        # 清理sequence中包含的多余词
        self.clearSequenceRepeatWord()
        # 将sequences赋值给最终字典
        self.final_action_dict["sequences"] = self.sequence


# 分解word和index
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
