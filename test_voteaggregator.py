import unittest
from schemes.majorityjudgement import VoteAggregator

class TestVoteAggregator(unittest.TestCase):
    def test_simple_aggregation(self):
        #This vote has 5 levels, ranging from worst (0) to best (4)

        # NOTE: The individual user votes use grades that start at 0 for worst,
        # and increase for better things (in this case 4 is the best)

        # However, the aggregated output lists the number of the *best* grade
        # first, going down in good-ness until the number of the *worst* grade
        # last.
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

        actual_output = VoteAggregator().aggregate(candidates, all_votes, 5)

        self.assertEqual(expected_output, actual_output)

    def test_noone_chose_some_of_the_grades(self):
        #This vote has 5 levels, ranging from worst (0) to best (4)
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

        actual_output = VoteAggregator().aggregate(candidates, all_votes, 5)

        self.assertEqual(expected_output, actual_output)
if __name__ == '__main__':
    unittest.main()
