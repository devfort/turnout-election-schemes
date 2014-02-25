import unittest
from schemes.singletransferablevote.scheme import SingleTransferableVoteScheme
from fractions import Fraction

class SingeTransferableVoteTest(unittest.TestCase):
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
            'elected': (('Anna', 3), ('Norm', 3)),
            'hopeful': (('Dom', 2 + Fraction(2,5)), ('Steve', 1 + Fraction(1,5))),
            'eliminated': (('Amy', Fraction(2,5))),
        }

        self.assertEqual(expected_round_1, results_1)
        self.assertFalse(stv.completed())

        results_2 = stv.run_round()
        expected_round_2 = {
            'elected': (('Anna', 3), ('Norm', 3)),
            'hopeful': (('Dom', 2 + Fraction(2,5))),
            'eliminated': (('Steve', 1 + Fraction(3,5))),
        }

        self.assertEqual(expected_round_2, results_2)
        self.assertFalse(stv.completed())

        results_3 = stv.run_round()
        expected_round_3 = {
            'elected': (('Anna', 3), ('Norm', 3), ('Dom', 3 + Fraction (59,115))),
            'hopeful': (),
            'eliminated': (),
        }

        self.assertEqual(expected_round_3, results_3)
        self.assertTrue(stv.completed())

        final_results = [
            'Anna',
            'Norm',
            'Dom',
        ]
        self.assertEqual(final_results, stv.final_results())
