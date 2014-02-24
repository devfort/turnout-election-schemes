import unittest
from schemes.majorityjudgement import MajorityJudgement

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

    #Good Steve
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

    #Anna
    def test_incomplete_vote(self):
        pass

    #Good Steve
    def test_even_number_of_voters_different_medians(self):
        """
        In this case, there are 6 voters.

        If we used the 3rd item for the median, result order would be pizza, burger, veggie.
        But, if we use the 4th item for the median, result would be   burger, pizza, veggie.

        The second is the *correct* way.
        """
        pizza = ('Pizza', (3,0,3))   #GGGPPP
        burger = ('Burger', (2,2,2)) #GGAAPP
        veggie = ('Veggie', (2,0,4)) #GGPPPP

        input_data = (pizza, burger, veggie)
        expected_output = (burger, pizza, veggie)

        actual_output = MajorityJudgement().sort_candidates(input_data)
        self.assertEqual(expected_output, actual_output)

    #Dom
    def test_two_identical_winners(self):
        pass

    #Whoever gets there first
    def test_two_identical_losers(self):
        pass

if __name__ == '__main__':
    unittest.main()
