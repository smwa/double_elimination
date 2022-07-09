''' Exhaustively test tournaments for a small number of competitors,
    making some basic assertions about correctness during and after running
    each tournament. '''

import unittest
import string
import itertools
import collections

from double_elimination import (
    Tournament as DoubleEliminationTournament,
    Match,
    Participant
)

class TestDoubleEliminationAuto(unittest.TestCase):

    def param_test_run_all_tournaments_with_n_teams(self,n: int) -> None:
        ''' Run every possible tournament with 'n' teams. All sequences
            of wins/losses are covered. '''
        competitors = list(string.ascii_uppercase)[:n]
        det = DoubleEliminationTournament(competitors)
        num_matches = len(det.get_matches())

        # Iterate over every possible sequence of (match-wise) winners.
        for winners in itertools.product(['left','right'], repeat=num_matches):
            # Track each competitor's wins and losses so we can assert about
            # them once the tournament is over.
            competitor_wins = collections.defaultdict(int)
            competitor_losses = collections.defaultdict(int)
            # Generate fresh tournament
            det = DoubleEliminationTournament(competitors)
            for winner in winners:
                # The tournament should not be completed yet.
                if det.get_winners() is not None:
                    raise AssertionError("Tournament should not be complete yet.")
                # Get first active match
                match = det.get_active_matches()[0]
                # Mark either the left team or the right team as the winner
                # of this match. Since we iterate over the cartesian product
                # above, this will test all possibilities.
                winner_idx = 0 if winner == 'left' else 1
                winner_participant = match.get_participants()[winner_idx]
                competitor = winner_participant.get_competitor()

                det.add_win(match, competitor)
                competitor_wins[competitor] += 1

                # Loser is the other participant from the same match.
                loser_idx = 1 - winner_idx
                loser_participant = match.get_participants()[loser_idx]

                competitor_losses[loser_participant.get_competitor()] += 1

            # Since we have added wins for all 6 games, the tournament
            # should now be completed.
            if det.get_winners() is None:
                raise AssertionError("Tournament should be complete.")

            winner = det.get_winners()[0]

            for competitor in competitors:
                wins = competitor_wins[competitor]
                losses = competitor_losses[competitor]

                if competitor == winner:
                    # The winner must have lost either 0 or 1 times.
                    # That is, they have NOT been double-eliminated.
                    self.assertLess(losses,2)
                    # The winner should have won some matches.
                    self.assertGreater(wins,0)
                else:
                    # Nobody should have lost more than twice.
                    self.assertLessEqual(losses,2)
                    # If we were running the grand finals,
                    # then we would also assert that every non-winner
                    # has been double eliminated. However, with only a finals
                    # match, it is possible that a competitor made it all
                    # the way through the upper bracket only to be beaten
                    # in the 'upper-vs-lower' finals match.

    def test_run_exhaustive_tournaments(self) -> None:
        ''' Parameterized test to run exhaustive tournaments for a few
            different values of 'n', where 'n' is the number of competitors. '''
        for n in range(2,8): # Run from n=2 to n=7 (inclusive).
            with self.subTest(n=n):
                self.param_test_run_all_tournaments_with_n_teams(n)

if __name__ == '__main__':
    unittest.main()
