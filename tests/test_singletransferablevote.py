import unittest
from schemes.singletransferablevote.scheme import SingleTransferableVoteScheme

class SingeTransferableVoteTest(unittest.TestCase):
    """
    """
    def test_basic_small_case(self):
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
            'hopeful': (('Dom', 2.4), ('Steve', 1.2)),
            'eliminated': (('Amy', 0.4)),
        }
        
        self.assertEqual(expected_round_1, results_1)
        self.assertFalse(stv.completed())
        
        results_2 = stv.run_round()
        expected_round_2 = {
            'elected': (('Anna', 3), ('Norm', 3)),
            'hopeful': (('Dom', 2.4)),
            'eliminated': (('Steve', 1.6)),
        }
        
        self.assertEqual(expected_round_2, results_2)
        self.assertFalse(stv.completed())
        
        results_3 = stv.run_round()
        expected_round_3 = {
            'elected': (('Anna', 3), ('Norm', 3), ('Dom', 3+(59/115))),
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

    def test_quota(self):
        seats = 3
        votes = [
            ['Red', 'Blue', 'Green'] for i in range(0,10)
        ]

        expected_quota = 3
        actual_quota = SingleTransferableVoteScheme(seats, 3, votes).calculate_quota(seats, votes)
        self.assertEqual(expected_quota, actual_quota)

    def test_calculate_totals(self):
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

        totals = SingleTransferableVoteScheme(seats, candidates, votes).calculate_totals()

        expected_totals = {
            'Dom': 2,
            'Anna': 5,
            'Norm': 3,
            'Steve': 0,
            'Amy': 0,
        }
        self.assertEqual(expected_totals, totals)
