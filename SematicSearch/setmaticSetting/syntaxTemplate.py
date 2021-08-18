from SematicSearch.model.analysisModel import SematicAnalysisModel
from SematicSearch.utils import *

lexicon = Lexicon()


class Template:
    def __init__(self, model: SematicAnalysisModel):
        self.model = model

        # HED词是"有"，"是"这些词

    # 如果只有ATT修饰HED
    # 远光软件股份有限公司投标项目的中标人
    def has_HED_Words(self):
        pass

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
