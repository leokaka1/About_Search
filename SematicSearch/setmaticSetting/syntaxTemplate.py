from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils import *

lexicon = Lexicon()


class Template:
    def __init__(self, model: SematicAnalysisModel):
        self.model = model
        self.final_action_dict = {"instances": [], "entities": [], "sequences": [], "count": False,
                                  "isContainValue": False}
        self.sequence = []
        self.degrees = ""
        self.values_str = ""
        self.nouns = self.model.nouns
        self.verbs = self.model.verbs
        self.adjs = self.model.adjs
        self.coos = self.model.coos
        self.attribute = self.model.attribute
        self.head_list = self.model.vertexModel.head_list
        self.word_list = self.model.vertexModel.word_list

        # 把找出来的实例给终极字典
        self.entities = self.findEntityWords()
        for entities in self.entities:
            index = self.model.vertexModel.word_list.index(entities)
            self.final_action_dict["instances"].append(index)
        self.entities = self.final_action_dict["entities"]
        self.instances = self.final_action_dict["instances"]

        # # 是否有次数,count
        for word in self.model.vertexModel.word_list:
            if countWord(word):
                self.final_action_dict["count"] = True

        # 判断句子中是否含有属性词，如果含有就把isContainValue置为True
        for word in self.model.vertexModel.word_list:
            # 如果一句话里面含有属性词或者含有一些金额，日期等词，就判断包含属性
            if lexicon.isContainAtrributeWord(word) or self.model.isValueWord(word):
                self.final_action_dict["isContainValue"] = True

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
            hed_word, hed_index = self.model.getHEDWord()
            if hed_index and hed_index not in self.sequence:
                self.sequence.append(hed_index)

        # 处理剩余的名词(如果词不在序列中并且不是问句词就添加)
        for noun in self.nouns:
            noun, position = wordAndIndex(noun)
            # targetWord_index = self.model.vertexModel.wordForTargetIndex(position)
            if position not in self.sequence \
                    and not isQuestionWord(noun) \
                    and position not in self.entities:
                self.sequence.append(position)

        self.dealWithEnd(self.sequence)
        return self.final_action_dict

    # 如果只有主语和中心词
    # 第②种情况
    def has_SBV_HED_Words(self):
        # FIXME: situation 2.1：有ATT，SBV和HED
        #   eg:中标最多的单位？ - 刘德华老婆出生于
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
                        self.sequence.append(position)

                    # print(self.sequence)

            # 处理剩余名词
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
            # 遍历动词
            for verb in self.verbs:
                verb, position = wordAndIndex(verb)
                target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                target_word = self.model.vertexModel.wordForTargetIndexWord(position)
                if position not in self.sequence:
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
                # target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                if position not in self.sequence \
                        and position not in self.entities \
                        and not countWord(noun):
                    self.sequence.append(position)

            # 处理剩下的属性词
            if self.attribute:
                for attribute in self.attribute:
                    attribute_word, position = wordAndIndex(attribute)
                    target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                    if position not in self.sequence \
                            and target_word_index in self.sequence:
                        self.sequence.insert(self.sequence.index(target_word_index), position)

        self.dealWithEnd(self.sequence)
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
        self.dealWithEnd(self.sequence)
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
                target_word_index = self.model.vertexModel.wordForTargetIndex(position)
                # print(target_word_index)
                # step 1.1 判断是否是HED动词
                # 不是HED动词
                if not self.model.isHedWord(verb):
                    # 如果target_word是entity，就不添加,并且将动词插入到第一位
                    if target_word_index not in self.entities:
                        self.sequence.append(position)
                        if target_word_index not in self.instances \
                                and target_word_index not in self.sequence \
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
                                and modi_index not in self.sequence \
                                and modi_index not in self.instances:
                            # iscontainValue = True情况，并且modi_word = sbv
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
                    if self.model.vertexModel.wordForDeprel(noun) == "SBV":
                        self.sequence.insert(self.sequence.index(noun_target_index), position)
                    # 如果是目标的VOB就插到目标词后面
                    elif self.model.vertexModel.wordForDeprel(noun) == "VOB":
                        self.sequence.insert(self.sequence.index(noun_target_index) + 1, position)
                    # 如果啥都不是就直接拼接
                    else:
                        if position not in self.sequence:
                            if noun_target_index in self.entities \
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

                # 判断是不是程度词，比如有大于，等于，为之类的
                if degreeWord(verb):
                    # print("position>>>>", position, target_word)
                    # step 1 找出targetword并且添加到sequence
                    if target_word_index \
                            and not self.model.isSkipWordsIndex(target_word_index) \
                            and not isVerbContainedSkipHEDwords(verb):
                        # 如果这个target_word是HED，SBV或者Att并且在entities中
                        if target_word_deprel == "SBV" or target_word_deprel == "ATT" or target_word_deprel == "HED":
                            if lexicon.isEntityWords(self.model.vertexModel.indexForWord(target_word_index)):
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
                            self.sequence.append(index)
                else:
                    # 不是程度词则组合
                    # 如果是中心词
                    if self.model.isHedWord(verb):
                        # print("position>>>>", position, target_word,verb)
                        if not isVerbContainedSkipHEDwords(verb):
                            self.sequence.append(position)
                            self.sequence.append(target_word_index)

            # 补充名词
            for noun in self.nouns:
                noun, position = wordAndIndex(noun)
                word_pos = self.model.vertexModel.wordForDeprel(noun)
                # print(lexicon.isEntityWords(noun))
                if position not in self.sequence \
                        and position not in self.entities \
                        and position not in self.instances:
                    if word_pos == "SBV" or word_pos == "ATT" or word_pos == "HED":
                        if lexicon.isEntityWords(noun):
                            self.dealWithEntities(position)

        self.dealWithEnd(self.sequence)
        return self.final_action_dict

    # 如果只有宾
    # 第⑤种情况
    def has_VOB_HED_Words(self):
        pass

    # 如果有状语，介宾和动宾
    # 第⑥种情况
    def has_ADV_SBV_VOB_HED_Words(self):
        # 遍历动词
        for verb in self.verbs:
            verb, position = wordAndIndex(verb)
            modified_word_index = self.model.vertexModel.modifiedWordIndex(position)
            if not self.model.isHedIndex(position) and not isVerbContainedSkipHEDwords(verb):
                self.sequence.append(position)

                for modi_index in modified_word_index:
                    if modi_index not in self.sequence and modi_index not in self.entities:
                        self.sequence.append(modi_index)

        # 处理剩下的名词
        for noun in self.nouns:
            noun, position = wordAndIndex(noun)
            if not isSkipNounWord(noun) \
                    and position not in self.sequence \
                    and position not in self.entities:
                if not self.model.indexOfTimeWord(position):
                    self.sequence.append(position)

        # 处理时间
        for noun in self.nouns:
            noun, position = wordAndIndex(noun)
            if self.model.indexOfTimeWord(position):
                self.sequence.append(position)

        self.dealWithEnd(self.sequence)
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
            if position not in self.sequence and position not in self.entities:
                self.sequence.append(position)

        self.dealWithEnd(self.sequence)
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

        self.dealWithEnd(self.sequence)
        return self.final_action_dict

    # 并列主谓宾
    # 第⑨种情况
    def has_COO_HED_SBV_VOB(self):
        for verb in self.verbs:
            verb, position = wordAndIndex(verb)
            target_word_index = self.model.vertexModel.wordForTargetIndex(position)
            modified_word_index = self.model.vertexModel.modifiedWordIndex(position)
            if not self.model.isHedIndex(position):
                if not isVerbContainedSkipHEDwords(verb):
                    self.sequence.append(position)
                if target_word_index not in self.entities:
                    self.sequence.append(target_word_index)
            else:
                for modified_index in modified_word_index:
                    if modified_index not in self.sequence:
                        self.sequence.append(modified_index)
                    if position not in self.sequence and not isVerbContainedSkipHEDwords(verb):
                        self.sequence.append(position)
        # 如果有属性
        for attribute_word in self.attribute:
            attribute, position = wordAndIndex(attribute_word)
            target_word_index = self.model.vertexModel.wordForTargetIndex(position)

            if target_word_index not in self.sequence:
                self.sequence.append(position)
                self.sequence.append(target_word_index)
            else:
                self.sequence.insert(self.sequence.index(target_word_index) + 1, position)

        # 处理名词
        for noun in self.nouns:
            noun, position = wordAndIndex(noun)
            target_word_index = self.model.vertexModel.wordForTargetIndex(position)
            if target_word_index and target_word_index in self.sequence:
                self.sequence.insert(self.sequence.index(target_word_index), position)
            elif self.model.isHedIndex(position) and not isVerbContainedSkipHEDwords(position):
                self.sequence.append(position)

        self.dealWithEnd(self.sequence)
        return self.final_action_dict

    # 有子句模式
    # 第⑩种情况
    def has_SBV_HED_VOB_IC(self):

        # 2020年公司投标有哪些项目
        for verb in self.verbs:
            verb, position = wordAndIndex(verb)
            modified_words_index = self.model.vertexModel.modifiedWordIndex(position)

            for modi_index in modified_words_index:
                if self.model.indexOfTimeWord(modi_index):
                    self.sequence.insert(len(self.sequence) - 1, modi_index)
                else:
                    if modi_index not in self.sequence:
                        self.sequence.append(modi_index)

            if not isVerbContainedSkipHEDwords(verb):
                self.sequence.append(position)

        self.dealWithEnd(self.sequence)
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

        self.dealWithEnd(self.sequence)
        return self.final_action_dict

    # 查找句子中的实例
    def findEntityWords(self):
        nouns = self.model.nouns
        coos = self.model.coos
        entities, entities_type = lexicon.receiveEntitiesInfo()
        entity_list = []

        for noun in nouns:
            noun = noun.split("-")[0]
            if noun in entities:
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
        for x in self.sequence:
            while self.sequence.count(x) > 1:
                del self.sequence[self.sequence.index(x)]

    def dealWithEnd(self, sequences):
        # 清除重复词
        self.clearRepeatWord()
        # 清理疑问词
        self.clearQuestionWord()
        # 将sequences赋值给最终字典
        self.final_action_dict["sequences"] = sequences

    def dealWithEntities(self, entity):
        self.final_action_dict["entities"].append(entity)


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
