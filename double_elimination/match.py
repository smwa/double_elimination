from double_elimination.participant import Participant

class Match:
    def __init__(self, left_participant, right_participant):
        self.__left_participant = left_participant
        self.__right_participant = right_participant
        self.__winner = Participant()
        self.__loser = Participant()

    def setWinner(self, competitor):
        if competitor is self.__left_participant.getCompetitor():
            self.__winner.setCompetitor(competitor)
            self.__loser.setCompetitor(self.__right_participant.getCompetitor())
        elif competitor is self.__right_participant.getCompetitor():
            self.__winner.setCompetitor(competitor)
            self.__loser.setCompetitor(self.__left_participant.getCompetitor())
        else:
            raise Exception("Invalid competitor")
    
    def getWinnerParticipant(self):
        return self.__winner
    
    def getLoserParticipant(self):
        return self.__loser
    
    def getParticipants(self):
        return [self.__left_participant, self.__right_participant]

    def isReadyToStart(self):
        return (self.__left_participant.getCompetitor() is not None and self.__right_participant.getCompetitor() is not None and self.__winner.getCompetitor() is None)
