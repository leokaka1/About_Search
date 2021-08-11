class SematicPosModel:
    def __init__(self,nouns,coos,verbs,adjs,attri):
        self.nouns = nouns
        self.coos = coos
        self.verbs = verbs
        self.adjs = adjs
        self.attri = attri
        self.isNone = True

        self.nounsHasWords = True if len(nouns) else False
        self.coosHasWords = True if len(coos) else False
        self.verbsHasWords = True if len(verbs) else False
        self.adjsHasWords = True if len(adjs) else False
        self.attriHasWords = True if len(attri) else False

