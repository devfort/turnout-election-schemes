from turnout_election_schemes.schemes.errors import FailedElectionError
from .candidate import Candidate
from .stv_round import Round, _Random
from .vote import Vote

class SingleTransferableVoteScheme(object):
    def __init__(self, num_vacancies, candidates, votes, random=_Random()):
        self.num_vacancies = num_vacancies
        self.original_candidates = candidates
        self.remaining_candidates = candidates
        self.votes = votes
        self.random = random
        self.rounds = []
        self.success = False

    def run_round(self):
        new_round = Round(self.num_vacancies, self.remaining_candidates, self.votes, random=self.random)
        new_round.run()

        self.remaining_candidates = filter(
            lambda candidate: not candidate in new_round.results()['excluded'].keys(),
            self.remaining_candidates
        )

        self.rounds.append(new_round)

    def latest_round(self):
        if len(self.rounds) > 0:
            return self.rounds[-1]

    def round_results(self):
        return map(lambda r: r.results(), self.rounds)

    def completed(self):
        if len(self.rounds) > 0:
            return self.latest_round().all_vacancies_filled()

    def final_results(self):
        if self.completed():
            return self.latest_round().elected_candidates()

    def outcome(self):
        return (self.success, self.round_results(), self.final_results())

    def run(self):
        self.success = True
        try:
            while not self.completed():
                self.run_round()
        except FailedElectionError:
            self.success = False
