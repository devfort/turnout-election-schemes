from operator import itemgetter
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
        totals = self.calculate_totals()
        #reallocate surplus votes 0+ times until done
        reallocated_totals = self.reallocate_surplus_votes(quota, totals)
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
        # get an ordered list of those who have exceeded the quota

        # Identify candidates whose surplus votes need to be rellocated
        provisionally_elected_candidates = self.candidates_that_meet_quota(quota, totals)
        reallocated_totals = totals

        for candidate in provisionally_elected_candidates:
            # calculate the value of their vote
            vote_value = Fraction(totals[candidate] - quota, totals[candidate])
            # reset their total to the max required, i.e. the quota
            reallocated_totals[candidate] = quota

            # go through all the votes
            # where our candidate is the first choice, find out
            # who their second choice is and assign them the vote value
            # other provisonally elected candidates do not received
            # tranferred votes in this way
            for vote in self.votes:
                if candidate == vote[0]:

                    for next_preference in vote:
                        if next_preference not in provisionally_elected_candidates:
                            reallocated_totals[next_preference] = reallocated_totals[next_preference] + vote_value
                            break

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
