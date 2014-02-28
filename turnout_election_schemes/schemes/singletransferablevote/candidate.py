from fractions import Fraction

class Candidate(object):
    def __init__(self, candidate_id):
        self.candidate_id = candidate_id
        self.votes = []
        self.elected = False
        self.elected_quota = 0

    def value_of_votes(self):
        """
        Get the total value of all votes allocated to this candidate. If the
        candidate has been marked as elected by calling devalue_votes() then
        this method returns the cached quota value given to it.
        """

        if self.elected:
            return self.elected_quota
        else:
            return reduce(lambda a, b: a + b, map(lambda v: v.value, self.votes), 0)

    def devalue_votes(self, quota):
        """
        Devalue the value of each of this candidate's votes based on the ratio
        of surplus to quota. Since we're devaluing the votes, we also cache the
        quota and mark ourselves as elected so we can reply correctly to calls
        to value_to_votes().
        """

        total_value = self.value_of_votes()
        surplus_ratio = Fraction(total_value - quota, total_value)
        for vote in self.votes:
            vote.value *= surplus_ratio

        self.elected = True
        self.elected_quota = quota
