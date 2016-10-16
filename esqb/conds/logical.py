from esqb.conds.base import Cond


class And(Cond):

    def __init__(self, *conds):
        self.conds = conds

    def attach(self, tree):
        bool_root = tree.setdefault('bool', {})
        must = bool_root.setdefault('must', [])
        must.extend([
            c.attach({}) for c in self.conds
        ])
        return tree


class Or(Cond):

    def __init__(self, *conds, **kwargs):
        self.conds = conds
        self.match = kwargs.get('match', 1)

    def attach(self, tree):
        bool_root = tree.setdefault('bool', {
            'minimum_should_match': self.match
        })
        should = bool_root.setdefault('should', [])
        should.extend([
            c.attach({}) for c in self.conds
        ])
        return tree


class Not(Cond):

    def __init__(self, *conds):
        self.conds = conds

    def attach(self, tree):
        bool_root = tree.setdefault('bool', {})
        must_not = bool_root.setdefault('must_not', [])
        must_not.extend([
            c.attach({}) for c in self.conds
        ])
        return tree
