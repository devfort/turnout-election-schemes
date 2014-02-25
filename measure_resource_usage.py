import random
import resource
from schemes.majorityjudgement import VoteAggregator, MajorityJudgementScheme
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

def usage():
    print 'Usage: %s num_grades num_candidates num_voters' % sys.argv[0]

def resource_usage():
    return resource.getrusage(resource.RUSAGE_SELF)

def print_resource_usage(initial, final):
    utime = final.ru_utime - initial.ru_utime
    stime = final.ru_stime - initial.ru_stime
    maxrss = final.ru_maxrss - initial.ru_maxrss
    print 'utime: %f\t\tstime: %f\t\tmaxrss: %i' % (utime, stime, maxrss)

if __name__ == '__main__':
    try:
        args = map(int, sys.argv[1:])
        generator = MajorityJudgementDataGenerator(*args)
        candidates = generator.candidates()
        votes = generator.votes()
    except ValueError:
        usage()
        sys.exit(1)
    except TypeError:
        usage()
        sys.exit(1)

    initial_resource_usage = resource_usage()
    aggregator = VoteAggregator(candidates, generator.num_grades)
    aggregated_votes = aggregator.aggregate(votes)
    scheme = MajorityJudgementScheme()
    scheme.sort_candidates(aggregated_votes)
    print_resource_usage(initial_resource_usage, resource_usage())
