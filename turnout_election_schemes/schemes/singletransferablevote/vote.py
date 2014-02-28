class Vote(object):
    def __init__(self, candidates_running, candidate_preferences):
        self.candidate_preferences = filter(
            lambda candidate: candidate in candidates_running,
            candidate_preferences
        )
        self.value = 1

    def is_exhausted(self):
        """
        Returns true if this vote has no preferred candidates still running.
        """

        return len(self.candidate_preferences) == 0

    def preference_from(self, candidates):
        """
        Returns the most preferred candidate from the list of candidates given,
        or None if there isn't one.
        """

        matches = filter(lambda candidate: candidate in candidates, self.candidate_preferences)

        if len(matches) > 0:
            return matches[0]
        else:
            return None
