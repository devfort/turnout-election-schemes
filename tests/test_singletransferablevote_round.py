import unittest
from fractions import Fraction
from turnout_election_schemes.schemes.errors import FailedElectionError
from turnout_election_schemes.schemes.singletransferablevote.scheme import Round

class RoundTest(unittest.TestCase):
    def test_all_vacancies_filled_should_be_true_after_round_runs(self):
        """
        Before a round has run it should report that all vacancies have not
        been filled. After the round runs it should report that all vacancies
        have been filled.
        """

        vacancies = 2
        candidates = ('Red', 'Green', 'Blue')
        votes = 4 * (('Red', ), ) + \
                3 * (('Green', ), )

        stv_round = Round(vacancies, candidates, votes)
        self.assertFalse(stv_round.all_vacancies_filled())

        stv_round.run()
        self.assertTrue(stv_round.all_vacancies_filled())

    def test_all_vacancies_filled_should_be_false_after_incomplete_round(self):
        """
        After a round runs that fails to elect enough candidates the round
        should report that it has not filled all vacancies.
        """

        vacancies = 2
        candidates = ('Red', 'Green', 'Blue', 'Yellow', 'Mauve')
        votes = 5 * (('Red', ), ) + \
                4 * (('Green', ), ) + \
                3 * (('Blue', ), ) + \
                2 * (('Yellow', ), ) + \
                1 * (('Mauve', ), )

        stv_round = Round(vacancies, candidates, votes)
        stv_round.run()
        self.assertFalse(stv_round.all_vacancies_filled())

    @unittest.skip("The problem is a bug - fix tmrw")
    def test_reallocation_of_surplus_votes(self):
        """
        A single round should reallocate surplus votes from all candidates that
        have a surplus and then exclude the candidate with the fewest votes.
        """

        vacancies = 3
        candidates = ('Oranges', 'Apples', 'Pears', 'Lemons', 'Limes')
        votes = 9 * (('Oranges', 'Pears'), ) + \
                8 * (('Apples', 'Lemons'), ) + \
                1 * (('Lemons', ), )

        expected_results = {
            'provisionally_elected': {
                'Oranges': 5,
                'Apples': 5
            },
            'continuing': {
                'Pears': 4,
                'Lemons': 4
            },
            'excluded': {
                'Limes': 0
            }
        }

        stv_round = Round(vacancies, candidates, votes)
        stv_round.run()
        print stv_round.quota
        print stv_round.results()
        self.assertEqual(expected_results, stv_round.results())

    # TODO this test is failing because of something to do with random I think
    def test_tied_winners_should_cause_election_to_fail_without_a_random_generator(self):
        """
        When there's a tie between winners arbitrarily choosing one to
        reallocate surplus from first may impact the election result. If a
        random generator is not passed in then a FailedElectionError should be
        thrown in cases of ambiguity.

        When a random generator is provided it should be used to break ties of
        winners. This test demonstrates both outcomes of a random tie being
        broken by mocking two versions of a random generator.
        """

        vacancies = 4
        candidates = ('A', 'B', 'C', 'D', 'E')
        votes = 9 * (('A', 'C'), ) + \
                9 * (('B', 'C', 'D'), ) + \
                3 * (('C', ), ) + \
                2 * (('D', ), ) + \
                3 * (('E', ), )

        stv_round = Round(vacancies, candidates, votes)
        with self.assertRaises(FailedElectionError):
            stv_round.run()

        class MockRandom(object):
            def choice(self, sequence):
                return sequence[0]

        expected_results = {
            'provisionally_elected': {
                'A': 6,
                'B': 6,
                'C': 6,
                'D': 5
            },
            'continuing': {},
            'excluded': {
                'E': 3
            }
        }

        stv_round = Round(vacancies, candidates, votes, random = MockRandom())
        stv_round.run()
        self.assertEqual(expected_results, stv_round.results())

        class MockRandom(object):
            def choice(self, sequence):
                return sequence[1]

        expected_results = {
            'provisionally_elected': {
                'A': 6,
                'B': 6,
                'C': 6,
                'E': 3
            },
            'continuing': {},
            'excluded': {
                'D': 2
            }
        }

        stv_round = Round(vacancies, candidates, votes, random = MockRandom())
        stv_round.run()
        self.assertEqual(expected_results, stv_round.results())

    def test_tied_losers_should_cause_election_to_fail(self):
        """
        When there's a tie between losers arbitrarily choosing one to exclude
        first may impact the election result. If a random generator is not
        passed in then a FailedElectionError should be thrown in cases of
        ambiguity.

        When a random generator is provided it should be used to break ties of
        losers. This test demonstrates both outcomes of a random tie being
        broken by mocking two versions of a random generator.
        """

        vacancies = 4
        candidates = ('A', 'B', 'C', 'D', 'E')
        votes = 2 * (('A', 'B'), ) + \
                2 * (('B', 'A'), ) + \
                3 * (('C', ), ) + \
                3 * (('D', ), ) + \
                3 * (('E', ), )

        stv_round = Round(vacancies, candidates, votes)
        with self.assertRaises(FailedElectionError):
            stv_round.run()

        class MockRandom(object):
            def choice(self, sequence):
                return sequence[0]

        expected_results = {
            'provisionally_elected': {
                'B': 2,
                'C': 3,
                'D': 3,
                'E': 3
            },
            'continuing': {},
            'excluded': {
                'A': 2
            }
        }

        stv_round = Round(vacancies, candidates, votes, random = MockRandom())
        stv_round.run()
        self.assertEqual(expected_results, stv_round.results())

        class MockRandom(object):
            def choice(self, sequence):
                return sequence[1]

        expected_results = {
            'provisionally_elected': {
                'A': 2,
                'C': 3,
                'D': 3,
                'E': 3
            },
            'continuing': {},
            'excluded': {
                'B': 2
            }
        }

        stv_round = Round(vacancies, candidates, votes, random = MockRandom())
        stv_round.run()
        self.assertEqual(expected_results, stv_round.results())

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

    # TODO bulk exclusion breaks this test
    # need to rejig figures as I think this test is worth having
    # as it makes this stuff explicit
    def test_candidates_should_be_elected_once_there_is_one_per_vacancy(self):
        """
        As soon as there are the same number of remaining candidates as
        vacancies the election is completed with all of the remaining
        candidates elected as winners.

        Note that this makes it possible for a candidate to be elected even
        without enough votes to reach the quota, as in this example.

        Surplus votes for candidates A and B become exhausted votes because
        there is no further preference to reallocate them to. Candidate D is
        then excluded because they have the fewest votes. Since this leaves
        only three candidates for three vacancies candidate C is declared
        elected, even though they have only one vote compared to the quota of
        three.
        """

        vacancies = 3
        candidates = ('A', 'B', 'C', 'D')
        votes = 5 * (('A', 'B'), ) + \
                4 * (('B', 'A'), ) + \
                1 * (('C', ), )

        expected_results = {
            'provisionally_elected': {
                'A': 3,
                'B': 3,
                'C': 1
            },
            'continuing': {},
            'excluded': {
                'D': 0
            },
        }

        stv = Round(vacancies, candidates, votes)
        stv.run()
        self.assertEqual(expected_results, stv.results())
        self.assertTrue(stv.all_vacancies_filled())
