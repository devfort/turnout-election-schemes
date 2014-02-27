from turnout_election_schemes.schemes.scheme_runner import SchemeRunner
from turnout_election_schemes.schemes.election_results import ElectionResults
from turnout_election_schemes.schemes.majorityjudgement import VoteAggregator, MajorityJudgementCount
import csv

class Runner(SchemeRunner):
    def run(self, stream):
        reader = csv.reader(stream)
        headers = next(reader)[1:]
        vote_tuples = []
        max_grade = 0

        for row in reader:
            row_votes = map(lambda s: int(s) if s else 0, row[1:])
            max_grade = max(max_grade, max(row_votes))

            vote_tuples.append(row_votes)

        aggregator = VoteAggregator(headers, max_grade + 1)
        aggregated_votes = aggregator.aggregate(vote_tuples)

        scheme = MajorityJudgementScheme()
        sorted_candidates = scheme.sort_candidates(aggregated_votes)

        return ElectionResults([sorted_candidates[0][0]], sorted_candidates)

    def plain_text_report(self, report):
        lines = []
        number_of_grades = len(report[0][1])

        max_candidate_length = max(map(len, [c for c,v in report]))

        lines.append(('\tGrade %s| ' % (' '*(max_candidate_length-5))) + ' | '.join(map(str, range(number_of_grades))))
        lines.append('-' * 100)

        for candidate, votes in report:
            tally = " | ".join(map(str, votes))
            lines.append("\t%s %s| %s" % (candidate, ' '*(max_candidate_length-len(candidate)), tally))

        return '\n'.join(lines)
