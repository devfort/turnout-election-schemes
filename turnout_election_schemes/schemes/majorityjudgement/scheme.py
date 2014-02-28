import math
from turnout_election_schemes.schemes.majorityjudgement.count import MajorityJudgementCount
from turnout_election_schemes.schemes.majorityjudgement.vote_aggregator import VoteAggregator

class Scheme(object):
    def perform_count(self, candidate_ids, votes_as_json, max_grade=4):
        """
        votes_as_json is a list of tuples, each one being an individual users votes.
        And each vote is a tuple with a numeric grade for each candidate, in the natural
        order of the candidates.
        """
        aggregator = VoteAggregator(candidate_ids, max_grade + 1)
        aggregated_votes = aggregator.aggregate(votes_as_json)

        scheme = MajorityJudgementCount()
        succeeded, result = scheme.sort_candidates(aggregated_votes)
        return (
            succeeded,
            { x[0]: self._candidate_dict(x[1], n) for n, x in enumerate(result) },
            (result[0][0],)
        )

    def _candidate_dict(self, counts, order):
        median = self._median_grade(counts)

        return {
                'grade': median,
                'order': order,
                'counts': counts
                }

    def _median_grade(self, counts):
        total_grades = sum(counts)
        median_point = math.ceil(float(total_grades)/2)
        total_so_far = 0
        for score, count in enumerate(counts):
            total_so_far += count
            if total_so_far >= median_point:
                return score
