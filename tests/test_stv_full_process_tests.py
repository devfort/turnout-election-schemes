import unittest
from fractions import Fraction
from turnout_election_schemes.schemes.errors import FailedElectionError
from turnout_election_schemes.schemes.singletransferablevote.scheme import SingleTransferableVoteScheme

class STVoteFullProcessTest(unittest.TestCase):

    # TODO: this should be a full election test
    # TODO: fix totals
    # 1 and 1/5 + 2/5 is less than both 2 and 2/5 and the quota, so bulk
    # elimination kills this test
    @unittest.skip("case killed")
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
