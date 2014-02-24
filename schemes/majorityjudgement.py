from operator import itemgetter

class MajorityJudgement(object):
    def sort_candidates(self, candidates):
        return candidates

class VoteAggregator(object):
    def aggregate(self, candidates, all_votes, number_of_grades):
        votes_for_candidates = (map(itemgetter(i), all_votes) for i, _ in enumerate(candidates))

        aggregate = []
        for candidate, votes in zip(candidates, votes_for_candidates):
            grade_counts = [0] * number_of_grades

            for vote in votes:
                grade_counts[vote] += 1

            aggregate.append((candidate, tuple(reversed(grade_counts))))

        return tuple(aggregate)
