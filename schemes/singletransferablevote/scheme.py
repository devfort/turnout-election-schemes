import math
from fractions import Fraction

class SingleTransferableVoteScheme(object):
    """"""
    def __init__(self, seats, candidates, votes):
        self.seats      = seats
        self.candidates = candidates
        self.votes      = votes

    def run_round(self):
        #calculate quota
        quota = self.calculate_quota(self.seats, self.votes)
        #calculate_totals
        #calculate_totals
        #reallocate surplus votes 0+ times until done
        #reallocate_surplus_votes
        #if there are not seats winners
            #eliminate loser
        #return candidates and their intermediate votes

    def completed(self):
        return False

    def final_results(self):
        pass

    def calculate_quota(self, seats, votes):
        # TODO needs to deal with exhausted votes
        # either in the method or before it's called
        # unresolved - hence duplication of parameters
        interim = len(votes)/(seats + 1)
        return math.floor(interim + 1)

    def calculate_totals(self):
        counts = {}

        for candidate in self.candidates:
            counts[candidate] = 0

        for vote in self.votes:
            first_choice = vote[0]
            counts[first_choice] = counts[first_choice] + 1

        return counts

    def reallocate_surplus_votes(self, quota, totals):
        # Identify candidate to be reallocated
        # TODO: Deal with reallocation for multiple candidates
        reallocation_candidate = None
        for candidate, total in totals.items():
            if total > quota:
                reallocation_candidate = candidate

        reallocated_vote_value = Fraction(totals[reallocation_candidate] - quota, totals[reallocation_candidate])

        # Reallocate candidate's votes
        reallocated_totals = totals
        reallocated_totals[reallocation_candidate] = quota
        for vote in self.votes:
            if reallocation_candidate == vote[0]:
                # TODO: Handle no candidate to reallocate vote to
                reallocated_totals[vote[1]] = reallocated_totals[vote[1]] + reallocated_vote_value

        return reallocated_totals
