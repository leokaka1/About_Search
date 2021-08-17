from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils import *

lexicon = Lexicon()


class SematicPasing:
    def __init__(self, analysisModel: SematicAnalysisModel, situation: Situations):
        self.analysisModel = analysisModel

    def pasing(self):
        # noAttribute
        # print(situation.value)
        entity = self.findSimpleEntityAndIndex()
        mapping_sequence = self.verbsRelatedNouns()
        final = self.combinationToSequence(entity, mapping_sequence)
        # if situation.value == 0:
        #     # 如果句子结尾是"HED"(不论HED是否是noun或verb)
        #     if analysisModel.isLastNounAndVerbObject():
        #         print("HED是最后一个")
        #         entities = findEntityAndIndex(analysisModel.nouns)
        #         verbsRelatedNouns(analysisModel)
        #     # 如果"HED"不在最后
        #     else:
        #         pass
        # else:
        #     print("有属性值")
        return final

    # 只有一个实例的情况
    def findSimpleEntityAndIndex(self):
        nouns = self.analysisModel.nouns
        entities, entities_type = lexicon.receiveEntitiesInfo()
        entity = ""

        for noun in nouns:
            noun = noun.split("-")[0]
            if noun in entities:
                word = lexicon.receiveEntitiesWordAndType(noun)
                entity = word

        print("1.搜索实例词>>>>>>>", entity)
        return entity

    # 重组动词和名词之间的关系
    def verbsRelatedNouns(self):
        verbs = self.analysisModel.verbs
        final_mapping_sequences = []

        for index, verb in enumerate(verbs):
            verbW = verb.split("-")[0]
            verbP = int(verb.split("-")[1])
            verb_target_word = self.analysisModel.vertexModel.headIndexForWord(verbP)
            # 如果动词是HED并且是虚拟问词
            if isVerbContainedHEDwords(verbW) and self.analysisModel.isHedWord(verbW):
                # 判断名词，如果有指向这个verb的词中间有SBV，那么可以判断这个noun是主语
                sbv_word = self.analysisModel.verbForSBV(verbW)
                if sbv_word not in final_mapping_sequences:
                    final_mapping_sequences.append(sbv_word)
                continue
            elif not self.analysisModel.isHedWord(verbW):
                final_mapping_sequences.append(verbW)
                # 如果动词的目标词不是空并且不是HED词，就添加
                # eg: 施工标的类项目都有哪些公司中标
                if verb_target_word != "" and not self.analysisModel.isHedWord(verb_target_word):
                    final_mapping_sequences.append(verb_target_word)

        # 如果返回数组为空，则考虑其他的情况
        if not final_mapping_sequences:
            print("为不畏龙")
            # FIXME: 判断有没有SBV，如果没有SBV的话，就判断主语和谓语之间的关系，有可能是VOB宾语
            #   eg: 有乙方的单位
            if not self.analysisModel.isSBVword():
                for noun in self.analysisModel.nouns:
                    noun = noun.split("-")[0]
                    if self.analysisModel.vertexModel.wordForDeprel(noun) == "VOB":
                        vob_target_list = self.analysisModel.vertexModel.modifiedWord(noun)
                        final_mapping_sequences.append(noun)
                        final_mapping_sequences += vob_target_list

        # FIXME：判断如果HED在最后，并且是名词，而且final_mapping_sequences没有HED，则添加在句尾
        #   eg：远光股份有限公司中标项目的类型
        if self.analysisModel.isLastNounAndVerbObject() and not self.analysisModel.islistContainHEDword(
                final_mapping_sequences):
            final_mapping_sequences.append(self.analysisModel.getHEDWord())

        print("2.重组了动词和名词之间的关系后>>>>>>", final_mapping_sequences)
        return final_mapping_sequences

    # 重组实例和后面的关系
    def combinationToSequence(self, entity, mapping_sequence):
        final_combination_list = []
        new_combination = []

        # print("new_verbs>>>>>", mapping_sequence)
        if not lexicon.listContainInstance(mapping_sequence):
            final_combination_list.append(entity)
        final_combination_list += mapping_sequence

        print("3.实例和动词序列重组之后>>>>>", final_combination_list)
        return final_combination_list
