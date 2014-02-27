import unittest
from fractions import Fraction
from schemes.errors import FailedElectionError
from schemes.singletransferablevote.scheme import Round

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

    @unittest.skip('bulk elimination functionality not yet written')
    def test_bulk_eliminiation_resolves_tied_loser_failures(self):
        votes = (
            ('A', 'D'), ('A', 'D'),
            ('B', 'E'), ('B', 'E'),
            ('C', 'F'), ('C', 'F'), ('C', 'F'),
            ('D', ), ('D', ), ('D', ), ('D', ), ('D', ), ('D', ), ('D', ), ('D', ),
            ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ),
            ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', )
        )
        candidates = ['A', 'B', 'C', 'D', 'E', 'F']
        vacancies = 2

        stv_round = Round(vacancies, candidates, votes)

        stv_round.run()

        expected_results = {
            'provisionally_elected': {},
            'continuing': {
                'D': 8,
                'E': 12,
                'F': 13
            },
            'excluded': {
                'A': 2,
                'B': 2,
                'C': 3
            },
        }

        self.assertEqual(expected_results, stv_round.round_results())

    def test_candidates_should_be_elected_once_there_is_one_per_vacancy(self):
        votes = (
            ('A', 'B'), ('A', 'B'), ('A', 'B'), ('A', 'B'), ('A', 'B'), ('A', 'B'),
            ('B', 'A'), ('B', 'A'), ('B', 'A'), ('B', 'A'),
            ('C')
        )
        candidates = ['A', 'B', 'C', 'D']
        vacancies = 3

        expected_results = {
            'provisionally_elected': {
                'A': 3,
                'B': 3,
                'C': 1
            },
            'continuing': {
            },
            'excluded': {
                'D': 0
            },
        }

        stv = Round(vacancies, candidates, votes)
        stv.run()

        self.assertEqual(expected_results, stv.results())
        self.assertTrue(stv.all_vacancies_filled())
