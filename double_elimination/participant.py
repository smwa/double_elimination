class Participant:
    def __init__(self, competitor=None):
        self.competitor = competitor

    def getCompetitor(self):
        return self.competitor

    def setCompetitor(self, competitor):
        self.competitor = competitor
