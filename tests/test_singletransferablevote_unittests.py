import unittest
from schemes.singletransferablevote.scheme import *
from fractions import Fraction

class SingeTransferableVoteTest(unittest.TestCase):

    # Moved from full test - should be unit test
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

        expected_totals = {
            'provisionally_elected': {
                'A': 4,
                'B': 3
            },
            'continuing': {
                'C': 1
            },
            'excluded': {}
        }

        self.assertEqual(expected_totals, stv_round.results())

    def test_provisionally_elect_candidates_auto_fills_vacancies(self):
        """
        If there are as many remaining vacancies as remaining candidates then
        all remaining candidates should be elected even if they don't meet the
        quota.

        In this example, the quota is 3 votes and we expected candidate C to be
        elected even though they only have 2 votes.
        """

        votes = (
            ('A', ), ('A', ), ('A', ), ('A', ),
            ('B', ), ('B', ), ('B', ),
            ('C', ), ('C', )
        )
        candidates = ('A', 'B', 'C')
        vacancies = 3

        stv_round = Round(vacancies, candidates, votes)
        stv_round._provisionally_elect_candidates()

        expected_totals = {
            'provisionally_elected': {
                'A': 4,
                'B': 3,
                'C': 2
            },
            'continuing': {
            },
            'excluded': {}
        }

        self.assertEqual(expected_totals, stv_round.results())

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

    def test_elected_candidates_returns_the_correct_order(self):
        """
        Check that candidates with more votes are returned ahead of candidates
        with fewer votes
        """

        vacancies = 2
        candidates = ('Back Bacon', 'Streaky Bacon', 'Peanut')
        votes = (
            ('Peanut',),
            ('Back Bacon',), ('Back Bacon',), ('Back Bacon',),
            ('Streaky Bacon',), ('Streaky Bacon',), ('Streaky Bacon',), ('Streaky Bacon',),
        )

        expected_order = ['Streaky Bacon', 'Back Bacon']

        stv_round = Round(vacancies, candidates, votes)
        stv_round._provisionally_elect_candidates()

        self.assertEqual(expected_order, stv_round.elected_candidates())
