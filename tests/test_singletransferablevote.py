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
        
        results_1 = stv.round()
        expected_round_1 = {
            'elected': (('Anna', 3), ('Norm', 3)),
            'hopeful': (('Dom', 2.4), ('Steve', 1.2)),
            'eleminated': (('Amy', 0.4)),
        }
        
        self.assertEqual(expected_round_1, results_1)
        self.assertFalse(stv.completed())
        
        results_2 = stv.round()
        expected_round_2 = {
            'elected': (('Anna', 3), ('Norm', 3)),
            'hopeful': (('Dom', 2.4)),
            'eleminated': (('Steve', 1.6)),
        }
        
        self.assertEqual(expected_round_2, results_2)
        self.assertFalse(stv.completed())
        
        results_3 = stv.round()
        expected_round_3 = {
            'elected': (('Anna', 3), ('Norm', 3), ('Dom', 3+(59/115))),
            'hopeful': (),
            'eleminated': (),
        }
        
        self.assertEqual(expected_round_3, results_3)
        self.assertTrue(stv.completed())
        
        final_results = [
            'Anna',
            'Norm',
            'Dom',
        ]
        self.assertEqual(final_results, stv.final_results())
