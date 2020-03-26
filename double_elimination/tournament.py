import math

from double_elimination.match import Match
from double_elimination.participant import Participant

class Tournament:
    def __init__(self, competitors_list):
        assert len(competitors_list) > 1
        self.__matches = []
        number_of_participants = int(math.pow(2, math.ceil(math.log2(len(competitors_list)))))
        number_of_byes = number_of_participants - len(competitors_list)
        incoming_participants = list(map(Participant, competitors_list))
        incoming_participants.extend([None] * number_of_byes)

        one_loss_participants = []
        extended_round_one = (number_of_byes > 0)
        # TODO Winners needs to keep everyone in round 1 until they've all played. Maybe the loser's round should be the min(number of matches played)
        while len(incoming_participants) > 1:
            one_loss_participants.append([])
            half_length = int(len(incoming_participants)/2)
            first = incoming_participants[0:half_length]
            last = incoming_participants[half_length:]
            last.reverse()
            new_participants = []
            for participant_pair in zip(first, last):
                if participant_pair[1] is None:
                    new_participants.append(participant_pair[0])
                else:
                    match = Match(participant_pair[0], participant_pair[1])
                    new_participants.append(match.getWinnerParticipant())
                    target_loser_round = len(one_loss_participants) - 1
                    one_loss_participants[target_loser_round].append(match.getLoserParticipant())
                    self.__matches.append(match)
            incoming_participants = new_participants
        
        for loser_round in range(0, len(one_loss_participants), 2):
            print(loser_round)
            one_loss_participants[loser_round].reverse()

        if extended_round_one:
            one_loss_participants[1].extend(one_loss_participants[0])
            del one_loss_participants[0]
        while len(one_loss_participants) < (math.ceil(math.log2(number_of_participants)) + 1):
            one_loss_participants.append([])
        winner = incoming_participants[0]

        for loser_round in range(len(one_loss_participants)):        
            incoming_participants = one_loss_participants[loser_round]
            number_of_participants = int(math.pow(2, math.ceil(math.log2(len(incoming_participants)))))
            number_of_byes = number_of_participants - len(incoming_participants)
            incoming_participants.extend([None] * number_of_byes)
            
            if len(incoming_participants) > 1:
                half_length = math.ceil(len(incoming_participants)/2)
                first = incoming_participants[0:half_length]
                last = incoming_participants[half_length:]
                last.reverse()
                winner_and_bye_participants = []
                for participant_pair in zip(first, last):
                    if participant_pair[0] is None:
                        winner_and_bye_participants.append(participant_pair[1])
                    elif participant_pair[1] is None:
                        winner_and_bye_participants.append(participant_pair[0])
                    else:
                        match = Match(participant_pair[0], participant_pair[1])
                        winner_and_bye_participants.append(match.getWinnerParticipant())
                        self.__matches.append(match)
                incoming_participants = winner_and_bye_participants
            if loser_round + 1 < len(one_loss_participants):
                # Next round exists
                one_loss_participants[loser_round + 1].extend(incoming_participants)
            else:
                # Grand finals
                print(len(incoming_participants))
                match = Match(incoming_participants[0], winner)
                self.__matches.append(match)
    
    def __iter__(self):
        return iter(self.__matches)
    
    def getActiveMatches(self):
        return [match for match in self.getMatches() if match.isReadyToStart()]
    
    def getMatches(self):
        return self.__matches

    def getActiveMatchForCompetitor(self, id):
        matches = [match for match in self.getActiveMatches() if id in [participant.getCompetitor() for participant in match.getParticipants()]]
        if len(matches) > 0:
            return matches[0]
        return None
    
    def addWin(self, match, competitor):
        match.setWinner(competitor)
