from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils.lexicon import *
from SematicSearch.utils.distinguishwords import *

lexicon = Lexicon()


def sematicPasing(analysisModel: SematicAnalysisModel):
    # 如果句子结尾是"HED"(不论HED是否是noun或verb)
    if analysisModel.isLastNounAndVerbObject():
        print("HED是最后一个")
        entities = findEntityAndIndex(analysisModel.nouns)
        verbsRelatedNouns(analysisModel)

    # 如果"HED"不在最后
    else:
        pass


def findEntityAndIndex(nouns):
    nouns = nouns
    entities, entities_type = lexicon.receiveEntitiesInfo()
    returnEntities_list = []

    for noun in nouns:
        if noun in entities:
            word = lexicon.receiveEntitiesWordAndType(noun)
            returnEntities_list.append(word)

    print("1. 搜索实例词，如果实例词在实例词库中，则构建成:>>>>>>>", returnEntities_list)
    return returnEntities_list


# 重组动词和名词之间的关系
def verbsRelatedNouns(analysisModel: SematicAnalysisModel):
    words = analysisModel.vertexModel.word_list
    verbs = analysisModel.verbs
    final_relation_sequences = []

    for index,verb in enumerate(verbs):
        word_deprel = analysisModel.vertexModel.wordForDeprel(verb)
        verb_position = analysisModel.vertexModel.wordForId(verb)

        # 如果动词是HED并且是虚拟问词
        if isVerbContainedHEDwords(verb) and analysisModel.isHedWord(verb):
            pass
        else:
            verb_target_word = analysisModel.vertexModel.wordForTargetWord(verb)
            final_relation_sequences.append(verb)
            final_relation_sequences.append(verb_target_word)

    print("2.清除了HED关系动词之后的数组>>>>>>", final_relation_sequences)