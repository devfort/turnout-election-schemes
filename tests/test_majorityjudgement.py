import unittest
from schemes.majorityjudgement.scheme import MajorityJudgementScheme
from schemes.errors import IncompleteVoteError, NoWinnerError

class MajorityJudgementTest(unittest.TestCase):
    """
    Note the endian-ness of the votes - they go in INCREASING order of good-ness
    i.e. (1,1,3) means 1 vote for Poor, 1 vote for Acceptable and 3 votes for good.
    """
    def test_basic_small_case(self):
        pizza = ('Pizza', (1,1,3))
        burger = ('Burger', (3,0,2))
        veggie = ('Veggie', (2,2,1))

        input_data = (pizza, burger, veggie)

        expected_output = (pizza, veggie, burger)

        actual_output = MajorityJudgementScheme().sort_candidates(input_data)
        self.assertEqual(expected_output, actual_output)

    def test_basic_larger_case(self):
        chinese = ('Chinese', (12,40,6,8,7,26))
        pizza = ('Pizza', (2,10,21,4,17,45))
        indian = ('Indian', (10,4,33,33,2,17))
        burger = ('Burger', (6,12,40,26,7,8))

        input_data = (chinese, pizza, indian, burger)

        expected_output = (pizza, indian, burger, chinese)

        actual_output = MajorityJudgementScheme().sort_candidates(input_data)
        self.assertEqual(expected_output, actual_output)

    def test_simple_tie_breaker(self):
        pizza = ('Pizza', (2,2,1))   #PPAAG, PPAG, PAG
        burger = ('Burger', (0,3,2)) #AAAGG, AAGG, AGG
        veggie = ('Veggie', (2,1,2)) #PPAGG, PPGG, PGG

        input_data = (pizza, burger, veggie)
        expected_output = (burger, veggie, pizza)

        actual_output = MajorityJudgementScheme().sort_candidates(input_data)
        self.assertEqual(expected_output, actual_output)

    def test_complex_tie_breaker(self):
        rioja = ('Rioja', (2, 2, 6, 1, 2))               #PPAAGGGGGGVEE, PPEE
        bordeaux = ('Bordeaux', (2, 2, 6, 2, 1))         #PPAAGGGGGGVVE, PPVE
        tempranillo = ('Tempranillo', (1, 3, 6, 2, 1))   #PAAAGGGGGGVVE, PAVE

        input_data = (rioja, bordeaux, tempranillo)
        expected = (tempranillo, rioja, bordeaux)

        self.assertEqual(expected, MajorityJudgementScheme().sort_candidates(input_data))

    def test_incomplete_vote(self):
        """
        We are expecting the input data to have votes for each of the candidates
        (i.e. any padding with 0 or defaulting to 'reject' should happen before
        it gets to us. If the data is not complete in this way, we raise an
        IncompleteVoteError.
        """
        pizza = ('Pizza', (3,1,1))
        burger = ('Burger', (2,0))
        veggie = ('Veggie', (1,2,2))

        input_data = (pizza, burger, veggie)

        with self.assertRaises(IncompleteVoteError):
            MajorityJudgementScheme().sort_candidates(input_data)

    #Good Steve
    def test_even_number_of_voters_different_medians(self):
        """
        In this case, there are 6 voters.

        If we used the 4th item for the median, result order would be red, blue, green.
        But, if we use the 3th item for the median, result would be   blue, red, green.

        The second is the *correct* way.
        """
        red = ('Red party', (3,0,3))     #PPPGGG
        blue = ('Blue party', (2,2,2))   #PPAAGG
        green = ('Green party', (4,0,2)) #PPPPGG

        input_data = (red, blue, green)
        expected_output = (blue, red, green)

        actual_output = MajorityJudgementScheme().sort_candidates(input_data)
        self.assertEqual(expected_output, actual_output)

    def test_two_identical_winners(self):
        """
        When the two highest ranked candidates have identical vote
        distributions we cannot pick a winner and an exception should be
        raised.
        """
        smith = ('L. Smith', (2, 7, 5, 8, 3))
        jones = ('Q. Jones', (11, 9, 2, 3, 0))
        rogers = ('P. Rogers', (2, 7, 5, 8, 3))

        input_data = (smith, jones, rogers)

        with self.assertRaises(NoWinnerError):
            MajorityJudgementScheme().sort_candidates(input_data)

    #Steve 2
    def test_two_identical_losers(self):
        castle = ('Castle', (2,2,1))               #PPAAG
        fort = ('Fort', (0,0,5))                   #GGGGG
        country_house = ('Country house', (2,2,1)) #PPAAG

        input_data = (castle, fort, country_house)
        expected_output = (fort, castle, country_house)

        actual_output = MajorityJudgementScheme().sort_candidates(input_data)
        self.fail("TODO: Sort this test and implementation out - we need to do something better when there are two losers")
