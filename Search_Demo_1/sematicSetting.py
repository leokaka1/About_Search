from Search_Demo_1.sematicPosModel import SematicPosModel
from Search_Demo_1.semanticVertexModel import SemanticGraphVertexModel
from Search_Demo_1.createCypher import createCypher
from Search_Demo_1.sematicAnalysisModel import SematicAnalysisModel


# 处理句法格式的各个情况
"""
语义解析模式
模式一 ： [HED在最后并且其他的都为ATT] 没有 SBV之类的主谓关系
"""
def posSetting(analysisModel:SematicAnalysisModel):
    posModel = analysisModel.posModel
    vertexModel = analysisModel.vertextModel
    # 最终的顺序输出列表
    final_sequence_word_list = []

    # print("收到的Sematic_dict为:", model.isNone)

    # 先判断词性对象中是否为空，如果为空就不做处理
    if not posModel.isNone:
        # First Situation
        if vertexModel.hedLast:
            final_sequence_word_list = hedWordLast(posModel,vertexModel)
        pass

    else:
        pass

    print("Step 3 确定的语序数组为:>>>>>\n")
    print(final_sequence_word_list)
    print("--------------------------------------------")
    createCypher(final_sequence_word_list)

# First situation
# 远光软件股份有限公司的投标项目的中标人
def hedWordLast(pos_model,vertex_model):
    # 假设动词和形容词表没有词
    if not pos_model.adjsHasWords and not pos_model.verbsHasWords:
        if not pos_model.coosHasWords:
            final_sequence_word_list = pos_model.nouns

    return final_sequence_word_list

