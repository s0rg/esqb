from .base import (
    KVCond,
    KVMeta,
    CompoundCond,
)


class Match(metaclass=KVMeta):
    pass


class Fuzzy(metaclass=KVMeta):
    pass


class Prefix(metaclass=KVMeta):
    pass


class Wildcard(metaclass=KVMeta):
    pass


class Regexp(metaclass=KVMeta):
    pass


class Type(metaclass=KVMeta):
    pass


class Exists(metaclass=KVMeta):

    def __init__(self, key, **kwargs):
        super().__init__('field', key, **kwargs)


class Term(KVCond):

    def __init__(self, key, val, **kwargs):
        super().__init__(key, val, **kwargs)
        self.term = 'terms' if isinstance(val, list) else 'term'


class IsTrue(Term):

    def __init__(self, key, **kwargs):
        super().__init__(key, True, **kwargs)


class IsFalse(Term):

    def __init__(self, key, **kwargs):
        super().__init__(key, False, **kwargs)


class Range(KVCond):

    def __init__(self, key, val, **kwargs):
        super().__init__(key, val, **kwargs)
        self.term = 'range'

    def attach(self, tree):
        _min, _max = self.val
        tree[self.term] = self.fill({
            self.key: {
                'gte': _min,
                'lte': _max
            }
        })
        return tree


class Nested(CompoundCond):

    def __init__(self, name, cond=None, **kwargs):
        super().__init__(**kwargs)
        self._name = name
        self.set_query(cond)

    def attach(self, tree):
        tree['nested'] = self.join({
            'path': self._name,
        })
        return tree
