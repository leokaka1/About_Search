class SematicPosModel:
    def __init__(self,nouns,coos,verbs,adjs,attri):
        self.nouns = nouns
        self.coos = coos
        self.verbs = verbs
        self.adjs = adjs
        self.attri = attri

        self.nounsHasWords = True if len(nouns) else False
        self.coosHasWords = False if len(coos) else True
        self.verbsHasWords = True if len(verbs) else False
        self.adjsHasWords = True if len(adjs) else False
        self.attriHasWords = True if len(attri) else False



