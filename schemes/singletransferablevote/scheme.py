from operator import itemgetter
import math
from fractions import Fraction
from schemes.errors import FailedElectionError

class Vote(object):
    def __init__(self, candidates_running, candidate_preferences):
        self.candidate_preferences = filter(
            lambda candidate: candidate in candidates_running,
            candidate_preferences
        )
        self.value = 1

    def is_exhausted(self):
        return len(self.candidate_preferences) == 0

    def preference_from(self, candidates):
        matches = filter(lambda candidate: candidate in candidates, self.candidate_preferences)

        if len(matches) > 0:
            return matches[0]
        else:
            return None

class Candidate(object):
    def __init__(self, candidate_id):
        self.candidate_id = candidate_id
        self.votes = []
        self.elected = False
        self.elected_quota = 0

    def value_of_votes(self):
        if self.elected:
            return self.elected_quota
        else:
            return reduce(lambda a, b: a + b, map(lambda v: v.value, self.votes), 0)

    def devalue_votes(self, quota):
        # devalue the votes based on the ratio of surplus to quota
        total_value = self.value_of_votes()
        surplus_ratio = Fraction(total_value - quota, total_value)
        for vote in self.votes:
            vote.value *= surplus_ratio

        self.elected = True
        self.elected_quota = quota

class Round(object):
    def __init__(self, num_vacancies, candidates, votes):
        self.num_vacancies = num_vacancies
        self._prepare_candidates(candidates)
        self._prepare_votes(votes)

    def run(self):
        self._provisionally_elect_candidates()

        if not self.all_vacancies_filled:
            # Putting it here assumes that if this eliminates all remaining
            # candidates it would be a failed election - 1000,1000,3,2,2
            # with three vacancies - does the 3 get elected? or is it
            # a failed election?
            self._bulk_exclusions()

        #import ipdb; ipdb.set_trace()
        while not self.all_vacancies_filled() and self._surplus_exists():
            self._reassign_votes_from_candidate_with_highest_surplus()
            self._provisionally_elect_candidates()

        if not self.all_vacancies_filled():
            self._exclude_candidates_with_fewest_votes()
            self._provisionally_elect_candidates()

    def results(self):
        #import ipdb; ipdb.set_trace()
        return {
            'provisionally_elected': self._provisionally_elected(),
            'continuing': self._continuing(),
            'excluded': self._excluded()
        }

    def all_vacancies_filled(self):
        return self._remaining_vacancies() == 0

    def _prepare_candidates(self, candidates):
        self._continuing_candidates = {candidate: Candidate(candidate) for candidate in candidates}
        self._provisionally_elected_candidates = []
        self._excluded_candidates = []

    def _prepare_votes(self, votes):
        self.votes = map(lambda v: Vote(self._continuing_candidates.keys(), v), votes)
        self.exhausted_votes = filter(lambda v: v.is_exhausted(), self.votes)
        self.unexhausted_votes = filter(lambda v: not v.is_exhausted(), self.votes)

        for vote in self.exhausted_votes:
            vote.value = 0

        self.quota = self._calculate_quota()
        self._assign_votes(self.unexhausted_votes)

    def _calculate_quota(self):
        return len(self.unexhausted_votes) / (self.num_vacancies + 1) + 1

    def _provisionally_elect_candidates(self):
        #import ipdb; ipdb.set_trace()
        if len(self._continuing_candidates) <= self._remaining_vacancies():
            candidates_to_elect = self._continuing_candidates.values()
        else:
            candidates_to_elect = filter(
                lambda c: c.value_of_votes() >= self.quota,
                self._continuing_candidates.values()
            )

        candidates_to_elect = sorted(
            candidates_to_elect,
            key = lambda c: c.value_of_votes(),
            reverse = True
        )

        for candidate in candidates_to_elect:
            self._provisionally_elected_candidates.append(candidate)
            del self._continuing_candidates[candidate.candidate_id]

    def elected_candidates(self):
        """
        Return the list of the candidates that have been
        provisionally elected in order of election.
        """
        return map(
            lambda c: c.candidate_id,
            self._provisionally_elected_candidates
        )

    def _remaining_vacancies(self):
        return self.num_vacancies - len(self._provisionally_elected_candidates)

    def _surplus_exists(self):
        return len(self._candidates_with_surplus()) > 0

    def _reassign_votes_from_candidate_with_highest_surplus(self):
        candidate = self._candidate_with_highest_surplus()
        candidate.devalue_votes(self.quota)
        self._assign_votes(candidate.votes)

    def _exclude_candidates_with_fewest_votes(self):
        candidates_to_exclude = self._candidates_with_fewest_votes()
        for candidate in candidates_to_exclude:
            self._excluded_candidates.append(candidate)
            del self._continuing_candidates[candidate.candidate_id]

    def _candidates_with_fewest_votes(self):
        candidates = sorted(
            self._continuing_candidates.values(),
            key = lambda c: c.value_of_votes()
        )

        lowest_candidates = [candidates[0]]

        if len(candidates) > 1 and candidates[0].value_of_votes() == candidates[1].value_of_votes():
            raise FailedElectionError

        return lowest_candidates

    def _bulk_exclusions(self):
        # If there are multiple candidates with very low
        # votes, we can exclude a few of them at once
        # get a list of candidates lowest first
        candidates = sorted(
            self._continuing_candidates.values(),
            key = lambda c: c.value_of_votes()
        )

        # deal with multiple very low votes
        total_lowest_votes = 0
        lowest_candidates = []
        for candidate in candidates:
            total_lowest_votes += candidate.value_of_votes()
            # it's not just this though, it's also for next candidate
            if total_lowest_votes < self.quota:
                print candidate.candidate_id
                lowest_candidates.append(candidate)
                self._continuing_candidates.remove(candidate)
            else:
                break


    def _candidate_with_highest_surplus(self):
        candidates = sorted(
            self._candidates_with_surplus(),
            key = lambda c: c.value_of_votes(),
            reverse = True
        )

        if len(candidates) > 1 and candidates[0].value_of_votes() == candidates[1].value_of_votes():
            raise FailedElectionError()

        return candidates[0]

    def _candidates_with_surplus(self):
        return filter(
            lambda c: c.value_of_votes() > self.quota,
            self._provisionally_elected_candidates
        )

    def _provisionally_elected(self):
        return self._candidate_dict_for_results(self._provisionally_elected_candidates)

    def _continuing(self):
        return self._candidate_dict_for_results(self._continuing_candidates.values())

    def _excluded(self):
        return self._candidate_dict_for_results(self._excluded_candidates)

    def _candidate_dict_for_results(self, candidates):
        return {candidate.candidate_id: candidate.value_of_votes() for candidate in candidates}

    def _assign_votes(self, votes):
        #import ipdb; ipdb.set_trace()
        for vote in votes:
            preferred_candidate = vote.preference_from(self._continuing_candidates.keys())
            if preferred_candidate is not None:
                self._continuing_candidates[preferred_candidate].votes.append(vote)

class SingleTransferableVoteScheme(object):
    def __init__(self, num_vacancies, candidates, votes):
        self.num_vacancies = num_vacancies
        self.original_candidates = candidates
        self.remaining_candidates = candidates
        self.votes = votes
        self.rounds = []

    def run_round(self):
        new_round = Round(self.num_vacancies, self.remaining_candidates, self.votes)
        new_round.run()

        #import ipdb; ipdb.set_trace()
        self.remaining_candidates = filter(
            lambda candidate: not candidate in new_round.results()['excluded'].keys(),
            self.remaining_candidates
        )

        self.rounds.append(new_round)

    def latest_round(self):
        if len(self.rounds) > 0:
            return self.rounds[-1]

    def round_results(self):
        if len(self.rounds) > 0:
            return self.latest_round().results()

    def completed(self):
        if len(self.rounds) > 0:
            return self.latest_round().all_vacancies_filled()

    def final_results(self):
        if self.completed():
            return self.latest_round().elected_candidates()
