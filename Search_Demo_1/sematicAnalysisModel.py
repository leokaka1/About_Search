from Search_Demo_1.semanticVertexModel import SemanticGraphVertexModel
from Search_Demo_1.sematicPosModel import SematicPosModel

"""
词性语义分析模型
"""


class SematicAnalysisModel:
    def __init__(self, vertexModel: SemanticGraphVertexModel, posModel: SematicPosModel):
        self.posModel = posModel
        self.vertexModel = vertexModel

    # 分析名词数组中最后一个词的词性
    def analysisNounsLastWord(self):
        last_noun_word = self.posModel.nouns[-1]
        last_noun_deprel = self.vertexModel.wordForDeprel(last_noun_word)
        # print("lastNoun的词性", last_noun_deprel)
        return last_noun_deprel

    # 分析动词数组中最后一个词的词性
    def analysisVerbsLastWord(self):
        last_verb_word = self.posModel.verbs[-1]
        last_verb_deprel = self.vertexModel.wordForDeprel(last_verb_word)
        # print("lastNoun的词性", last_noun_deprel)
        return last_verb_deprel

    def isLastNounObject(self):
        if self.analysisNounsLastWord() == "SBV" or self.analysisNounsLastWord() == "HED":
            return True
        else:
            return False

    def isLastVerbObject(self):
        if self.analysisVerbsLastWord() == "HED":
            return True
        else:
            return False

    def isLastNounAndVerbObject(self):
        if self.isLastNounObject() or self.isLastVerbObject():
            return True
        else:
            return False

    def assembleRelationshipWord(self):
        relation_word_list = []
        final_sequence_word_list = self.posModel.nouns.copy()
        # 远光软件股份有限公司投标的项目有哪些
        # 远光软件股份有限公司的投标的实际的项目的中标人
        # 1. 先找出n修饰了哪个v，v一般是中心词，所以head=0，只能有n来修饰v
        for verb in self.posModel.verbs:
            target_index = self.vertexModel.wordForHead(verb)
            target_word = self.vertexModel.word_list[target_index]
            relation_word = verb + target_word
            relation_word_list.append(relation_word)
            # 删除noun中的target_index的词
            if target_word in self.posModel.nouns:
                target_word_index_in_nouns = self.posModel.nouns.index(target_word)
                final_sequence_word_list.insert(target_word_index_in_nouns,relation_word)
            if target_word in final_sequence_word_list:
                # print(target_word)
                # print(final_sequence_word_list)
                final_sequence_word_list.remove(target_word)
        # final_sequence_word = self.posModel.nouns + relation_word_list
        print("关系词有>>>>>",relation_word_list)
        print("剩下的名词有>>>>>",self.posModel.nouns)
        print("组装完成后的词序列>>>>>",final_sequence_word_list)



