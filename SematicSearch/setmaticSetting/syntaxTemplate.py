from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils import *

lexicon = Lexicon()


class Template:
    def __init__(self, model: SematicAnalysisModel):
        self.model = model

    # 如果只有ATT修饰HED
    # 远光软件股份有限公司投标项目的中标人
    def has_HED_Words(self):
        final_sequence = []
        nouns = self.model.nouns
        verbs = self.model.verbs
        adjs = self.model.adjs
        head_list = self.model.vertexModel.head_list
        word_list = self.model.vertexModel.word_list

        entity = self.findEntityWords()
        print(adjs)
        print(entity)

        # 没有形容词修饰，比如有形容词修饰：最多-最少之类的
        if adjs:
            # 有verb的时候
            if verbs:
                for index, verb in enumerate(verbs):
                    word, position = wordAndIndex(verb)
                    head = head_list[position]
                    target_word = word_list[head]
                    final_sequence.append(word)
                    final_sequence.append(target_word)

                    # 判断HED在不在句子中，如果不在就添加到末尾
                    hed = self.model.getHEDWord()
                    if hed and hed not in final_sequence:
                        final_sequence.append(hed)
            else:
                for noun in nouns:
                    noun, position = wordAndIndex(noun)
                    final_sequence.append(noun)

        else:
            # 如果形容词和动词都修饰HED，那么就把adj给v
            pass

        print("final_sequence>>>>>>>", final_sequence)

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
        entity = ""

        for noun in nouns:
            noun = noun.split("-")[0]
            if noun in entities:
                word = lexicon.receiveEntitiesWordAndType(noun)
                entity = word

        print("1.搜索实例词>>>>>>>", entity)
        return entity


def wordAndIndex(word):
    words = word.split("-")[0]
    index = int(word.split("-")[1])
    return words, index