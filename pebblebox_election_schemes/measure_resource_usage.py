import random
import resource
from schemes.majorityjudgement import VoteAggregator, MajorityJudgementCount
from schemes.singletransferablevote import SingleTransferableVoteScheme
import sys

class MajorityJudgementDataGenerator(object):
    def __init__(self, num_grades, num_candidates, num_voters):
        self.num_grades = num_grades
        self.num_candidates = num_candidates
        self.num_voters = num_voters

    def votes(self):
        return tuple(self.vote() for _ in range(self.num_voters))

    def vote(self):
        return tuple(self.grade() for candidate in self.candidates())

    def grade(self):
        return random.randint(0, self.num_grades - 1)

    def candidates(self):
        return range(self.num_candidates)

class SingleTransferableVoteDataGenerator(object):
    def __init__(self, num_candidates, num_voters):
        self.num_candidates = num_candidates
        self.num_voters = num_voters

    def votes(self):
        return tuple(self.vote() for _ in range(self.num_voters))

    def vote(self):
        return random.sample(self.candidates(), random.randrange(len(self.candidates()) + 1))

    def candidates(self):
        return range(self.num_candidates)

def usage():
    print 'Usage: %s mj num_grades num_candidates num_voters' % sys.argv[0]
    print '       %s stv num_vacancies num_candidates num_voters' % sys.argv[0]

def resource_usage():
    return resource.getrusage(resource.RUSAGE_SELF)

def print_resource_usage(initial, final):
    utime = final.ru_utime - initial.ru_utime
    stime = final.ru_stime - initial.ru_stime
    maxrss = final.ru_maxrss - initial.ru_maxrss
    print 'utime: %f\t\tstime: %f\t\tmaxrss: %i' % (utime, stime, maxrss)

def test_majority_judgement(num_grades, num_candidates, num_voters):
    generator = MajorityJudgementDataGenerator(num_grades, num_candidates, num_voters)
    candidates = generator.candidates()
    votes = generator.votes()

    initial_resource_usage = resource_usage()

    aggregator = VoteAggregator(candidates, generator.num_grades)
    aggregated_votes = aggregator.aggregate(votes)
    scheme = MajorityJudgementCount()
    scheme.sort_candidates(aggregated_votes)

    print_resource_usage(initial_resource_usage, resource_usage())

def test_single_transferable_vote(num_vacancies, num_candidates, num_voters):
    generator = SingleTransferableVoteDataGenerator(num_candidates, num_voters)
    candidates = generator.candidates()
    votes = generator.votes()

    initial_resource_usage = resource_usage()

    scheme = SingleTransferableVoteScheme(num_vacancies, candidates, votes)
    rounds = 0

    while not scheme.completed():
        scheme.run_round()
        rounds += 1
        if rounds > num_candidates:
            print 'Election did not complete within %d rounds' % rounds
            break

    print_resource_usage(initial_resource_usage, resource_usage())

if __name__ == '__main__':
    if len(sys.argv) != 5:
        usage()
        sys.exit(1)

    try:
        system = sys.argv[1]
        args = map(int, sys.argv[2:])
    except ValueError:
        usage()
        sys.exit(1)

    if system == 'mj':
        test_majority_judgement(*args)
    elif system == 'stv':
        test_single_transferable_vote(*args)
