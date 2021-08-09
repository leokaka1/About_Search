from Search_Demo_1.sematicPosModel import SematicPosModel
from Search_Demo_1.semanticGraphVertexModel import SemanticGraphVertex
from Search_Demo_1.createCypher import createCypher

# 处理句法格式的各个情况
"""
"""
def posSetting(posModel: SematicPosModel,vertexModel:SemanticGraphVertex):
    # print("收到的Sematic_dict为:", model.isNone)

    # 先判断词性对象中是否为空，如果为空就不做处理
    if not posModel.isNone:
        # 第一种情况 - [HED在最后并且其他的都为ATT] 没有 SBV之类的主谓关系
        pass

    else:
        pass

def hedWordLast():
    pass