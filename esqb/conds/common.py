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


class Nested(Cond):

    def __init__(self, name, query=None):
        self._name = name
        self._query = query
        self._filter = None

    def set_query(self, cond=None):
        self._query = cond
        return self

    def set_filter(self, cond=None):
        self._filter = cond
        return self

    def attach(self, tree):
        d = {
            'path': self._name,
        }
        if self._query:
            self._query.attach(d.setdefault('query', {}))

        if self._filter:
            self._filter.attach(d.setdefault('filter', {}))

        tree['nested'] = d

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
