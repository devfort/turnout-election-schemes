from operator import itemgetter
import math
from fractions import Fraction

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

        #import ipdb; ipdb.set_trace()
        while not self.all_vacancies_filled() and self._surplus_exists():
            self._reassign_votes_from_candidate_with_highest_surplus()
            self._provisionally_elect_candidates()

        if not self.all_vacancies_filled():
            self._exclude_candidate_with_fewest_votes()
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
        self.continuing_candidates = {candidate: Candidate(candidate) for candidate in candidates}
        self.provisionally_elected_candidates = []
        self.excluded_candidates = []

    def _prepare_votes(self, votes):
        self.votes = map(lambda v: Vote(self.continuing_candidates.keys(), v), votes)
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
        if len(self.continuing_candidates) <= self._remaining_vacancies():
            candidates_to_elect = self.continuing_candidates.values()
        else:
            candidates_to_elect = filter(
                lambda c: c.value_of_votes() >= self.quota,
                self.continuing_candidates.values()
            )

        for candidate in candidates_to_elect:
            self.provisionally_elected_candidates.append(candidate)
            del self.continuing_candidates[candidate.candidate_id]

    def _remaining_vacancies(self):
        return self.num_vacancies - len(self.provisionally_elected_candidates)

    def _surplus_exists(self):
        return len(self._candidates_with_surplus()) > 0

    def _reassign_votes_from_candidate_with_highest_surplus(self):
        candidate = self._candidates_with_surplus()[0]
        candidate.devalue_votes(self.quota)
        self._assign_votes(candidate.votes)

    def _exclude_candidate_with_fewest_votes(self):
        candidate = self._candidate_with_fewest_votes()
        self.excluded_candidates.append(candidate)
        del self.continuing_candidates[candidate.candidate_id]

    def _candidate_with_fewest_votes(self):
        candidates = sorted(
            self.continuing_candidates.values(),
            key = lambda c: c.value_of_votes()
        )

        return candidates[0]

    def _candidates_with_surplus(self):
        candidates = filter(
            lambda c: c.value_of_votes() > self.quota,
            self.provisionally_elected_candidates
        )

        return sorted(
            candidates,
            key = lambda c: c.value_of_votes(),
            reverse = True
        )

    def _provisionally_elected(self):
        return self._candidate_dict_for_results(self.provisionally_elected_candidates)

    def _continuing(self):
        return self._candidate_dict_for_results(self.continuing_candidates.values())

    def _excluded(self):
        return self._candidate_dict_for_results(self.excluded_candidates)

    def _candidate_dict_for_results(self, candidates):
        return {candidate.candidate_id: candidate.value_of_votes() for candidate in candidates}

    def _assign_votes(self, votes):
        #import ipdb; ipdb.set_trace()
        for vote in votes:
            preferred_candidate = vote.preference_from(self.continuing_candidates.keys())
            if preferred_candidate is not None:
                self.continuing_candidates[preferred_candidate].votes.append(vote)

class SingleTransferableVoteScheme(object):
    def __init__(self, num_vacancies, candidates, votes):
        self.num_vacancies = num_vacancies
        self.original_candidates = candidates
        self.remaining_candidates = candidates
        self.votes = votes

    def run_round(self):
        self.latest_round = Round(self.num_vacancies, self.remaining_candidates, self.votes)
        self.latest_round.run()

        #import ipdb; ipdb.set_trace()
        self.remaining_candidates = filter(
            lambda candidate: not candidate in self.round_results()['excluded'].keys(),
            self.remaining_candidates
        )

    def round_results(self):
        return self.latest_round.results()

    def completed(self):
        return self.latest_round.all_vacancies_filled()

class __SingleTransferableVoteScheme(object):
    """"""
    def __init__(self, seats, candidates, votes):
        self.seats      = seats
        self.candidates = candidates
        self.votes      = votes

    def run_round(self):
        #calculate quota
        quota = self.calculate_quota(self.seats, self.votes)
        #calculate_totals
        totals = self.calculate_totals()
        #reallocate surplus votes 0+ times until done
        reallocated_totals = self.reallocate_surplus_votes(quota, totals)
        #reallocate_surplus_votes
        #if there are not seats winners
            #eliminate loser
        #return candidates and their intermediate votes

    def round_results(self):
        pass

    def completed(self):
        return False

    def final_results(self):
        pass

    def calculate_quota(self, seats, votes):
        # TODO needs to deal with exhausted votes
        # either in the method or before it's called
        # unresolved - hence duplication of parameters
        interim = len(votes)/(seats + 1)
        quota_floor = math.floor(interim + 1)
        return int(quota_floor)

    def calculate_totals(self):
        counts = {}

        for candidate in self.candidates:
            counts[candidate] = 0

        for vote in self.votes:
            first_choice = vote[0]
            counts[first_choice] = counts[first_choice] + 1

        return counts

    def reallocate_surplus_votes(self, quota, totals):
        reallocated_totals = totals

        # get an ordered list of those who meet the quota
        provisionally_elected_candidates = self.candidates_that_meet_quota(quota, reallocated_totals)
        highest_candidate = provisionally_elected_candidates[0]

        processed = {}
        while reallocated_totals[highest_candidate] > quota:
            # calculate the value of their vote
            vote_value = Fraction(reallocated_totals[highest_candidate] - quota, reallocated_totals[highest_candidate])

            # go through all the votes for transferring
            # look here first for efficiency gains!
            for vote in self.votes:
                # the question is - are they the highest not-yet-processed
                # candidate on this ballot paper
                if highest_candidate in vote:
                    devalued_vote = vote_value
                    # Use slices for this
                    evaluate = True
                    position = vote.index(highest_candidate)
                    for processed_candidate in vote[:position]:
                        if not processed.has_key(processed_candidate):
                            evaluate = False
                    
                    if evaluate:
                        for candidate in vote:
                            if candidate == highest_candidate:
                                continue
                            elif processed.has_key(candidate):
                                devalued_vote = devalued_vote * processed[candidate]
                            # we do not want to allocate votes to someone else
                            # who has met the quota - in this case skip, it
                            # will go to the next preference on this vote
                            elif candidate not in provisionally_elected_candidates:
                                reallocated_totals[candidate] = reallocated_totals[candidate] + devalued_vote
                                break

            # reset their total to the max required, i.e. the quota
            reallocated_totals[highest_candidate] = quota
            processed[highest_candidate] = vote_value
            #reset totals
            provisionally_elected_candidates = self.candidates_that_meet_quota(quota, reallocated_totals)
            highest_candidate = provisionally_elected_candidates[0]

        return reallocated_totals

    def candidates_that_meet_quota(self, quota, totals):
        # return names ordered by descending total for those whose total is
        # greather than or equal to the quota
        met_quota = []
        sorted_totals = sorted(totals.items(), key=itemgetter(1), reverse=True) 
        for candidate, total in sorted_totals:
            if total >= quota:
                met_quota.append(candidate)
        return met_quota
