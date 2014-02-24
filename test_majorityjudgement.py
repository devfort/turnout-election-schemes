import unittest
from schemes.majorityjudgement import MajorityJudgement
from schemes.errors import IncompleteVoteError, NoWinnerError


class MajorityJudgementTest(unittest.TestCase):

    def test_basic_small_case(self):
        pizza = ('Pizza', (3,1,1))
        burger = ('Burger', (2,0,3))
        veggie = ('Veggie', (1,2,2))

        input_data = (pizza, burger, veggie)

        expected_output = (pizza, veggie, burger)

        actual_output = MajorityJudgement().sort_candidates(input_data)
        self.assertEqual(expected_output, actual_output)

    def test_basic_larger_case(self):
        chinese = ('Chinese', (26,7,8,6,40,12))
        pizza = ('Pizza', (45,17,4,21,10,2))
        indian = ('Indian', (17,2,33,33,4,10))
        burger = ('Burger', (8,7,26,40,12,6))

        input_data = (chinese, pizza, indian, burger)

        expected_output = (pizza, indian, burger, chinese)

        actual_output = MajorityJudgement().sort_candidates(input_data)
        self.assertEqual(expected_output, actual_output)

    def test_simple_tie_breaker(self):
        pizza = ('Pizza', (1,2,2))   #GAAPP, #GAPP, #GAP
        burger = ('Burger', (2,3,0)) #GGAAA, #GGAA, #GGA
        veggie = ('Veggie', (2,1,2)) #GGAPP, #GGPP, #GGP

        input_data = (pizza, burger, veggie)
        expected_output = (burger, veggie, pizza)

        actual_output = MajorityJudgement().sort_candidates(input_data)
        self.assertEqual(expected_output, actual_output)

    def test_complex_tie_breaker(self):
        rioja = ('Rioja', (2, 1, 6, 2, 2))
        bordeaux = ('Bordeaux', (1, 2, 6, 2, 2))
        tempranillo = ('Tempranillo', (1, 2, 6, 3, 1))

        input_data = (rioja, bordeaux, tempranillo)
        expected = (rioja, tempranillo, bordeaux)

        self.assertEqual(expected, MajorityJudgement().sort_candidates(input_data))

    def test_incomplete_vote(self):
        pizza = ('Pizza', (3,1,1))
        burger = ('Burger', (2,0))
        veggie = ('Veggie', (1,2,2))

        with self.assertRaises(IncompleteVoteError):
            input_data = (pizza, burger, veggie)

    #Good Steve
    def test_even_number_of_voters_different_medians(self):
        """
        In this case, there are 6 voters.

        If we used the 3rd item for the median, result order would be red, blue, green.
        But, if we use the 4th item for the median, result would be   blue, red, green.

        The second is the *correct* way.
        """
        red = ('Red party', (3,0,3))     #GGGPPP
        blue = ('Blue party', (2,2,2))   #GGAAPP
        green = ('Green party', (2,0,4)) #GGPPPP

        input_data = (red, blue, green)
        expected_output = (blue, red, green)

        actual_output = MajorityJudgement().sort_candidates(input_data)
        self.assertEqual(expected_output, actual_output)

    def test_two_identical_winners(self):
        smith = ('L. Smith', (3, 8, 5, 7, 2))
        jones = ('Q. Jones', (0, 3, 2, 9, 11))
        rogers = ('P. Rogers', (3, 8, 5, 7, 2))

        input_data = (smith, jones, rogers)

        with self.assertRaises(NoWinnerError):
            MajorityJudgement().sort_candidates(input_data)

    #Steve 2
    def test_two_identical_losers(self):
        castle = ('Castle', (1,2,2))               #GAAPP
        fort = ('Fort', (5,0,0))                   #GGGGG
        country_house = ('Country house', (1,2,2)) #GAAPP

        input_data = (castle, fort, country_house)
        expected_output = (fort, castle, country_house)

        actual_output = MajorityJudgement().sort_candidates(input_data)
        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main()
