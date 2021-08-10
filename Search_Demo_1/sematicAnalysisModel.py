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
        if self.posModel.nounsHasWords:
            last_noun_word = self.posModel.nouns[-1]
            last_noun_deprel = self.vertexModel.wordForDeprel(last_noun_word)
            print("lastNoun的词性", last_noun_deprel)
            return last_noun_deprel

    # 分析动词数组中最后一个词的词性
    def analysisVerbsLastWord(self):
        if self.posModel.verbsHasWords:
            last_verb_word = self.posModel.verbs[-1]
            last_verb_deprel = self.vertexModel.wordForDeprel(last_verb_word)
            print("lastNoun的词性", last_verb_deprel)
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

    def assembleRelationshipWordAtHEDLast(self):
        relation_word_list = []
        temp_coos_list = []
        coos_relations_list = []
        final_sequence_word_list = self.posModel.nouns.copy()
        flag_index = 0
        # 远光软件股份有限公司投标的项目有哪些
        # 远光软件股份有限公司的投标的实际的项目的中标人
        # 1. 先找出n修饰了哪个v，v一般是中心词，所以head=0，只能有n来修饰v
        for verb in self.posModel.verbs:
            # target_index = self.vertexModel.wordForHead(verb)
            target_word = self.vertexModel.wordForTargetWord(verb)
            # 如果中心词不在谓语列表中，说明在名词中，在谓语中则不拼接
            if target_word not in self.posModel.verbs:
                relation_word = verb + target_word
                relation_word_list.append(relation_word)
            else:
                # 若谓词不是HED中心词就添加，是中心词则放弃
                if self.vertexModel.wordForDeprel(verb) != "HED":
                    relation_word_list.append(verb)
            # 删除noun中的target_index的词
            if target_word in self.posModel.nouns:
                target_word_index_in_nouns = self.posModel.nouns.index(target_word)
                final_sequence_word_list.insert(target_word_index_in_nouns, relation_word)
            else:
                # 如果targeted不在nouns有可能是动词自己创建关系，所以只添加除了中心词之外的谓词
                for index, word in enumerate(final_sequence_word_list):
                    # 如果遇到剩下的谓词是VOB修饰中心词HED，那么调整一下VOB和SBV的位置
                    # FIXME:施工标的类合同都有哪些公司中标
                    if word in self.vertexModel.word_list:
                        word_pos = self.vertexModel.wordForHead(word)
                        verb_pos = self.vertexModel.wordForHead(verb)
                        # print("word_pos",word_pos)
                        # print("verb_pos",verb_pos)
                        # print(verb)
                        if word_pos == verb_pos:
                            flag_index = index + 1
                    # print(flag_index)
                # 这里保证如果谓语是"HED"中心词则不添加，避免加入其他词汇
                if self.vertexModel.wordForDeprel(verb) != "HED":
                    final_sequence_word_list.insert(flag_index, verb)

            if target_word in final_sequence_word_list:
                # print(target_word)
                # print(final_sequence_word_list)
                final_sequence_word_list.remove(target_word)

        # 找到有没有并列的COO的词，如果是并列关系则会生成两条解析
        for word in self.posModel.nouns:
            if self.vertexModel.wordForDeprel(word) == "COO":
                target_word = self.vertexModel.wordForTargetWord(word)
                temp_coos_list.append(word)
                temp_coos_list.append(target_word)
                if target_word in final_sequence_word_list:
                    final_sequence_word_list.remove(target_word)
                final_sequence_word_list.remove(word)
                # print(word)
                # print(target_word)
        temp_coos_list = set(temp_coos_list)
        # print(temp_coos_list)
        # print(final_sequence_word_list)

        for word in temp_coos_list:
            temp_list = final_sequence_word_list.copy()
            temp_list.insert(0, word)
            coos_relations_list.append(temp_list)
            # print(coos_relations_list)

        if self.vertexModel.isHasCOO:
            final_sequence_word_list = coos_relations_list

        print("关系词有>>>>>", relation_word_list)
        print("剩下的名词有>>>>>", self.posModel.nouns)
        print("组装完成后的词序列>>>>>", final_sequence_word_list)

        return final_sequence_word_list

    # 处理成三元组
    def copeTripleRelations(self):
        triple_ralation_list = []
        # 遍历nouns
        for index,nounWord in enumerate(self.posModel.nouns):
            noun_target_word = self.vertexModel.wordForTargetWord(nounWord)

            if self.vertexModel.wordForDeprel(nounWord) != "HED":
                for verbWord in self.posModel.verbs:
                    temp_triple_relation = []
                    verb_target_word = self.vertexModel.wordForTargetWord(verbWord)
                    # 如果名词和动词的目标词一致，则规划三元组
                    if noun_target_word == verb_target_word:
                        temp_triple_relation.append(nounWord)
                        temp_triple_relation.append(verbWord)
                        temp_triple_relation.append(verb_target_word)
                        triple_ralation_list.append(temp_triple_relation)
                    elif noun_target_word == verbWord:
                        # 如果名词修饰动词，则直接规划三元组
                        temp_triple_relation.append(nounWord)
                        temp_triple_relation.append(verbWord)
                        temp_triple_relation.append(verb_target_word)
                        triple_ralation_list.append(temp_triple_relation)

        print("构造出来的三元组合为:>>>>>",triple_ralation_list)