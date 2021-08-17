from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils import *

lexicon = Lexicon()


def sematicPasing(analysisModel: SematicAnalysisModel, situation: Situations):
    # noAttribute
    # print(situation.value)
    verbsRelatedNouns(analysisModel)
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
    verbs = analysisModel.verbs
    final_relation_sequences = []

    for index, verb in enumerate(verbs):
        verbW = verb.split("-")[0]
        verbP = int(verb.split("-")[1])
        verb_target_word = analysisModel.vertexModel.headIndexForWord(verbP)
        # 如果动词是HED并且是虚拟问词
        if isVerbContainedHEDwords(verbW) and analysisModel.isHedWord(verbW):
            # 判断名词，如果有指向这个verb的词中间有SBV，那么可以判断这个noun是主语
            sbv_word = analysisModel.verbForSBV(verbW)
            final_relation_sequences.append(sbv_word)
            continue
        elif not analysisModel.isHedWord(verbW):
            final_relation_sequences.append(verbW)
            if verb_target_word != "":
                final_relation_sequences.append(verb_target_word)

    print("2.清除了HED关系动词之后的数组>>>>>>", final_relation_sequences)
