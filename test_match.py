from double_elimination import Match, Participant

competitors = ['1', '2']

match = Match(Participant(competitors[0]), Participant(competitors[1]))
participants = match.get_participants()
assert participants[0].get_competitor() == competitors[0], 'bad competitor'
assert participants[1].get_competitor() == competitors[1], 'bad competitor'
assert len(participants) == len(competitors), 'bad competitor list'
assert match.get_winner_participant().get_competitor() is None, 'Bad winner'
try:
    match.set_winner(2)
    assert False, 'allows setting winner to bad id'
except Exception:
    pass

match.set_winner(competitors[0])
winner = match.get_winner_participant().get_competitor()
assert winner == '1', 'bad winner'

matchOne = Match(Participant('1'), Participant('2'))
matchOne.set_winner('2')
assert matchOne.get_loser_participant().get_competitor() == '1'
matchTwo = Match(Participant('3'), Participant('4'))
assert matchTwo.is_ready_to_start() is True
matchThree = Match(matchOne.get_winner_participant(), matchTwo.get_winner_participant())
assert matchThree.is_ready_to_start() is False
matchTwo.set_winner('4')
assert matchTwo.is_ready_to_start() is False
assert matchThree.is_ready_to_start() is True
matchThree.set_winner('2')
assert matchThree.is_ready_to_start() is False
winner = matchThree.get_winner_participant().get_competitor()
assert winner is '2', winner

print("Match tests passed")
