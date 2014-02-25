import unittest
from schemes.majorityjudgement.vote_aggregator import VoteAggregator
from schemes.errors import IncompleteVoteError, InvalidVoteError

class TestVoteAggregator(unittest.TestCase):
    def setUp(self):
        candidates = ('Pizza', 'Chinese', 'Indian', 'Burger')
        number_of_grades = 5

        self.aggregator = VoteAggregator(candidates, number_of_grades)

    def test_simple_aggregation(self):
        # Arrange
        steves_vote   = (0, 4, 2, 4)
        doms_vote     = (1, 3, 3, 4)
        annas_vote    = (4, 1, 0, 4)
        steve_2s_vote = (0, 2, 1, 2)

        all_votes = (steves_vote, doms_vote, annas_vote, steve_2s_vote)

        # Act
        actual_output = self.aggregator.aggregate(all_votes)

        # Assert
        expected_output = (
                ('Pizza',   (2, 1, 0, 0, 1)),
                ('Chinese', (0, 1, 1, 1, 1)),
                ('Indian',  (1, 1, 1, 1, 0)),
                ('Burger',  (0, 0, 1, 0, 3))
                )

        self.assertEqual(expected_output, actual_output)

    def test_noone_chose_top_or_bottom_grade_returns_zeros_for_those_grades(self):
        # Arrange
        steves_vote   = (2, 1, 2, 3)
        doms_vote     = (1, 3, 3, 1)
        annas_vote    = (1, 1, 2, 3)
        steve_2s_vote = (2, 3, 3, 3)

        all_votes = (steves_vote, doms_vote, annas_vote, steve_2s_vote)

        # Act
        actual_output = self.aggregator.aggregate(all_votes)

        # Assert
        expected_output = (
                ('Pizza',   (0, 2, 2, 0, 0)),
                ('Chinese', (0, 2, 0, 2, 0)),
                ('Indian',  (0, 0, 2, 2, 0)),
                ('Burger',  (0, 1, 0, 3, 0)))

        self.assertEqual(expected_output, actual_output)

    def test_no_votes_returns_zeros_for_every_grade(self):
        # Arrange
        all_votes = []

        # Act
        actual_output = self.aggregator.aggregate(all_votes)

        # Assert
        expected_output = (
                ('Pizza',   (0, 0, 0, 0, 0)),
                ('Chinese', (0, 0, 0, 0, 0)),
                ('Indian',  (0, 0, 0, 0, 0)),
                ('Burger',  (0, 0, 0, 0, 0)))

        self.assertEqual(expected_output, actual_output)

    def test_someones_votes_are_incomplete_raises_error(self):
        # Arrange
        steves_vote   = (2, 1, 2, 3)
        doms_vote     = (1, 3, 3, 1)
        annas_vote    = (1, 1, 2) # This person only has 3 preferences listed, 4 are needed.
        steve_2s_vote = (2, 3, 3, 3)

        all_votes = (steves_vote, doms_vote, annas_vote, steve_2s_vote)

        # Act/assert
        with self.assertRaises(IncompleteVoteError):
            self.aggregator.aggregate(all_votes)

    def test_someones_vote_is_too_high_raises_error(self):
        # Arrange
        steves_vote   = (2, 1, 2, 3)
        doms_vote     = (1, 3, 3, 1)
        annas_vote    = (1, 1, 2, 5) # The highest number allowed is 4, this person has said 5
        steve_2s_vote = (2, 3, 3, 3)

        all_votes = (steves_vote, doms_vote, annas_vote, steve_2s_vote)

        # Act/assert
        with self.assertRaises(InvalidVoteError):
            self.aggregator.aggregate(all_votes)

    def test_someones_vote_is_too_low_raises_error(self):
        # Arrange
        steves_vote   = (2, 1, 2, 3)
        doms_vote     = (1, 3, 3, 1)
        annas_vote    = (1, 1, 2, -4) # The lowest number allowed is 0, this person has said -4
        steve_2s_vote = (2, 3, 3, 3)

        all_votes = (steves_vote, doms_vote, annas_vote, steve_2s_vote)

        # Act/assert
        with self.assertRaises(InvalidVoteError):
            self.aggregator.aggregate(all_votes)
