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
    Optional options dict fields:
    """
    def __init__(self, competitors_list, bracket_reset_finals=True):
        # Only tournaments with 2 or more competitors are valid.
        assert len(competitors_list) > 1
        self.__matches = []
        self.__bracket_reset_finals = bracket_reset_finals
        # Find minimum 'n' such that 2^n >= number of competitors
        next_higher_power_of_two = int(math.pow(2, math.ceil(math.log2(len(competitors_list)))))
        # Since the bracket is fundamentally a binary tree with 2^n nodes,
        # assign the winners enough byes to fill out the 2^n slots.
        winners_number_of_byes = next_higher_power_of_two - len(competitors_list)
        # Create participants for first round (real and empty)
        incoming_participants = list(map(Participant, competitors_list))
        incoming_participants.extend([None] * winners_number_of_byes)
        # Keep track of the participants at the end of the winner's and
        # loser's brackets. Later, we will assemble these into the finals match.
        last_winner = None
        last_loser = None

        losers_by_round = []
        while len(incoming_participants) > 1:
            losers = []
            # Split participants into best and worst
            half_length = int(len(incoming_participants)/2)
            first = incoming_participants[0:half_length]
            last = incoming_participants[half_length:]
            last.reverse()

            next_round_participants = []
            for participant_pair in zip(first, last):
                # If we have only one participant, send that participant
                # directly to the next round.
                if participant_pair[1] is None:
                    next_round_participants.append(participant_pair[0])
                elif participant_pair[0] is None:
                    next_round_participants.append(participant_pair[1])
                # If we have two participants, generate a match and send
                # the winner of the match to the next winner's round,
                # and the loser of the match to the loser's bracket.
                else:
                    match = Match(participant_pair[0], participant_pair[1])
                    next_round_participants.append(match.get_winner_participant())
                    last_winner = match.get_winner_participant()
                    losers.append(match.get_loser_participant())
                    self.__matches.append(match)
            # If we have any losers, create a new losers round.
            # This condition means there will be no empty loser's rounds.
            if len(losers) > 0:
                losers_by_round.append(losers)
            incoming_participants = next_round_participants

        # If we gave anybody bye's in the winner's bracket and there are
        # more than 1 loser's bracket rounds, then skip the first loser's
        # bracket round and merge it with the second loser's bracket round.
        if winners_number_of_byes > 0 and len(losers_by_round) > 1:
            losers_by_round[1].extend(losers_by_round[0])
            losers_by_round = losers_by_round[1:]

        # Mix in empty rounds to the loser's bracket. This gives extra 'room'
        # such that we can sufficiently thin out the loser's bracket
        # to match the number of incoming participants from the winner's
        # bracket in each round.
        # Rationale: For any round beyond the first, the loser's brakcet will 
        # receive 'n' participants from the previous round of the winner's
        # bracket and the loser's bracket. In the next round, we will receive
        # 'n/2' participants from the winner's bracket. Thus, we need to trim
        # down the loser's bracket by a factor of 4, which will take 2 rounds.
        empty_by_round = []
        for __ in losers_by_round:
            empty_by_round.append([])
        losers_by_round = list(itertools.chain(*zip(losers_by_round, empty_by_round)))
        # If there are more than 2 loser's bracket rounds, then
        # remove the 1st empty round from the loser's bracket and keep the rest.
        # Effectively, this disables the thinning for round 1.
        # Round 1 is a special case because it is the ONLY round of the loser's
        # bracket where we ONLY receive participants from the winner's bracket.
        if len(losers_by_round) > 2:
            new_losers = [losers_by_round[0]]
            new_losers.extend(losers_by_round[2:])
            losers_by_round = new_losers

        # Reverse participants every 4 loser's bracket rounds.
        for loser_round in range(0, len(losers_by_round), 4):
            losers_by_round[loser_round].reverse()

        # Create loser's bracket using loser participants from winner's bracket.
        index = 0
        incoming_participants = []
        for losers in losers_by_round:
            incoming_participants = losers

            if len(incoming_participants) > 1:
                # Find minimum 'n' such that 
                # 2^n < number of participants in this round.
                next_higher_power_of_two = int(math.pow(2, math.ceil(math.log2(len(incoming_participants)))))
                # Since every round has a different number of matches
                # in the winners bracket ( non-trivial due to winner's byes),
                # we compute the number of bye's in the loser's bracket
                # on a per-round basis.
                number_of_byes = next_higher_power_of_two - len(incoming_participants)
                incoming_participants.extend([None] * number_of_byes)
                # Loser's bracket is also seeded so match top competitors
                # with bottom competitors
                half_length = math.ceil(len(incoming_participants)/2)
                first = incoming_participants[0:half_length]
                last = incoming_participants[half_length:]
                last.reverse()

                incoming_participants = []
                for participant_pair in zip(first, last):
                    # If we have only one participant, send that participant
                    # directly to the next round.
                    if participant_pair[0] is None:
                        incoming_participants.append(participant_pair[1])
                    elif participant_pair[1] is None:
                        incoming_participants.append(participant_pair[0])
                    else:
                        # If we have two participants, generate a match and send
                        # the winner of the match to the next loser's round,
                        match = Match(participant_pair[0], participant_pair[1])
                        incoming_participants.append(match.get_winner_participant())
                        self.__matches.append(match)
                if len(incoming_participants) > 0:
                    # If this is the last round
                    if len(losers_by_round) <= index + 1:
                        # Create a new round.
                        losers_by_round.append(incoming_participants)
                    # Otherwise, if there is another round
                    else:
                        # Send our (outputted) participants to that round.
                        losers_by_round[index + 1].extend(incoming_participants)
            # If there are 0 or 1 participants in this round, and there is
            # a future round, send the participants there.
            elif len(losers_by_round) > index + 1:
                losers_by_round[index + 1].extend(incoming_participants)
            # If this round only has 1 participant, then set this participant
            # as the winner of the loser's bracket.
            if len(incoming_participants) == 1:
                last_loser = incoming_participants[0]
            index += 1

        # Generate finals match.
        # Important: the incoming winner should always be the first participant to determine bracket reset
        finals_match = Match(last_winner, last_loser)
        self.__matches.append(finals_match)
        self.__finals_match = finals_match
        
        if bracket_reset_finals:
            bracket_reset_finals_match = Match(finals_match.get_winner_participant(), finals_match.get_loser_participant())
            self.__matches.append(bracket_reset_finals_match)
            # The winner of the overall tournament is the winner of the
            # bracket reset finals match.
            self.__winner = bracket_reset_finals_match.get_winner_participant()
            self.__bracket_reset_finals_match = bracket_reset_finals_match
        else:
            self.__winner = finals_match.get_winner_participant()

    def __iter__(self):
        return iter(self.__matches)

    def __repr__(self) -> str:
        winner = self.__winner
        num_matches = len(self.__matches)
        return f'<Tournament winner={winner} num_matches={num_matches}>'

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

    def get_active_matches_for_competitor(self, competitor):
        """
        Given the string or object of the competitor that was supplied
        when creating the tournament instance,
        returns a list of Match's that they are currently playing in.
        """
        matches = []
        for match in self.get_active_matches():
            competitors = [participant.get_competitor() for participant in match.get_participants()]
            if competitor in competitors:
                matches.append(match)
        return matches

    def get_winners(self):
        """
        Returns None if the tournament is done, otherwise
        returns list of the one victor.
        """
        if len(self.get_active_matches()) > 0:
            return None
        return [self.__winner.get_competitor()]

    def add_win(self, match, competitor):
        """
        Set the victor of a match, given the competitor string/object and match.
        """
        match.set_winner(competitor)
        # If we show a match after the winner of the lower bracket beats the winner of the upper bracket
        if self.__bracket_reset_finals:
            finals = self.__finals_match
            bracket_reset = self.__bracket_reset_finals_match
            # If the finals match is played but the bracket reset match is not
            if finals.get_winner_participant().get_competitor() is not None:
                if bracket_reset.get_winner_participant().get_competitor() is None:
                    # If the incoming winner of the finals match won the finals match, then don't play the reset
                    if finals.get_winner_participant().get_competitor() is finals.get_participants()[0].get_competitor():
                        self.add_win(bracket_reset, finals.get_winner_participant().get_competitor())
