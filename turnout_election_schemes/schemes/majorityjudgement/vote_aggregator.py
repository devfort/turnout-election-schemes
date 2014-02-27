from operator import itemgetter
from turnout_election_schemes.schemes.errors import IncompleteVoteError, InvalidVoteError

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
