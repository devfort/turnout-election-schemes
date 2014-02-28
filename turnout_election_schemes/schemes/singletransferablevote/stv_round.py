from turnout_election_schemes.schemes.errors import FailedElectionError
from .candidate import Candidate
from .vote import Vote

class _Random(object):
    def choice(self, sequence):
        raise FailedElectionError()

class Round(object):
    def __init__(self, num_vacancies, candidates, votes, random=_Random()):
        self.num_vacancies = num_vacancies
        self.random = random
        self._prepare_candidates(candidates)
        self._prepare_votes(votes)

    def run(self):
        self._provisionally_elect_candidates()

        while not self.all_vacancies_filled() and self._surplus_exists():
            self._reassign_votes_from_candidate_with_highest_surplus()
            self._provisionally_elect_candidates()

        if not self.all_vacancies_filled():
            self._exclude_candidates_with_fewest_votes()
            self._provisionally_elect_candidates()

    def results(self):
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
        for candidate in self._candidates_to_exclude():
            self._excluded_candidates.append(candidate)
            del self._continuing_candidates[candidate.candidate_id]

    def _candidates_to_exclude(self):
        """
        Returns a list of candidates that should be excluded. Checks to see if
        a bulk exclusion is possible first, and then falls back to providing
        the candidate with the fewest votes.
        """

        bulk_exclusions = self._bulk_exclusions()

        if len(bulk_exclusions) > 0:
            return bulk_exclusions
        else:
            return [self._candidate_with_fewest_votes()]

    def _candidate_with_fewest_votes(self):
        """
        Return the candidate with the fewest votes. In case of a tie, break it
        using the random generator.
        """

        fewest_votes = min(map(
            lambda c: c.value_of_votes(),
            self._continuing_candidates.values()
        ))

        candidates = filter(
            lambda c: c.value_of_votes() == fewest_votes,
            self._continuing_candidates.values()
        )

        if len(candidates) > 1:
            return self.random.choice(candidates)
        else:
            return candidates[0]

    def _bulk_exclusions(self):
        """
        Two or more candidates may be excluded simultaneously if the aggregated
        value of all candidates to be excluded is less then the value of the
        next lowest candidate and the value required by a candidate to obtain a
        quota.

        If bulk exclusion mean that too few candidates remain to fill the
        vacancies, bulk exclusion should not be applied.

        This method returns a list of candidates which may be excluded in this
        way or an empty list if a bulk exclusion isn't possible.
        """

        candidates = sorted(
            self._continuing_candidates.values(),
            key = lambda c: c.value_of_votes()
        )

        eligible_slice = []
        current_slice = []
        for index in range(0, len(candidates)-1):
            current_slice = self._lowest_to_n_inclusive(candidates, index)
            total_votes = self._slice_total_votes(current_slice)
            if (
                total_votes < self.quota
                and total_votes < self._next_highest_total(index, candidates)
            ):
                    eligible_slice = current_slice

        bulk_exclusions = []
        if (
            len(eligible_slice) > 1
            and self._enough_candidates_would_remain(eligible_slice)
        ):
            bulk_exclusions = eligible_slice

        return bulk_exclusions

    def _enough_candidates_would_remain(self, eligible_slice):
        number_to_exclude = len(eligible_slice)
        potential_candidates = len(self._continuing()) + len(self._provisionally_elected())
        return potential_candidates - number_to_exclude >= self.num_vacancies

    def _slice_total_votes(self, current_slice):
        totals = 0
        for candidate in current_slice:
            totals += candidate.value_of_votes()
        return totals

    def _next_highest_total(self, index, candidates):
        next_candidate = candidates[index+1]
        return next_candidate.value_of_votes()

    def _lowest_to_n_inclusive(self, candidates, index):
        low_slice = []
        # to n inclusive
        for index in range(0,index+1):
            low_slice.append(candidates[index])
        return low_slice

    def _candidate_with_highest_surplus(self):
        most_votes = max(map(
            lambda c: c.value_of_votes(),
            self._candidates_with_surplus()
        ))

        candidates = filter(
            lambda c: c.value_of_votes() == most_votes,
            self._candidates_with_surplus()
        )

        if len(candidates) > 1:
            return self.random.choice(candidates)
        else:
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
        for vote in votes:
            preferred_candidate = vote.preference_from(self._continuing_candidates.keys())
            if preferred_candidate is not None:
                self._continuing_candidates[preferred_candidate].votes.append(vote)
