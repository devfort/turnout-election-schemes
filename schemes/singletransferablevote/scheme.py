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
