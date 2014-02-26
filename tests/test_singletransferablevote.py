import unittest
from schemes.singletransferablevote.scheme import SingleTransferableVoteScheme
from fractions import Fraction

class SingeTransferableVoteTest(unittest.TestCase):

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

    def test_reallocate_surplus_votes(self):
        """
        This test is where only one of the candidates has met the quota.
        We are testing that their surplus votes are redistributed correctly.
        """
        votes = [
            ['Green', 'Blue', 'Yellow', 'Red'],
            ['Green', 'Blue', 'Yellow', 'Red'],
            ['Green', 'Blue', 'Yellow', 'Red'],
            ['Green', 'Blue', 'Yellow', 'Red'],
            ['Green', 'Blue', 'Red', 'Yellow'],
            ['Green', 'Blue', 'Red', 'Yellow'],
            ['Green', 'Yellow', 'Red', 'Blue'],
            ['Green', 'Yellow', 'Red', 'Blue'],
            ['Green', 'Yellow', 'Blue', 'Red'],
            ['Red', 'Blue', 'Yellow', 'Green'],
            ['Red', 'Blue', 'Green', 'Yellow'],
            ['Blue', 'Green', 'Red', 'Yellow'],
            ['Blue', 'Yellow', 'Red', 'Green'],
            ['Yellow', 'Blue', 'Red', 'Green'],
            ['Yellow', 'Green', 'Red', 'Blue'],
            ['Yellow', 'Red', 'Green', 'Blue'],
            ['Yellow', 'Blue', 'Green', 'Red'],
        ]
        quota = 6
        totals = {
            'Red': 2,
            'Green': 9,
            'Blue': 2,
            'Yellow': 4,
        }

        expected_reallocated_totals = {
            'Red': 2,
            'Green': 6,
            'Blue': 4,
            'Yellow': 5,
        }

        # TODO passing in None - indicates no validation...
        test_reallocated_totals = SingleTransferableVoteScheme(None, None, votes).reallocate_surplus_votes(quota, totals)

        self.assertEqual(expected_reallocated_totals, test_reallocated_totals)

    def test_reallocate_multiple_surplus_votes_simple(self):
        """
        This is to test the case where more than one candidate has exceeded
        the quota so there are more than one set of surplus votes to reallocate.
        This is the simple case - the reallocated votes go to people who have not
        and will not exceed the quota.
        """
        votes = [
            ['Oranges', 'Pears'],
            ['Oranges', 'Pears'],
            ['Oranges', 'Pears'],
            ['Oranges', 'Lemons'],
            ['Oranges'],
            ['Oranges'],
            ['Oranges'],
            ['Oranges'],
            ['Oranges'],
            ['Apples', 'Pears'],
            ['Apples', 'Lemons'],
            ['Apples'],
            ['Apples'],
            ['Apples'],
            ['Apples'],
            ['Apples'],
        ]

        quota = 5
        totals = {
            'Oranges': 9,
            'Apples': 7,
            'Pears': 0,
            'Lemons': 0,
            'Limes':0,
        }

        expected_reallocated_totals = {
            'Oranges': 5,
            'Apples': 5,
            'Pears': 1 + Fraction(13,21),
            'Lemons': Fraction(46, 63),
            'Limes':0,
        }

        test_reallocated_totals = SingleTransferableVoteScheme(None, None, votes).reallocate_surplus_votes(quota, totals)

        self.assertEqual(expected_reallocated_totals, test_reallocated_totals)

    def test_reallocate_multiple_surplus_votes(self):
        """
        This is to test the case where more than one candidate has exceeded
        the quota so there are more than one set of surplus votes to reallocate.
        This is the more complex case. In this case, Anna has the most votes so
        we process her surplus votes first, but since Norm also has enough votes
        to exceed the quota, Anna's surplus votes are not reallocated to Norm but
        instead to voter's next choices.
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

        quota = 3
        totals = {
            'Dom': 2,
            'Anna': 5,
            'Steve': 0,
            'Norm': 3,
            'Amy': 0,
        }

        expected_reallocated_totals = {
            'Dom': 2 + Fraction(2,5),
            'Anna': 3,
            'Steve': 1 + Fraction(1,5),
            'Norm': 3,
            'Amy': Fraction(2,5),
        }

        test_reallocated_totals = SingleTransferableVoteScheme(None, None, votes).reallocate_surplus_votes(quota, totals)

        self.assertEqual(expected_reallocated_totals, test_reallocated_totals)
