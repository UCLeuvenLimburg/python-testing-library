from contextlib import contextmanager
from ucll_scripting.dynamic import create_dynamic_variable, let, value
from ucll_scripting.testing import *


class Score:
    def __init__(self, grade, maximum):
        self.__grade = grade
        self.__maximum = maximum

    @property
    def grade(self):
        return self.__grade

    @property
    def maximum(self):
        return self.__maximum

    def __add__(self, other):
        return Score(self.grade + other.grade, self.maximum + other.maximum)

    def __eq__(self, other):
        return self.grade == other.grade and self.maximum == other.maximum

    def rescale(self, maximum):
        factor = maximum / self.maximum
        return Score(self.grade * factor, maximum)

    @property
    def is_perfect(self):
        return self.grade == self.maximum

    @property
    def zero(self):
        return Score(0, self.maximum)

    def __str__(self):
        return f"{self.grade}/{self.maximum}"

    def __repr__(self):
        return f"Score[{self.grade}/{self.maximum}]"


class ScoreKeeper:
    def __init__(self):
        self.score = Score(0, 0)

class NotKeepingScoresError(Exception):
    pass

class MissingScoreKeeper(ScoreKeeper):
    def test_passed(self):
        self.__complain()

    def test_failed(self):
        self.__complain()

    def test_skipped(self):
        self.__complain()

    def suite_finished(self, score):
        self.__complain()

    def __complain(self):
        raise NotKeepingScoreError('No ScoreKeeper installed; run scored tests in a keep_scorer() environment.')
    
    
class CumulativeScoreKeeper(ScoreKeeper):
    def test_passed(self):
        self.score += Score(1, 1)

    def test_failed(self):
        self.score += Score(0, 1)

    def test_skipped(self):
        self.score += Score(0, 1)

    def suite_finished(self, score):
        self.score += score

    
__scorer = create_dynamic_variable( MissingScoreKeeper() )


def score(func):
    '''
    Sets up scoring mechanism. All tests to be scored are to be placed inside a function,
    given as parameter to this function.

    Returns the final score of the tests in func.
    '''
    def passed():
        value(__scorer).test_passed()

    def failed():
        value(__scorer).test_failed()
        
    def skipped():
        value(__scorer).test_skipped()

    scorer = CumulativeScoreKeeper()
        
    with let(__scorer, scorer), on_pass(passed), on_fail(failed), on_skip(skipped):
        func()

    return scorer.score


@contextmanager
def cumulative():
    scorer = CumulativeScoreKeeper()
    
    with let(__scorer, scorer):
        yield

    value(__scorer).suite_finished(scorer.score)

    
@contextmanager
def all_or_nothing():
    scorer = CumulativeScoreKeeper()
    
    with let(__scorer, scorer):
        yield

    score = scorer.score

    if not score.is_perfect:
        score = score.zero
        
    value(__scorer).suite_finished(score)

    
@contextmanager
def weight(maximum):
    scorer = CumulativeScoreKeeper()
    
    with let(__scorer, scorer):
        yield

    score = scorer.score

    value(__scorer).suite_finished(score.rescale(maximum))
