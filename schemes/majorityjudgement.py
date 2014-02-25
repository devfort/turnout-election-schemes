from operator import itemgetter
from errors import IncompleteVoteError, InvalidVoteError, NoWinnerError

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
        for i, tally_item in enumerate(tally):
            votes_so_far += tally_item
            if (total_votes % 2 == 1 and votes_so_far > (total_votes-1)/2) \
                or (total_votes % 2 == 0 and votes_so_far > (total_votes/2)-1):
                    return [i] + self._get_majority_value(self._tally_with_ith_decremented(tally, i))
        return []

    def _tally_with_ith_decremented(self, tally, i_to_change):
        new_tally = []
        for i, t in enumerate(tally):
            if i == i_to_change:
                new_tally.append(t-1)
            else:
                new_tally.append(t)

        return tuple(new_tally)

    @classmethod
    def from_tuple(klass, t):
        return klass(t[0], t[1])

class MajorityJudgement(object):

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


class VoteAggregator(object):
    def __init__(self, candidate_names, number_of_grades):
        self.candidate_names = candidate_names
        self.number_of_grades = number_of_grades

    def aggregate(self, votes):
        votes_for_candidates = self._transpose_votes(votes)

        return tuple(
            self._candidate_tuple(candidate_name, candidate_votes)
                for candidate_name, candidate_votes
                in zip(self.candidate_names, votes_for_candidates))

    def _transpose_votes(self, votes):
        """
        Takes a set of user votes as input (which is a list of lists - each inner
        list is a specific user's votes, expressed as a numeric preference for
        each candidate. e.g. (1,0,2) means the user gave score 1 to the first
        candidate, score 0 to the second, and score 2 to the third).

        It returns a set of scores for each candidate (i.e. a list of lists,
        with each inner list being a set of scores given to that candidate).
        """
        try:
            return tuple(map(itemgetter(i), votes) for i, _ in enumerate(self.candidate_names))
        except IndexError:
            raise IncompleteVoteError()

    def _grade_counts_for_candidate(self, candidate_votes):
        """
        Calculates the number of votes at each grade level a candidate received.
        E.g. if the candidate received 5 "1"s, 3 "3"s and 2 "0"s, and the
        maximum score is 4, it would return (2, 5, 0, 3, 0)
        """
        grade_counts = [0] * self.number_of_grades

        for vote in candidate_votes:
            if vote < 0 or vote > self.number_of_grades - 1:
                raise InvalidVoteError()

            grade_counts[vote] += 1

        return tuple(grade_counts)

    def _candidate_tuple(self, candidate_name, candidate_votes):
        return (candidate_name, self._grade_counts_for_candidate(candidate_votes))
