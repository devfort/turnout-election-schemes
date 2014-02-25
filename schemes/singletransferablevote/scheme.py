import math

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
