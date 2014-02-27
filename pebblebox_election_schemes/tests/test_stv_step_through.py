import unittest
from fractions import Fraction
from schemes.singletransferablevote.scheme import Round

class STVStepThroughTest(unittest.TestCase):

    def test_reallocate_candidate_reaching_quota(self):
        """
        This test steps through the run round algorithm, demonstrating
        each step.

        Only one candidate reaches the quota initially, but reallocation
        causes another to reach quota and require reallocation of their now
        surplus votes.

        Note that this reallocation of Mars's now surplus votes requires their
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
        vacancies = 3
        candidates = ['Mars', 'Bounty', 'Galaxy', 'Crunchie']

        # At this stage, we have calculated initial totals but
        # done no more work with the votes
        stv_round = Round(vacancies, candidates, votes)

        initial_totals = {
            'provisionally_elected': {},
            'continuing': {
                'Mars': 0,
                'Bounty': 0,
                'Galaxy': 11,
                'Crunchie': 0,
            },
            'excluded': {}
        }

        self.assertEqual(initial_totals, stv_round.results())

        # Now we run the first pass of calculating which
        # candidates are provisionally elected
        stv_round._provisionally_elect_candidates()

        first_provisional_election_totals = {
            'provisionally_elected': {
                'Galaxy': 11,
            },
            'continuing': {
                'Mars': 0,
                'Bounty': 0,
                'Crunchie': 0,
            },
            'excluded': {}
        }

        self.assertEqual(first_provisional_election_totals, stv_round.results())

        # Now we reassign Galaxy's surplus votes to the
        # next preferences of votes for Galaxy.
        # Note that the 8 for Mars is actually 11 votes each worth 8/11ths.
        stv_round._reassign_votes_from_candidate_with_highest_surplus()

        first_reallocation_totals = {
            'provisionally_elected': {
                'Galaxy': 3,
            },
            'continuing': {
                'Mars': 8,
                'Bounty': 0,
                'Crunchie': 0,
            },
            'excluded': {}
        }

        self.assertEqual(first_reallocation_totals, stv_round.results())

        # After reallocation, we run a provisional election again to see if any
        # new candidates have reached the quota
        stv_round._provisionally_elect_candidates()

        second_provisional_election_totals = {
            'provisionally_elected': {
                'Galaxy': 3,
                'Mars': 8,
            },
            'continuing': {
                'Bounty': 0,
                'Crunchie': 0,
            },
            'excluded': {}
        }

        self.assertEqual(second_provisional_election_totals, stv_round.results())

        # Now Mars has reached the quota, we need to reallocate
        # Mars's surplus votes to the next preferences of votes
        # for Mars.
        # However, votes that have been allocated to Mars from Galaxy
        # are not worth 1, they are worth 8/11 because of their
        # previous reallocation from Galaxy.
        stv_round._reassign_votes_from_candidate_with_highest_surplus()

        second_reallocation_totals = {
            'provisionally_elected': {
                'Galaxy': 3,
                'Mars': 3,
            },
            'continuing': {
                'Bounty': Fraction(5,11),
                'Crunchie': 4 + Fraction(6, 11)
            },
            'excluded': {}
        }

        self.assertEqual(second_reallocation_totals, stv_round.results())

        # We now provisonally elect candidates again to see if anyone else has
        # reached the quota - Crunchie has
        stv_round._provisionally_elect_candidates()

        third_provisional_election_total = {
            'provisionally_elected': {
                'Galaxy': 3,
                'Mars': 3,
                'Crunchie': 4 + Fraction(6, 11)
            },
            'continuing': {
                'Bounty': Fraction(5,11),
            },
            'excluded': {}
        }

        self.assertEqual(third_provisional_election_total, stv_round.results())

        # Now that we have three provisionally elected candidates for the three
        # vacancies, the election is over
        self.assertTrue(stv_round.all_vacancies_filled())
