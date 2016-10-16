from esqb.conds.base import (
    Cond,
    KVCond,
)


class Exists(Cond):

    def __init__(self, key):
        self.key = key

    def attach(self, tree):
        tree['exists'] = {
            'field': self.key
        }
        return tree


class Match(KVCond):

    def attach(self, tree):
        tree['match'] = {
            self.key: self.val,
        }
        return tree


class Fuzzy(KVCond):

    def attach(self, tree):
        tree['fuzzy'] = {
            self.key: self.val,
        }
        return tree


class Term(KVCond):

    def attach(self, tree):
        key = 'terms' if isinstance(self.val, list) else 'term'
        tree[key] = {
            self.key: self.val,
        }
        return tree


class IsTrue(Term):

    def __init__(self, key):
        super().__init__(key, True)


class IsFalse(Term):

    def __init__(self, key):
        super().__init__(key, False)


class Range(KVCond):

    def attach(self, tree):
        _min, _max = self.val
        tree['range'] = {
            'gte': _min,
            'lte': _max
        }
        return tree
