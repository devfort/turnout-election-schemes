import unittest
from fractions import Fraction
from schemes.errors import FailedElectionError
from schemes.singletransferablevote.scheme import Round

class RoundTest(unittest.TestCase):
    def test_all_vacancies_filled(self):
        """
        Test that Round can report when all the vacancies have been filled
        """
        candidates = ['Red', 'Green', 'Blue']
        vacancies = 3
        votes = ()
        stv_round = Round(vacancies, candidates, votes)
        stv_round.run()

        self.assertTrue(stv_round.all_vacancies_filled())

    def test_all_vacancies_not_filled(self):
        """
        Test that Round can report when all the vacancies haven't been filled
        """
        candidates = ['Red', 'Green', 'Blue', 'Yellow', 'Mauve']
        vacancies = 2
        votes = (
            ('Red',),
            ('Red',),
            ('Red',),
            ('Red',),
            ('Red',),
            ('Green',),
            ('Green',),
            ('Green',),
            ('Green',),
            ('Blue',),
            ('Blue',),
            ('Blue',),
            ('Yellow',),
            ('Yellow',),
            ('Mauve',),
        )
        stv_round = Round(vacancies, candidates, votes)
        stv_round.run()

        self.assertFalse(stv_round.all_vacancies_filled())

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

    def test_reallocate_multiple_surplus_votes(self):
        """
        This is to test the case where more than one candidate has exceeded
        the quota so there are more than one set of surplus votes to reallocate.
        This is the more complex case. In this case, Anna has the most votes so
        we process her surplus votes first, but since Norm also has enough votes
        to exceed the quota, Anna's surplus votes are not reallocated to Norm but
        instead to voter's next choices.

        Initial total votes are:
            'Dom': 1,
            'Anna': 5,
            'Steve': 0,
            'Norm': 4,
            'Amy': 0,

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
        candidates = ['Anna', 'Amy', 'Steve', 'Norm', 'Dom']
        vacancies = 3

        expected_results = {
            'provisionally_elected': {
                'Anna': 3,
                'Norm': 3
            },
            'continuing': {
                'Dom': 1 + Fraction(2,5),
                'Steve': 2 + Fraction(1,5),
            },
            'excluded': {
                'Amy': Fraction(2,5),
            }
        }

        stv_round = Round(vacancies, candidates, votes)
        stv_round.run()

        self.assertEqual(expected_results, stv_round.results())

    def test_reallocate_multiple_quota_met(self):
        """
        This case is where more than one candidate has met the quota. Anna has
        exceeded the quota but Norm has only met the quota. So we want to make
        sure that Anna's surplus votes are not reallocated to Norm.
        Initial totals:
            'Dom': 2,
            'Anna': 5,
            'Steve': 0,
            'Norm': 3,
            'Amy': 0,
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
        candidates = ['Norm', 'Anna', 'Dom', 'Amy', 'Steve']
        vacancies = 3

        stv_round = Round(vacancies, candidates, votes)
        stv_round.run()

        expected_results = {
            'provisionally_elected': {
                'Anna': 3,
                'Norm': 3
            },
            'continuing': {
                'Dom': 2 + Fraction(2,5),
                'Steve': 1 + Fraction(1,5),
            },
            'excluded': {
                'Amy': Fraction(2,5),
            }
        }

        self.assertEqual(expected_results, stv_round.results())

    def test_tied_winners_should_cause_election_to_fail(self):
        votes = (
            ('A', 'C'), ('A', 'C'), ('A', 'C'), ('A', 'C'), ('A', 'C'),
            ('B', 'C'), ('B', 'C'), ('B', 'C'), ('B', 'C'), ('B', 'C'),
        )
        candidates = ['A', 'B', 'C', 'D', 'E']
        vacancies = 3

        stv_round = Round(vacancies, candidates, votes)

        with self.assertRaises(FailedElectionError):
            stv_round.run()

    def test_tied_losers_should_cause_election_to_fail(self):
        votes = (
            ('A', 'C'), ('A', 'D'),
            ('B', 'E'), ('B', 'E'),
            ('C', ), ('C', ), ('C', ),
            ('D', ), ('D', ), ('D', ),
            ('E', ), ('E', ), ('E', ),
        )
        candidates = ['A', 'B', 'C', 'D', 'E']
        vacancies = 3

        stv_round = Round(vacancies, candidates, votes)

        with self.assertRaises(FailedElectionError):
            stv_round.run()

    #@unittest.skip('bulk elimination functionality not yet written')
    def test_bulk_eliminiation_resolves_tied_loser_failures(self):
        votes = (
            ('A', 'D'), ('A', 'D'),
            ('B', 'E'), ('B', 'E'),
            ('C', 'F'), ('C', 'F'), ('C', 'F'),
            ('D', ), ('D', ), ('D', ), ('D', ), ('D', ), ('D', ), ('D', ), ('D', ),
            ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ), ('E', ),
            ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', ), ('F', )
        )
        candidates = ['A', 'B', 'C', 'D', 'E', 'F']
        vacancies = 2

        stv_round = Round(vacancies, candidates, votes)

        stv_round.run()

        expected_results = {
            'provisionally_elected': {},
            'continuing': {
                'D': 8,
                'E': 12,
                'F': 13
            },
            'excluded': {
                'A': 2,
                'B': 2,
                'C': 3
            },
        }

        self.assertEqual(expected_results, stv_round.results())

    def test_candidates_should_be_elected_once_there_is_one_per_vacancy(self):
        votes = (
            ('A', 'B'), ('A', 'B'), ('A', 'B'), ('A', 'B'), ('A', 'B'), ('A', 'B'),
            ('B', 'A'), ('B', 'A'), ('B', 'A'), ('B', 'A'),
            ('C')
        )
        candidates = ['A', 'B', 'C', 'D']
        vacancies = 3

        expected_results = {
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

        stv = Round(vacancies, candidates, votes)
        stv.run()

        self.assertEqual(expected_results, stv.results())
        self.assertTrue(stv.all_vacancies_filled())
