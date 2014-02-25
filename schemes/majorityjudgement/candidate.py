class Candidate(object):
    def __init__(self, name, votes):
        self.name = name
        self.votes = votes
        self.majority_value = self._get_majority_value(self.votes)

    def to_tuple(self):
        return (self.name, self.votes)

    def _get_majority_value(self, tally):
        total_votes = sum(tally)
        votes_so_far = 0
        vote_cutoff = (total_votes / 2 - 1) if total_votes % 2 == 0 else (total_votes - 1) / 2

        for i, tally_item in enumerate(tally):
            votes_so_far += tally_item
            if votes_so_far > vote_cutoff:
                return [i] + self._get_majority_value(self._tally_with_ith_decremented(tally, i))
        return []

    def _tally_with_ith_decremented(self, tally, i):
        new_tally = list(tally)
        new_tally[i] -= 1
        return tuple(new_tally)

    @classmethod
    def from_tuple(klass, t):
        return klass(t[0], t[1])
