class SematicPosModel:
    def __init__(self):
        self.nouns = []
        self.coos = []
        self.verbs = []
        self.adjs = []
        self.isNone = True

        self.nounsHasWords = True if len(self.nouns) else False
        self.coosHasWords = True if len(self.coos) else False
        self.verbsHasWords = True if len(self.verbs) else False
        self.adjsHasWords = True if len(self.adjs) else False