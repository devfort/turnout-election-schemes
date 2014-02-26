import unittest
from schemes.singletransferablevote.scheme import SingleTransferableVoteScheme
from fractions import Fraction

class SingleTransferableVoteTest(unittest.TestCase):
    """
    Pulling out the test for the full process from tests for individual methods.
    Expect this to change as method is refined.
    """
    def test_initial_case(self):
        """
        This election has three rounds and ends successfully with three
        candidates elected.
        """
        votes = [
            ['Norm', 'Anna', 'Steve'],
            ['Dom', 'Anna', 'Steve', 'Norm', 'Amy'],
            ['Dom', 'Steve', 'Norm', 'Anna'],
            ['Norm', 'Steve', 'Amy', 'Anna', 'Dom'],
            ['Anna', 'Amy', 'Steve', 'Norm', 'Dom'],
            ['Anna', 'Steve', 'Norm', 'Amy', 'Dom'],
            ['Anna', 'Dom', 'Steve', 'Norm'],
            ['Norm', 'Steve', 'Dom', 'Anna', 'Amy'],
            ['Anna', 'Norm', 'Steve', 'Dom', 'Amy'],
            ['Anna', 'Norm', 'Steve'],
        ]
        candidates = ['Dom', 'Anna', 'Steve', 'Norm', 'Amy']
        seats = 3

        stv = SingleTransferableVoteScheme(seats, candidates, votes)

        results_1 = stv.run_round()
        expected_round_1 = {
            'provisionally_elected': {
                'Anna': 3,
                'Norm': 3,
            },
            'continuing': {
                'Dom', 2 + Fraction(2,5),
                'Steve', 1 + Fraction(1,5),
            },
            'excluded': {
                'Amy', Fraction(2,5),
            },
        }

        self.assertEqual(expected_round_1, results_1)
        self.assertFalse(stv.completed())

        results_2 = stv.run_round()
        expected_round_2 = {
            'provisionally_elected': {
                'Anna': 3,
                'Norm': 3,
            },
            'continuing': {
                'Dom': 2 + Fraction(2,5),
            },
            'excluded': {
                'Steve': 1 + Fraction(3,5),
            },
        }

        self.assertEqual(expected_round_2, results_2)
        self.assertFalse(stv.completed())

        results_3 = stv.run_round()
        expected_round_3 = {
            'provisionally_elected': {
                'Anna': 3,
                'Norm': 3,
                'Dom': 3 + Fraction (59,115),
            },
            'continuing': {},
            'excluded': {},
        }

        self.assertEqual(expected_round_3, results_3)
        self.assertTrue(stv.completed())

        final_results = [
            'Anna',
            'Norm',
            'Dom',
        ]
        self.assertEqual(final_results, stv.final_results())

    def test_exhausted_ballots_should_not_be_used(self):
        votes = (
            ('A',),
            ('B',), ('B',),
            ('C',), ('C',), ('C',),
            ('D',), ('D',), ('D',), ('D',),
            ('E',), ('E',), ('E',), ('E',), ('E',),
            ('F',), ('F',), ('F',), ('F',), ('F',), ('F',)
        )
        candidates = ['A', 'B', 'C', 'D', 'E', 'F']
        seats = 2

        stv = SingleTransferableVoteScheme(seats, candidates, votes)

        results_1 = stv.run_round()
        expected_round_1 = {
            'provisionally_elected': {},
            'continuing': {
                'B': 2,
                'C': 3,
                'D': 4,
                'E': 5,
                'F': 6
            },
            'excluded': {
                'A': 1
            },
        }

        self.assertEqual(expected_round_1, results_1)
        self.assertFalse(stv.completed())

        results_2 = stv.run_round()
        expected_round_2 = {
            'provisionally_elected': {},
            'continuing': {
                'C': 3,
                'D': 4,
                'E': 5,
                'F': 6
            },
            'excluded': {
                'A': 1,
                'B': 2
            },
        }

        self.assertEqual(expected_round_2, results_2)
        self.assertFalse(stv.completed())

        results_3 = stv.run_round()
        expected_round_3 = {
            'provisionally_elected': {},
            'continuing': {
                'D': 4,
                'E': 5,
                'F': 6
            },
            'excluded': {
                'A': 1,
                'B': 2,
                'C': 3
            },
        }

        self.assertEqual(expected_round_3, results_3)
        self.assertFalse(stv.completed())

        results_4 = stv.run_round()
        expected_round_4 = {
            'provisionally_elected': {
                'F': 6
            },
            'continuing': {
                'E': 5
            },
            'excluded': {
                'A': 1,
                'B': 2,
                'C': 3,
                'D': 4
            },
        }

        self.assertEqual(expected_round_4, results_4)
        self.assertFalse(stv.completed())

        results_5 = stv.run_round()
        expected_round_5 = {
            'provisionally_elected': {
                'E': 5,
                'F': 6
            },
            'continuing': {},
            'excluded': {
                'A': 1,
                'B': 2,
                'C': 3,
                'D': 4
            },
        }

        self.assertEqual(expected_round_5, results_5)
        self.assertTrue(stv.completed())

        final_results = ['E', 'F']
        self.assertEqual(final_results, stv.final_results())

    def test_candidates_should_be_elected_once_there_is_one_per_vacancy(self):
        votes = (
            ('A', 'B'), ('A', 'B'), ('A', 'B'), ('A', 'B'), ('A', 'B'),
            ('B', 'A'), ('B', 'A'), ('B', 'A'), ('B', 'A'), ('B', 'A'),
            ('C')
        )
        candidates = ['A', 'B', 'C', 'D']
        seats = 3

        stv = SingleTransferableVoteScheme(seats, candidates, votes)

        results_1 = stv.run_round()
        expected_round_1 = {
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

        self.assertEqual(expected_round_1, results_1)
        self.assertTrue(stv.completed())

        final_results = ['A', 'B', 'C']
        self.assertEqual(final_results, stv.final_results())
