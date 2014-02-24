import unittest
from schemes.majorityjudgement import VoteAggregator
from schemes.errors import IncompleteVoteError, InvalidVoteError

class TestVoteAggregator(unittest.TestCase):
    def test_simple_aggregation(self):
        #This vote has 5 levels, ranging from worst (0) to best (4)

        candidates = ('Pizza', 'Chinese', 'Indian', 'Burger')

        steves_vote   = (0, 4, 2, 4)
        doms_vote     = (1, 3, 3, 4)
        annas_vote    = (4, 1, 0, 4)
        steve_2s_vote = (0, 2, 1, 2)

        all_votes = (steves_vote, doms_vote, annas_vote, steve_2s_vote)

        expected_output = (
                ('Pizza',   (1, 0, 0, 1, 2)),
                ('Chinese', (1, 1, 1, 1, 0)),
                ('Indian',  (0, 1, 1, 1, 1)),
                ('Burger',  (3, 0, 1, 0, 0)))

        actual_output = VoteAggregator(candidates, 5).aggregate(all_votes)

        self.assertEqual(expected_output, actual_output)

    def test_noone_chose_top_or_bottom_grade_returns_zeros_for_those_grades(self):
        candidates = ('Pizza', 'Chinese', 'Indian', 'Burger')

        steves_vote   = (2, 1, 2, 3)
        doms_vote     = (1, 3, 3, 1)
        annas_vote    = (1, 1, 2, 3)
        steve_2s_vote = (2, 3, 3, 3)

        all_votes = (steves_vote, doms_vote, annas_vote, steve_2s_vote)

        expected_output = (
                ('Pizza',   (0, 0, 2, 2, 0)),
                ('Chinese', (0, 2, 0, 2, 0)),
                ('Indian',  (0, 2, 2, 0, 0)),
                ('Burger',  (0, 3, 0, 1, 0)))

        actual_output = VoteAggregator(candidates, 5).aggregate(all_votes)

        self.assertEqual(expected_output, actual_output)

    def test_no_votes_returns_zeros_for_every_grade(self):
        candidates = ('Pizza', 'Chinese', 'Indian', 'Burger')
        all_votes = []

        expected_output = (
                ('Pizza',   (0, 0, 0, 0, 0)),
                ('Chinese', (0, 0, 0, 0, 0)),
                ('Indian',  (0, 0, 0, 0, 0)),
                ('Burger',  (0, 0, 0, 0, 0)))

        actual_output = VoteAggregator(candidates, 5).aggregate(all_votes)

        self.assertEqual(expected_output, actual_output)

    def test_someones_votes_are_incomplete_raises_error(self):
        candidates = ('Pizza', 'Chinese', 'Indian', 'Burger')

        steves_vote   = (2, 1, 2, 3)
        doms_vote     = (1, 3, 3, 1)
        annas_vote    = (1, 1, 2) # This person only has 3 preferences listed, 4 are needed.
        steve_2s_vote = (2, 3, 3, 3)

        all_votes = (steves_vote, doms_vote, annas_vote, steve_2s_vote)

        with self.assertRaises(IncompleteVoteError):
            VoteAggregator(candidates, 5).aggregate(all_votes)

    def test_someones_vote_is_too_high_raises_error(self):
        candidates = ('Pizza', 'Chinese', 'Indian', 'Burger')

        steves_vote   = (2, 1, 2, 3)
        doms_vote     = (1, 3, 3, 1)
        annas_vote    = (1, 1, 2, 5) # The highest number allowed is 4, this person has said 5
        steve_2s_vote = (2, 3, 3, 3)

        all_votes = (steves_vote, doms_vote, annas_vote, steve_2s_vote)

        with self.assertRaises(InvalidVoteError):
            VoteAggregator(candidates, 5).aggregate(all_votes)

    def test_someones_vote_is_too_low_raises_error(self):
        candidates = ('Pizza', 'Chinese', 'Indian', 'Burger')

        steves_vote   = (2, 1, 2, 3)
        doms_vote     = (1, 3, 3, 1)
        annas_vote    = (1, 1, 2, -4) # The lowest number allowed is 0, this person has said -4
        steve_2s_vote = (2, 3, 3, 3)

        all_votes = (steves_vote, doms_vote, annas_vote, steve_2s_vote)

        with self.assertRaises(InvalidVoteError):
            VoteAggregator(candidates, 5).aggregate(all_votes)

if __name__ == '__main__':
    unittest.main()
