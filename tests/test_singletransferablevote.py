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
            ['Anna', 'Amy', 'Steve', 'Norm', 'Dom'],
            ['Anna', 'Dom', 'Steve', 'Norm'],
            ['Anna', 'Norm', 'Steve', 'Dom', 'Amy'],
            ['Anna', 'Norm', 'Steve'],
            ['Anna', 'Steve', 'Norm', 'Amy', 'Dom'],
            ['Dom', 'Anna', 'Steve', 'Norm', 'Amy'],
            ['Norm', 'Anna', 'Steve'],
            ['Norm', 'Steve', 'Amy', 'Anna', 'Dom'],
            ['Norm', 'Steve', 'Dom', 'Anna', 'Amy'],
            ['Norm', 'Steve', 'Norm', 'Anna'],
        ]

        quota = 3
        totals = {
            'Dom': 1,
            'Anna': 5,
            'Steve': 0,
            'Norm': 4,
            'Amy': 0,
        }

        expected_reallocated_totals = {
            'Dom': 1 + Fraction(2,5),
            'Anna': 3,
            'Steve': 2 + Fraction(1,5),
            'Norm': 3,
            'Amy': Fraction(2,5),
        }

        test_reallocated_totals = SingleTransferableVoteScheme(None, None, votes).reallocate_surplus_votes(quota, totals)

        self.assertEqual(expected_reallocated_totals, test_reallocated_totals)

    def test_reallocate_multiple_quota_met(self):
        """
        This case is where more than one candidate has met the quota. Anna has
        exceeded the quota but Norm has only met the quota. So we want to make
        sure that Anna's surplus votes are not reallocated to Norm.
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

    def test_reallocate_candidate_reaching_quota(self):
        """
        Test when only one candidate reaches the quota initially, but
        reallocation causes another to reach quota and require reallocation.
        So two iterations are required, one to reallocate Galaxy's votes and
        then one to reallocated Mars's now surplus votes.
        Note that the reallocation of Mars's now surplus votes requires their
        devaluing to have been recorded, i.e. it's not 8 at the end of the
        first iteration, it's 11 votes worth 8/11ths each.
        """
        votes = [
            ['Galaxy', 'Mars', 'Crunchie'],
            ['Galaxy', 'Mars', 'Crunchie'],
            ['Galaxy', 'Mars', 'Crunchie'],
            ['Galaxy', 'Mars', 'Crunchie'],
            ['Galaxy', 'Mars', 'Crunchie'],
            ['Galaxy', 'Mars', 'Crunchie'],
            ['Galaxy', 'Mars', 'Crunchie'],
            ['Galaxy', 'Mars', 'Crunchie'],
            ['Galaxy', 'Mars', 'Crunchie'],
            ['Galaxy', 'Mars', 'Crunchie'],
            ['Galaxy', 'Mars', 'Bounty'],
        ]

        quota = 3
        totals = {
            'Mars': 0,
            'Bounty': 0,
            'Galaxy': 11,
            'Crunchie': 0,
        }

        expected_reallocated_totals = {
            'Mars': 3,
            'Bounty': Fraction(5,11),
            'Galaxy': 3,
            'Crunchie': 4 + Fraction(6, 11)
        }

        test_reallocated_totals = SingleTransferableVoteScheme(None, None, votes).reallocate_surplus_votes(quota, totals)

        self.assertEqual(expected_reallocated_totals, test_reallocated_totals)

    def test_candidates_that_meet_quota_is_ordered(self):
        """
        We want the method under test to return a list of candidates whose
        total votes are equal to or exceed the quota, and that list of
        candidates to be ordered, highest votes first.
        This test tests a number of these conditions:
            Mars = 3 (i.e. equal to but not exceeding quota)
            Galaxy = 8 (i.e. exceeding quota)
            That the results are returned in order, highest first
        """
        quota = 3
        totals = {
            'Mars': 3,
            'Bounty': 6,
            'Galaxy': 8,
            'Crunchie': 2,
        }
        expected_candidates_meeting_quota = ['Galaxy', 'Bounty', 'Mars']

        actual_candidates_meeting_quota = SingleTransferableVoteScheme(None, None, None).candidates_that_meet_quota(quota, totals)

        self.assertEqual(expected_candidates_meeting_quota, actual_candidates_meeting_quota)
