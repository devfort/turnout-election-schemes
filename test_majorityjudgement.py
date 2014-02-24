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

    #Dom
    def test_complex_tie_breaker(self):
        pass

    #Anna
    def test_incomplete_vote(self):
        pass

    #Good Steve
    def test_even_number_of_voters_different_medians(self):
        pass

    #Dom
    def test_two_identical_winners(self):
        pass

    #Whoever gets there first
    def test_two_identical_losers(self):
        pass

if __name__ == '__main__':
    unittest.main()
