"""
This defines a double elimination 'Tournament' object.
"""
import math
import itertools

from double_elimination.match import Match
from double_elimination.participant import Participant

class Tournament:
    """
    This is a double-elimination tournament where each match is between 2 competitors.
    When a competitor loses they are sent to the losers bracket where they'll play until
    they lose again or they make it to the final match against the winner of the winners bracket.
    It does not handle a second "grand finals" match, that should be handled outside of this object.
    It takes in a list of competitors, which can be strings or any type of Python object,
    but they should be unique. They should be ordered by a seed, with the first entry being the most
    skilled and the last being the least. They can also be randomized before creating the instance.
    """
    def __init__(self, competitors_list):
        assert len(competitors_list) > 1
        self.__matches = []
        next_higher_power_of_two = int(math.pow(2, math.ceil(math.log2(len(competitors_list)))))
        winners_number_of_byes = next_higher_power_of_two - len(competitors_list)
        incoming_participants = list(map(Participant, competitors_list))
        incoming_participants.extend([None] * winners_number_of_byes)

        last_winner = None
        last_loser = None

        losers_by_round = []
        while len(incoming_participants) > 1:
            losers = []
            half_length = int(len(incoming_participants)/2)
            first = incoming_participants[0:half_length]
            last = incoming_participants[half_length:]
            last.reverse()
            next_round_participants = []
            for participant_pair in zip(first, last):
                if participant_pair[1] is None:
                    next_round_participants.append(participant_pair[0])
                elif participant_pair[0] is None:
                    next_round_participants.append(participant_pair[1])
                else:
                    match = Match(participant_pair[0], participant_pair[1])
                    next_round_participants.append(match.get_winner_participant())
                    last_winner = match.get_winner_participant()
                    losers.append(match.get_loser_participant())
                    self.__matches.append(match)
            if len(losers) > 0:
                losers_by_round.append(losers)
            incoming_participants = next_round_participants

        if winners_number_of_byes > 0 and len(losers_by_round) > 1:
            losers_by_round[1].extend(losers_by_round[0])
            losers_by_round = losers_by_round[1:]

        empty_by_round = []
        for __ in losers_by_round:
            empty_by_round.append([])
        losers_by_round = list(itertools.chain(*zip(losers_by_round, empty_by_round)))
        if len(losers_by_round) > 2:
            new_losers = [losers_by_round[0]]
            new_losers.extend(losers_by_round[2:])
            losers_by_round = new_losers

        for loser_round in range(0, len(losers_by_round), 4):
            losers_by_round[loser_round].reverse()

        index = 0
        incoming_participants = []
        for losers in losers_by_round:
            incoming_participants = losers

            if len(incoming_participants) > 1:
                next_higher_power_of_two = int(math.pow(2, math.ceil(math.log2(len(incoming_participants)))))
                number_of_byes = next_higher_power_of_two - len(incoming_participants)
                incoming_participants.extend([None] * number_of_byes)

                half_length = math.ceil(len(incoming_participants)/2)
                first = incoming_participants[0:half_length]
                last = incoming_participants[half_length:]
                last.reverse()
                incoming_participants = []
                for participant_pair in zip(first, last):
                    if participant_pair[0] is None:
                        incoming_participants.append(participant_pair[1])
                    elif participant_pair[1] is None:
                        incoming_participants.append(participant_pair[0])
                    else:
                        match = Match(participant_pair[0], participant_pair[1])
                        incoming_participants.append(match.get_winner_participant())
                        self.__matches.append(match)
                if len(incoming_participants) > 0:
                    if len(losers_by_round) <= index + 1:
                        losers_by_round.append(incoming_participants)
                    else:
                        losers_by_round[index + 1].extend(incoming_participants)
            elif len(losers_by_round) > index + 1:
                losers_by_round[index + 1].extend(incoming_participants)
            if len(incoming_participants) == 1:
                last_loser = incoming_participants[0]
            index += 1
        match = Match(last_winner, last_loser)
        self.__winner = match.get_winner_participant()
        self.__matches.append(match)

    def __iter__(self):
        return iter(self.__matches)

    def get_active_matches(self):
        """
        Returns a list of all matches that are ready to be played.
        """
        return [match for match in self.get_matches() if match.is_ready_to_start()]

    def get_matches(self):
        """
        Returns a list of all matches for the tournament.
        """
        return self.__matches

    def get_active_match_for_competitor(self, competitor):
        """
        Given the string or object of the competitor that was supplied
        when creating the tournament instance,
        returns a Match that they are currently playing in,
        or None if they are not up to play.
        """
        matches = []
        for match in self.get_active_matches():
            competitors = [participant.get_competitor() for participant in match.get_participants()]
            if competitor in competitors:
                matches.append(match)
        if len(matches) > 0:
            return matches[0]
        return None

    def get_winners(self):
        """
        Returns None if the tournament is done, otherwise
        returns list of the one victor.
        """
        if len(self.get_active_matches()) > 0:
            return None
        return [self.__winner.get_competitor()]

    def add_win(self, competitor):
        """
        Set the victor of a match, given the competitor string/object.
        """
        self.get_active_match_for_competitor(competitor).set_winner(competitor)
