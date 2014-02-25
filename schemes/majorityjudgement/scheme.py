from operator import itemgetter
from schemes.errors import NoWinnerError, IncompleteVoteError
from schemes.majorityjudgement.algorithm import MajorityJudgement as MJCandidate

class MajorityJudgementScheme(object):
    def sort_candidates(self, candidates):
        self._ensure_all_votes_are_of_same_length(map(itemgetter(1), candidates))

        mj_candidates = []
        for c in candidates:
            mj_candidate = MJCandidate(c[1])
            mj_candidate.original_tuple = c
            mj_candidates.append(mj_candidate)

        sorted_candidates = sorted(mj_candidates, reverse=True)

        self._ensure_no_duplicate_winner(sorted_candidates)

        return tuple(c.original_tuple for c in sorted_candidates)

    def _ensure_all_votes_are_of_same_length(self, votes):
        unique_vote_sizes = set(map(len, votes))
        if len(unique_vote_sizes) > 1:
            raise IncompleteVoteError()

    def _ensure_no_duplicate_winner(self, sorted_items):
        if len(sorted_items) >= 2 and not cmp(sorted_items[0], sorted_items[1]):
            raise NoWinnerError()
