from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils import *

lexicon = Lexicon()


class Template:
    def __init__(self, model: SematicAnalysisModel):
        self.model = model
        self.final_action_dict = {"entities": [], "sequences": [], "degree": []}

    # 如果只有ATT修饰HED
    # 远光软件股份有限公司投标项目的中标人
    def has_HED_Words(self):

        sequence = []
        nouns = self.model.nouns
        verbs = self.model.verbs
        adjs = self.model.adjs
        head_list = self.model.vertexModel.head_list
        word_list = self.model.vertexModel.word_list

        # 把找出来的实例给终极字典
        entities = self.findEntityWords()
        self.final_action_dict["entities"] = entities

        # 没有形容词修饰，比如有形容词修饰：最多-最少之类的
        if not adjs:
            # 有verb的时候
            if verbs:
                for index, verb in enumerate(verbs):
                    word, position = wordAndIndex(verb)
                    head = head_list[position]
                    target_word = word_list[head]
                    sequence.append(word)
                    sequence.append(target_word)

                # 判断HED在不在句子中，如果不在就添加到末尾
                hed = self.model.getHEDWord()
                if hed and hed not in sequence:
                    sequence.append(hed)
            else:
                for noun in nouns:
                    noun, position = wordAndIndex(noun)
                    sequence.append(noun)

            self.final_action_dict["sequences"] = sequence
        else:
            degrees = []
            # 如果形容词和动词都修饰HED，那么就把adj给v
            for word in adjs:
                word, _ = wordAndIndex(word)
                if degreeWord(word) and word not in degrees:
                    degrees.append(word)
            self.final_action_dict["degree"] = degrees
            # 如果有动词
            if verbs:
                # 再处理动词
                for word in verbs:
                    word, position = wordAndIndex(word)
                    head = head_list[position]
                    targetword = word_list[head]

                    if self.model.isHedWord(targetword):
                        sequence.append(targetword)
                        sequence.append(word)
                    else:
                        actionword = word + targetword
                        sequence.append(actionword)
            else:
                for noun in nouns:
                    noun, position = wordAndIndex(noun)
                    sequence.append(noun)
            self.final_action_dict["sequences"] = sequence

        print("final_sequence>>>>>>>", self.final_action_dict)

    # 如果有主谓宾三个
    def has_SBV_VOB_HED_Words(self):
        pass

    # 如果只有主
    def has_SBV_HED_Words(self):
        pass

    # 如果只有宾
    def has_VOB_HED_Words(self):
        pass

    # 如果有状语，介宾和动宾
    # 远光股份有限公司与中国水利电力物资集团有限公司有签订合同吗
    def has_ADV_POB_VOB_SBV_HED_Words(self):
        pass

    # 只有状中，介宾，
    # 与远光软件股份有限公司签订合同的企业
    def has_ADV_POB_VOB_HED_Words(self):
        pass

    # 只有一个实例的情况
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
