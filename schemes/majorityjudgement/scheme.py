from operator import itemgetter
from schemes.errors import NoWinnerError, IncompleteVoteError
from schemes.majorityjudgement.candidate import Candidate

class MajorityJudgementScheme(object):
    def sort_candidates(self, candidates):
        self._ensure_all_votes_are_of_same_length(map(itemgetter(1), candidates))

        candidate_objects = map(Candidate.from_tuple, candidates)
        sorted_candidates = self._get_sorted_candidates(candidate_objects)

        self._ensure_no_duplicate_winner(sorted_candidates)

        return tuple(c.to_tuple() for c in sorted_candidates)

    def _get_sorted_candidates(self, candidates):
        return sorted(
                    candidates,
                    lambda c1, c2: cmp(c1.majority_value, c2.majority_value),
                    reverse=True)

    def _ensure_all_votes_are_of_same_length(self, votes):
        unique_vote_sizes = set(map(len, votes))
        if len(unique_vote_sizes) > 1:
            raise IncompleteVoteError()

    def _ensure_no_duplicate_winner(self, sorted_items):
        if len(sorted_items) >= 2 and sorted_items[0].majority_value == sorted_items[1].majority_value:
            raise NoWinnerError()
