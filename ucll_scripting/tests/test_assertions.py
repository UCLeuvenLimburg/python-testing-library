from ucll_scripting.testing.assertions import *
import unittest


class AssertionTests(unittest.TestCase):
    def test_equality(self):
        assert equal(expected=4, actual=4)
        assert equal(expected='a', actual='a')
        assert equal(expected=[1, 2, 3], actual=[1, 2, 3])

    def test_inequality(self):
        assert not equal(expected=1, actual=3)
        assert not equal(expected='a', actual='b')
        assert not equal(expected=5, actual='b')
        assert not equal(expected=[1, 2, 3], actual=[1, 2])
        assert not equal(expected=[1, 2, 3], actual=[1, 2, 4])
        assert not equal(expected=[1, 2, 3], actual=[3, 2, 1])

    def test_truthy(self):
        assert truthy(actual=True)
        assert truthy(actual='x')
        assert truthy(actual=1)
        assert truthy(actual=[5])
        assert truthy(actual={'a'})

        assert not truthy(actual=False)
        assert not truthy(actual=0)
        assert not truthy(actual='')
        assert not truthy(actual=[])
        assert not truthy(actual={})

    def test_falsey(self):
        assert not falsey(actual=True)
        assert not falsey(actual='x')
        assert not falsey(actual=1)
        assert not falsey(actual=[5])
        assert not falsey(actual={'a'})

        assert falsey(actual=False)
        assert falsey(actual=0)
        assert falsey(actual='')
        assert falsey(actual=[])
        assert falsey(actual={})
        
    def test_same_truthiness(self):
        assert same_truthiness(expected=True, actual=True)
        assert same_truthiness(expected=False, actual=False)
        assert same_truthiness(expected=False, actual=0)
        assert same_truthiness(expected='', actual={})

        assert not same_truthiness(expected=True, actual=False)
        assert not same_truthiness(expected=0, actual=5)
        assert not same_truthiness(expected=True, actual={})
        assert not same_truthiness(expected='bc', actual='')

    def test_permutation(self):
        assert permutation(expected=[], actual=[])
        assert permutation(expected=[1], actual=[1])
        assert permutation(expected=[1, 2], actual=[1, 2])
        assert permutation(expected=[1, 2], actual=[2, 1])
        assert permutation(expected=[1, 2, 3], actual=[2, 1, 3])
        assert permutation(expected=[1, 1, 2, 2, 3, 3], actual=[1, 2, 3, 1, 2, 3])

        assert not permutation(expected=[], actual=[1])
        assert not permutation(expected=[1], actual=[])
        assert not permutation(expected=[1, 2], actual=[1, 2, 2])
