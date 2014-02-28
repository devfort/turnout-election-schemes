"""
Majority Judgement is a method of voting proposed by Michel Balinski
and Rida Laraki in "A theory of measuring, electing, and ranking"
(http://www.pnas.org/content/104/21/8720.full)

Members of the electorate vote by assigning grades to candidates. These grades
can be any ordinal values (numbers, "A,B,C", "Good, Bad,Terrible", etc.
All that matters is the relative ordinal positions of the grades.

In this module we assume that grades are consecutive integer values starting
from 0 as the lowest. Because all that matters is the ordering, any other
grading scheme can be trivially converted to this form.

The essential idea of majority judgement is that we sort the grades assigned to
the candidate in order of most significant to least significant in order to compare candidates. At any given point the most significant grade of those left is the lower median of the set (i.e. the highest grade which at least 50% of the population supports).

For example:

Candidate A has four votes: Bad, OK, OK, Good. The median of A's votes is OK, so that is the most significant grade. Once OK is removed, the median of the remainder (Bad, OK, Good) is OK.

In this way, we order candidate A's votes like this:

OK, OK, Bad, Good.

Candidate B might have the gradings OK, OK, Good, Good, ordered in the same way:

OK, Good, OK, Good

Candidate B would win because their second grading is better than candidates A's.
This module provides a type which wraps a tally of grades and is then ordered
in terms of the majority judgement. It may then be used to implement a voting
procedure by assigning each candidate their tally and taking the maximum.
"""


def pop_median(tally):
    total = sum(tally)
    assert total > 0
    median = (total - 1) // 2
    running_total = 0
    for i, t in enumerate(tally):
        running_total += t
        if running_total > median:
            tally[i] -= 1
            result = i
            break
    else:
        assert False
    while tally and not tally[-1]:
        tally.pop()
    return result


class MajorityJudgement(object):
    """
    Objects of type MajorityJudgement support comparison and ordering options
    as per the ordering of the described voting algorithm. They expose no other
    operations.
    """
    def __init__(self, tally):
        """
        Create a MajorityJudgement object from a tally of grades. Note that
        the votes are taken as tallies, not as a list of grades. i.e.
        [1,2,1] means that there is one vote each of grades 0 and 2 and 2 votes
        of grade 1, not that there 2 votes of grade 1 and 1 of grade 2.
        """
        for x in tally:
            if type(x) is not int:
                raise ValueError("Tally counts must be integers: %s" % tally)
            if x < 0:
                raise ValueError(
                    "Tally counts may not be negative: %s" % tally
                )
        tally = list(tally)
        while tally and not tally[-1]:
            tally.pop()

        self.size = sum(tally)
        self.tally = tuple(tally)

    def __repr__(self):
        return "MajorityJudgement(tally=%s,)" % (
            self.tally,
        )

    def __eq__(self, other):
        return self.tally == other.tally

    def __ne__(self, other):
        return self.tally != other.tally

    def __lt__(self, other):
        return self._compare(other) < 0

    def __le__(self, other):
        return self._compare(other) <= 0

    def __gt__(self, other):
        return self._compare(other) > 0

    def __ge__(self, other):
        return self._compare(other) >= 0

    def grade_list(self):
        tally = list(self.tally)
        result = []
        while tally:
            result.append(pop_median(tally))
        return result

    def _compare(self, other):
        """
        Return an integer expressing the order relation between self and
        other. -1 if self < other, 0 if self == other, 1 if self > other.

        The ordering relationship is defined by the majority judgement
        voting order
        """
        assert self.size == other.size
        if self is other:
            return 0

        self_tallies = list(self.tally)
        other_tallies = list(other.tally)

        while self_tallies and other_tallies:
            self_median = pop_median(self_tallies)
            other_median = pop_median(other_tallies)
            if self_median < other_median:
                return -1
            if other_median < self_median:
                return 1
        assert not self_tallies
        assert not other_tallies
        return 0
