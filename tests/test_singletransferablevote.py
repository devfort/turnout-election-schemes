import unittest
from schemes.singletransferablevote.scheme import *
from fractions import Fraction

class SingeTransferableVoteTest(unittest.TestCase):

    def test_quota(self):
        """
        Tests a simple quota case. Quota should be 10 / (3 + 1) + 1 => 3
        """

        votes = [
            ['Red', 'Blue', 'Green'] for i in range(0,10)
        ]

        quota = Round(3, ('Red', 'Blue', 'Green'), votes).quota
        self.assertEqual(3, quota)

    def test_calculate_initial_totals(self):
        """
        Tests the initial assignment of votes
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

        results = Round(seats, candidates, votes).results()

        expected_totals = {
            'Dom': 2,
            'Anna': 5,
            'Norm': 3,
            'Steve': 0,
            'Amy': 0,
        }
        self.assertEqual(expected_totals, results['continuing'])

    def test_provisionally_elect_candidates(self):
        """
        Tests that candidates at or above the quota are marked as provisionally elected
        """

        votes = (
            ('A', ), ('A', ), ('A', ), ('A', ),
            ('B', ), ('B', ), ('B', ),
            ('C', )
        )
        candidates = ('A', 'B', 'C')
        vacancies = 2

        stv_round = Round(vacancies, candidates, votes)
        stv_round._provisionally_elect_candidates()
        results = stv_round.results()

        expected_totals = {
            'A': 4,
            'B': 3
        }

        self.assertEqual(expected_totals, results['provisionally_elected'])

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
        candidates = ('Green', 'Blue', 'Yellow', 'Red')
        vacancies = 2

        expected_reallocated_totals = {
            'provisionally_elected': {
                'Green': 6
            },
            'continuing': {
                'Red': 2,
                'Blue': 4,
                'Yellow': 5
            },
            'excluded': {}
        }

        stv_round = Round(vacancies, candidates, votes)
        stv_round._provisionally_elect_candidates()
        stv_round._reassign_votes_from_candidate_with_highest_surplus()

        self.assertEqual(expected_reallocated_totals, stv_round.results())

    def test_exhausted_votes_are_not_reallocated(self):
        """
        A vote with no further preferences for other candidates shouldn't be
        reallocated. In this example Anna starts with 9 votes which means she
        has 3 surplus votes above the quota of 6. Second preference choices for
        Anna's votes are split equally between no preference, Steve and Norm.
        Steve and Norm should get 1 vote each and the final vote should
        disappear.
        """

        votes = (
            ('Anna', ), ('Anna', ), ('Anna', ),
            ('Anna', 'Steve'), ('Anna', 'Steve'), ('Anna', 'Steve'),
            ('Anna', 'Norm'), ('Anna', 'Norm'), ('Anna', 'Norm'),
            ('Steve', ), ('Steve', ), ('Steve', ), ('Steve', ),
            ('Norm', ), ('Norm', ), ('Norm', ),
        )

        candidates = ('Anna', 'Steve', 'Norm')
        vacancies = 2

        expected_results = {
            'provisionally_elected': {
                'Anna': 6
            },
            'continuing': {
                'Steve': 5,
                'Norm': 4
            },
            'excluded': {}
        }

        stv_round = Round(vacancies, candidates, votes)
        stv_round._provisionally_elect_candidates()
        stv_round._reassign_votes_from_candidate_with_highest_surplus()

        self.assertEqual(expected_results, stv_round.results())

    def test_reallocate_multiple_surplus_votes_simple(self):
        """
        This is to test the case where more than one candidate has exceeded
        the quota so there are more than one set of surplus votes to reallocate.
        This is the simple case - the reallocated votes go to people who have not
        and will not exceed the quota.
        i.e. testing that it does the right thing, the right number of times
        Tests a full round so includes excluded candidates.
        """
        votes = [
            ['Oranges', 'Pears'],
            ['Oranges', 'Pears'],
            ['Oranges', 'Pears'],
            ['Oranges', 'Pears'],
            ['Oranges', 'Pears'],
            ['Oranges', 'Pears'],
            ['Oranges', 'Pears'],
            ['Oranges', 'Pears'],
            ['Oranges', 'Pears'],
            ['Apples', 'Lemons'],
            ['Apples', 'Lemons'],
            ['Apples', 'Lemons'],
            ['Apples', 'Lemons'],
            ['Apples', 'Lemons'],
            ['Apples', 'Lemons'],
            ['Apples', 'Lemons'],
        ]

        candidates = ['Oranges', 'Apples', 'Pears', 'Lemons', 'Limes']
        vacancies = 3

        expected_totals = {
            'provisionally_elected': {
                'Oranges': 5,
                'Apples': 5,
            },
            'continuing': {
                'Pears': 4,
                'Lemons': 2,
            },
            'excluded': {
                'Limes': 0
            }
        }

        stv_round = Round(vacancies, candidates, votes)
        stv_round.run()

        self.assertEqual(expected_totals, stv_round.results())

    def test_reallocate_fractional_votes(self):
        """
        This is the case where a candidates second preferences are split
        between other candidates so fractions of votes are reallocated
        """
        votes = [
            ['Amy', 'James'],
            ['Amy', 'James'],
            ['Amy', 'James'],
            ['Amy', 'James'],
            ['Amy', 'David'],
            ['Amy', 'David'],
            ['Amy', 'David'],
        ]
        candidates = ['Amy', 'James', 'David']
        vacancies = 2

        expected_result = {
            'provisionally_elected': {
                'Amy': 3
            },
            'continuing': {
                'James': Fraction(16,7),
                'David': Fraction(12,7)
            },
            'excluded': {}
        }

        stv_round = Round(vacancies, candidates, votes)
        stv_round._provisionally_elect_candidates()
        stv_round._reassign_votes_from_candidate_with_highest_surplus()

        self.assertEqual(expected_result, stv_round.results())

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

    def test_candidates_with_surplus_is_ordered(self):
        """
        We want the method under test to return a list of candidates whose
        total votes exceed the quota, and that list of candidates to be
        ordered, highest votes first.

        With 3 seats available and the following votes:

            Mars: 3
            Bounty: 6
            Galaxy: 8
            Crunchie: 2

        We have a quota of 5 and expect Galaxy and Bounty to be returned as
        candidates with surplus, in that order.
        """

        votes = (
            ('Mars', ), ('Mars', ), ('Mars', ),
            ('Bounty', ), ('Bounty', ), ('Bounty', ), ('Bounty', ), ('Bounty', ), ('Bounty', ),
            ('Galaxy', ), ('Galaxy', ), ('Galaxy', ), ('Galaxy', ), ('Galaxy', ), ('Galaxy', ), ('Galaxy', ), ('Galaxy', ),
            ('Crunchie', ), ('Crunchie', )
        )
        candidates = ('Mars', 'Bounty', 'Galaxy', 'Crunchie')
        seats = 3

        expected_candidates = ['Galaxy', 'Bounty']

        stv_round = Round(seats, candidates, votes)
        stv_round._provisionally_elect_candidates()
        candidates_with_surplus = map(
            lambda c: c.candidate_id,
            stv_round._candidates_with_surplus()
        )

        self.assertEqual(expected_candidates, candidates_with_surplus)

    def test_exclude_candidate_with_fewest_votes(self):
        """
        Check that the method moves the candidate with the fewest vote total is
        moved to excluded
        """

        votes = (
            ('Chocolate', ), ('Chocolate', ), ('Chocolate', ), ('Chocolate', ),
            ('Fruit', ), ('Fruit', ),
            ('Vegetables', )
        )

        candidates = ('Vegetables', 'Chocolate', 'Fruit')
        vacancies = 2

        expected_results = {
            'provisionally_elected': {},
            'continuing': {
                'Chocolate': 4,
                'Fruit': 2
            },
            'excluded': {
                'Vegetables': 1
            }
        }

        stv_round = Round(vacancies, candidates, votes)
        stv_round._exclude_candidate_with_fewest_votes()

        self.assertEqual(expected_results, stv_round.results())
