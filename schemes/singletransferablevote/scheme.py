class SingleTransferableVoteScheme(object):
    """"""
    def __init__(self, seats, candidates, votes):
        self.seats      = seats
        self.candidates = candidates
        self.votes      = votes
    
    def round(self):
        pass
    
    def completed(self):
        return False

   def final_results(self):
        pass
