import random

class MajorityJudgementDataGenerator(object):
    def __init__(self, num_grades, num_candidates, num_voters):
        self.num_grades = num_grades
        self.num_candidates = num_candidates
        self.num_voters = num_voters

    def votes(self):
        return [self.vote() for _ in range(self.num_voters)]

    def vote(self):
        return {candidate: self.grade() for candidate in self.candidates()}

    def grade(self):
        return random.randint(0, self.num_grades - 1)

    def candidates(self):
        return range(self.num_candidates)
