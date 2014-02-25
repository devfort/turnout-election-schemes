import random
import resource
import sys

class MajorityJudgementDataGenerator(object):
    def __init__(self, num_grades, num_candidates, num_voters):
        self.num_grades = num_grades
        self.num_candidates = num_candidates
        self.num_voters = num_voters

    def votes(self):
        return (self.vote() for _ in range(self.num_voters))

    def vote(self):
        return (self.grade() for candidate in self.candidates())

    def grade(self):
        return random.randint(0, self.num_grades - 1)

    def candidates(self):
        return range(self.num_candidates)

def usage():
    print 'Usage: %s num_grades num_candidates num_voters' % sys.argv[0]

def print_resource_usage():
    rusage = resource.getrusage(resource.RUSAGE_SELF)
    print 'utime: %f\t\tstime: %f\t\tmaxrss: %i' % (rusage.ru_utime, rusage.ru_stime, rusage.ru_maxrss)

if __name__ == '__main__':
    try:
        print_resource_usage()
        args = map(int, sys.argv[1:])
        generator = MajorityJudgementDataGenerator(*args)
        votes = generator.votes()
        print_resource_usage()
    except ValueError:
        usage()
    except TypeError:
        usage()
