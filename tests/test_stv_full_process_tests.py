import unittest
from fractions import Fraction
from schemes.errors import FailedElectionError
from schemes.singletransferablevote.scheme import SingleTransferableVoteScheme

class SingleTransferableVoteTest(unittest.TestCase):
    # TODO: this should be a full election test
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

        stv.run_round()

        expected_round_1 = {
            'provisionally_elected': {
                'Anna': 3,
                'Norm': 3,
            },
            'continuing': {
                'Dom': 2 + Fraction(2,5),
                'Steve': 1 + Fraction(1,5),
            },
            'excluded': {
                'Amy': Fraction(2,5),
            },
        }

        self.assertEqual(expected_round_1, stv.round_results())
        self.assertFalse(stv.completed())

        stv.run_round()

        expected_round_2 = {
            'provisionally_elected': {
                'Anna': 3,
                'Norm': 3,
                'Dom': 2 + Fraction(2,5),
            },
            'continuing': { },
            'excluded': {
                'Steve': 1 + Fraction(3,5),
            },
        }

        self.assertEqual(expected_round_2, stv.round_results())
        self.assertTrue(stv.completed())

        final_results = [
            'Anna',
            'Norm',
            'Dom',
        ]
        self.assertEqual(final_results, stv.final_results())

    # TODO: this should become a unit test on Round.quota
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

        stv.run_round()

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

        self.assertEqual(expected_round_1, stv.round_results())
        self.assertFalse(stv.completed())

        stv.run_round()

        expected_round_2 = {
            'provisionally_elected': {},
            'continuing': {
                'C': 3,
                'D': 4,
                'E': 5,
                'F': 6
            },
            'excluded': {
                'B': 2
            },
        }

        self.assertEqual(expected_round_2, stv.round_results())
        self.assertFalse(stv.completed())

        stv.run_round()

        expected_round_3 = {
            'provisionally_elected': {},
            'continuing': {
                'D': 4,
                'E': 5,
                'F': 6
            },
            'excluded': {
                'C': 3
            },
        }

        self.assertEqual(expected_round_3, stv.round_results())
        self.assertFalse(stv.completed())

        stv.run_round()

        expected_round_4 = {
            'provisionally_elected': {
                'F': 6,
                'E': 5
            },
            'continuing': {
            },
            'excluded': {
                'D': 4
            },
        }

        self.assertEqual(expected_round_4, stv.round_results())
        self.assertTrue(stv.completed())

        final_results = ['F', 'E']
        self.assertEqual(final_results, stv.final_results())
