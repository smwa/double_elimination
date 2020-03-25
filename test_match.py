from double_elimination import Match, Participant

competitors = ['1', '2']

match = Match(Participant(competitors[0]), Participant(competitors[1]))
participants = match.getParticipants()
assert participants[0].getCompetitor() == competitors[0], 'bad competitor'
assert participants[1].getCompetitor() == competitors[1], 'bad competitor'
assert len(participants) == len(competitors), 'bad competitor list'
assert match.getWinnerParticipant().getCompetitor() is None, 'Bad winner'
try:
    match.setWinner(2)
    assert False, 'allows setting winner to bad id'
except Exception:
    pass

match.setWinner(competitors[0])
winner = match.getWinnerParticipant().getCompetitor()
assert winner == '1', 'bad winner'

matchOne = Match(Participant('1'), Participant('2'))
matchOne.setWinner('2')
assert matchOne.getLoserParticipant().getCompetitor() == '1'
matchTwo = Match(Participant('3'), Participant('4'))
assert matchTwo.isReadyToStart() is True
matchThree = Match(matchOne.getWinnerParticipant(), matchTwo.getWinnerParticipant())
assert matchThree.isReadyToStart() is False
matchTwo.setWinner('4')
assert matchTwo.isReadyToStart() is False
assert matchThree.isReadyToStart() is True
matchThree.setWinner('2')
assert matchThree.isReadyToStart() is False
winner = matchThree.getWinnerParticipant().getCompetitor()
assert winner is '2', winner

print("Match tests passed")
