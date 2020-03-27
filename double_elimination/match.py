"""
A match represents a single match in a tournament, between 2 participants.
It adds empty participants as placeholders for the winner and loser,
so they can be accessed as individual object pointers.
"""
from double_elimination.participant import Participant

class Match:
    """
    A match represents a single match in a tournament, between 2 participants.
    It adds empty participants as placeholders for the winner and loser,
    so they can be accessed as individual object pointers.
    """
    def __init__(self, left_participant, right_participant):
        self.__left_participant = left_participant
        self.__right_participant = right_participant
        self.__winner = Participant()
        self.__loser = Participant()

    def set_winner(self, competitor):
        """
        When the match is over, set the winner competitor here and the loser will be set too.
        """
        if competitor == self.__left_participant.get_competitor():
            self.__winner.set_competitor(competitor)
            self.__loser.set_competitor(self.__right_participant.get_competitor())
        elif competitor == self.__right_participant.get_competitor():
            self.__winner.set_competitor(competitor)
            self.__loser.set_competitor(self.__left_participant.get_competitor())
        else:
            raise Exception("Invalid competitor")

    def get_winner_participant(self):
        """
        If the winner is set, get it here. Otherwise this return None.
        """
        return self.__winner

    def get_loser_participant(self):
        """
        If the winner is set, you can get the loser here. Otherwise this return None.
        """
        return self.__loser

    def get_participants(self):
        """
        Get the left and right participants in a list.
        """
        return [self.__left_participant, self.__right_participant]

    def is_ready_to_start(self):
        """
        This returns True if both of the participants coming in have their competitors "resolved".
        This means that the match that the participant is coming from is finished.
        It also ensure that the winner hasn't been set yet.
        """
        is_left_resolved = self.__left_participant.get_competitor() is not None
        is_right_resolved = self.__right_participant.get_competitor() is not None
        is_winner_resolved = self.__winner.get_competitor() is not None
        return is_left_resolved and is_right_resolved and not is_winner_resolved
