import unittest
from fractions import Fraction
from turnout_election_schemes.schemes.errors import FailedElectionError
from turnout_election_schemes.schemes.singletransferablevote.scheme import Round

class RoundTest(unittest.TestCase):
    def test_all_vacancies_filled_should_be_true_after_round_runs(self):
        """
        Before a round has run it should report that all vacancies have not
        been filled. After the round runs it should report that all vacancies
        have been filled.
        """

        vacancies = 2
        candidates = ('Red', 'Green', 'Blue')
        votes = 4 * (('Red', ), ) + \
                3 * (('Green', ), )

        stv_round = Round(vacancies, candidates, votes)
        self.assertFalse(stv_round.all_vacancies_filled())

        stv_round.run()
        self.assertTrue(stv_round.all_vacancies_filled())

    def test_all_vacancies_filled_should_be_false_after_incomplete_round(self):
        """
        After a round runs that fails to elect enough candidates the round
        should report that it has not filled all vacancies.
        """

        vacancies = 2
        candidates = ('Red', 'Green', 'Blue', 'Yellow', 'Mauve')
        votes = 5 * (('Red', ), ) + \
                4 * (('Green', ), ) + \
                3 * (('Blue', ), ) + \
                2 * (('Yellow', ), ) + \
                1 * (('Mauve', ), )

        stv_round = Round(vacancies, candidates, votes)
        stv_round.run()
        self.assertFalse(stv_round.all_vacancies_filled())

    def test_reallocation_of_surplus_votes(self):
        """
        A single round should reallocate surplus votes from all candidates that
        have a surplus and then exclude the candidate with the fewest votes.
        """

        vacancies = 3
        candidates = ('Oranges', 'Apples', 'Pears', 'Lemons', 'Limes')
        votes = 9 * (('Oranges', 'Pears'), ) + \
                7 * (('Apples', 'Lemons'), )

        expected_results = {
            'provisionally_elected': {
                'Oranges': 5,
                'Apples': 5
            },
            'continuing': {
                'Pears': 4,
                'Lemons': 2
            },
            'excluded': {
                'Limes': 0
            }
        }

        stv_round = Round(vacancies, candidates, votes)
        stv_round.run()
        self.assertEqual(expected_results, stv_round.results())

    def test_tied_winners_should_cause_election_to_fail(self):
        votes = (
            ('A', 'C'), ('A', 'C'), ('A', 'C'), ('A', 'C'), ('A', 'C'),
            ('B', 'C'), ('B', 'C'), ('B', 'C'), ('B', 'C'), ('B', 'C'),
        )
        candidates = ['A', 'B', 'C', 'D', 'E']
        vacancies = 3

        stv_round = Round(vacancies, candidates, votes)

        with self.assertRaises(FailedElectionError):
            stv_round.run()

    def test_tied_losers_should_cause_election_to_fail(self):
        votes = (
            ('A', 'C'), ('A', 'D'),
            ('B', 'E'), ('B', 'E'),
            ('C', ), ('C', ), ('C', ),
            ('D', ), ('D', ), ('D', ),
            ('E', ), ('E', ), ('E', ),
        )
        candidates = ['A', 'B', 'C', 'D', 'E']
        vacancies = 3

        stv_round = Round(vacancies, candidates, votes)

        with self.assertRaises(FailedElectionError):
            stv_round.run()

    def test_candidates_should_be_elected_once_there_is_one_per_vacancy(self):
        """
        As soon as there are the same number of remaining candidates as
        vacancies the election is completed with all of the remaining
        candidates elected as winners.

        Note that this makes it possible for a candidate to be elected even
        without enough votes to reach the quota, as in this example.

        Surplus votes for candidates A and B become exhausted votes because
        there is no further preference to reallocate them to. Candidate D is
        then excluded because they have the fewest votes. Since this leaves
        only three candidates for three vacancies candidate C is declared
        elected, even though they have only one vote compared to the quota of
        three.
        """

        vacancies = 3
        candidates = ('A', 'B', 'C', 'D')
        votes = 6 * (('A', 'B'), ), + \
                5 * (('B', 'A'), ), + \
                1 * (('C', ), )

        expected_results = {
            'provisionally_elected': {
                'A': 3,
                'B': 3,
                'C': 1
            },
            'continuing': {},
            'excluded': {
                'D': 0
            },
        }

        stv = Round(vacancies, candidates, votes)
        stv.run()
        self.assertEqual(expected_results, stv.results())
        self.assertTrue(stv.all_vacancies_filled())
