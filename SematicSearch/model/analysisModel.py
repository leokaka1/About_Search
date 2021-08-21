from SematicSearch.model.sematicModel import SemanticModel
from SematicSearch.utils import *

"""
词性语义分析模型
"""


class SematicAnalysisModel:
    def __init__(self, vertexModel: SemanticModel, nouns, coos, verbs, adjs, attribute):
        self.vertexModel = vertexModel
        self.nouns = nouns
        self.coos = coos
        self.verbs = verbs
        self.adjs = adjs
        self.attribute = attribute

        self.nounsHasWords = True if len(nouns) > 0 else False
        self.coosHasWords = True if len(coos) > 0 else False
        self.verbsHasWords = True if len(verbs) > 0 else False
        self.adjsHasWords = True if len(adjs) > 0 else False
        self.attributeHasWords = True if len(attribute) > 0 else False

    # 分析名词数组中最后一个词的词性
    def analysisNounsLastWord(self):
        if self.nounsHasWords:
            last_noun_word = self.nouns[-1].split("-")[0]
            last_noun_deprel = self.vertexModel.wordForDeprel(last_noun_word)
            return last_noun_deprel

    # 分析动词数组中最后一个词的词性
    def analysisVerbsLastWord(self):
        if self.verbsHasWords:
            last_verb_word = self.verbs[-1].split("-")[0]
            last_verb_deprel = self.vertexModel.wordForDeprel(last_verb_word)
            # print("lastNoun的词性", last_verb_deprel)
            return last_verb_deprel

    # 最后一个名词是HED
    def isLastNounObject(self):
        if self.analysisNounsLastWord() == "HED":
            return True
        else:
            return False

    # 最后一个动词是HED
    def isLastVerbObject(self):
        if self.analysisVerbsLastWord() == "HED":
            return True
        else:
            return False

    # 最后一个名词或者动词是HED
    def isLastNounAndVerbObject(self):
        if self.isLastNounObject() or self.isLastVerbObject():
            return True
        else:
            return False

    # 本词是否是HED
    def isHedWord(self, word):
        deprel = self.vertexModel.wordForDeprel(word)
        if deprel == "HED":
            return True
        else:
            return False

    def isHedIndex(self, index):
        deprel = self.vertexModel.deprel_list[index]
        if deprel == "HED":
            return True
        else:
            return False

    # 判断一个词组里面有没有HED词
    def islistContainHEDword(self, wordlist):
        for word in wordlist:
            if self.isHedWord(word):
                return True
        return False

    # 是否是SBV word
    def getSentenceSBVwords(self):
        sbv_words = []
        for index, deprel in enumerate(self.vertexModel.deprel_list):
            if deprel == "SBV":
                word = self.vertexModel.word_list[index]
                sbv_words.append(word)

        return sbv_words

    # 是否是属性值词
    def isValueWord(self, word):
        if word in self.vertexModel.word_list:
            posWord = self.vertexModel.wordForPos(word)
            if posWord == "TIME" or posWord == "m" or posWord == "PER":
                return True
            else:
                return False

    # 是否是虚词，可以过滤
    def isSkipWord(self, word):
        posWord = self.vertexModel.wordForPos(word)
        if posWord == "MT":
            return True
        else:
            return False

    # 判断是否
    def isSkipWordsIndex(self, index):
        if self.vertexModel.pos_list[index] == "xc" \
                or self.vertexModel.pos_list[index] == "u":
            return True
        return False

    # 是否是时间词
    def indexOfTimeWord(self, index):
        pos = self.vertexModel.pos_list[index]
        word = self.vertexModel.word_list[index]
        if pos == "TIME" or word == "今年" or word == "去年" or word == "明年" or word == "前年":
            return True
        else:
            return False

    # 获取动词的SBV主语
    def getverbSBV(self, verb):
        temp_list = []
        # verb_id = self.vertexModel.wordForId(verb)
        for word in self.vertexModel.word_list:
            if self.vertexModel.wordForTargetWord(word) == verb:
                if self.vertexModel.wordForDeprel(word) == "SBV":
                    temp_list.append(word)
        return temp_list

    # 获取句子中的HED词
    def getHEDWord(self):
        for index, deprel in enumerate(self.vertexModel.deprel_list):
            if deprel == "HED":
                return self.vertexModel.word_list[index], index
        return "", 0

    def getVOBWord(self):
        vob_list = []
        for index, deprel in enumerate(self.vertexModel.deprel_list):
            if deprel == "VOB":
                vob_list.append(self.vertexModel.word_list[index])
        return vob_list

    # 判断传入的deprel是否是在句子中
    def sentenceContainWhichDeqrel(self, deprels):
        flag = 0
        sentence_deprel_list = self.vertexModel.deprel_list.copy()
        # 先去掉ATT修饰词,因为先要保留主干，避免定中关系影响成分
        for deprel in sentence_deprel_list[::-1]:
            if deprel == "ATT" or deprel == "MT":
                sentence_deprel_list.remove(deprel)

        for i in deprels:
            if i in sentence_deprel_list:
                flag += 1

        if flag == len(set(sentence_deprel_list)):
            return True

        return False

    # FIXME: 这里是判断句子中有没有包含一些类别的词
    def sentenceSematicSituations(self):
        # 只有主语中心词 eg：2020年（ATT）招标文件（HED)
        if self.sentenceContainWhichDeqrel(["HED"]):
            return 1
        # 有主谓宾完整 eg:哪些单位(SBV)有(HED)投标 基于NLP的商务数据清洗项目(VOB)
        elif self.sentenceContainWhichDeqrel(["HED", "SBV"]):
            return 2
        elif self.sentenceContainWhichDeqrel(["HED", "VOB"]):
            return 3
        # 有动HED和动词的SBV主语
        elif self.sentenceContainWhichDeqrel(["HED", "SBV", "VOB"]):
            return 4
        # 有状语和中心语 eg:2020年 (时间状语)招标那些类型的 项目(HED)主语
        elif self.sentenceContainWhichDeqrel(["ADV", "HED"]):
            return 5
        # 状语，主,谓，宾 eg:2020年(ADV)远光股份有限公司(SBV)有(HED)投标服务类项目(VOB)吗
        elif self.sentenceContainWhichDeqrel(["ADV", "SBV", "HED", "VOB"]):
            return 6
        # 状，介宾，主，谓，宾 eg:与(ADV)远光软件股份有限公司(POB)签订合同(VOB)的企业(SBV)有哪些
        elif self.sentenceContainWhichDeqrel(["ADV", "POB", "VOB", "SBV", "HED"]):
            return 7
        elif self.sentenceContainWhichDeqrel(["COO", "HED"]):
            return 8
        elif self.sentenceContainWhichDeqrel(["COO", "HED", "SBV", "VOB"]):
            return 9
