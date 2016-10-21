from .base import Cond


class LogicalCond(Cond):

    def __init__(self, cond_name, *conds, **kwargs):
        super().__init__(**kwargs)
        self.cond_name = cond_name
        if len(conds) == 1 and isinstance(conds[0], list):
            self.conds = conds[0]
        else:
            self.conds = conds

    def attach(self, tree):
        root = tree.setdefault('bool', {})
        cond = root.setdefault(self.cond_name, [])
        cond.extend([
            c.attach({}) for c in self.conds
        ])
        self.fill(root)
        return tree


class And(LogicalCond):

    def __init__(self, *conds, **kwargs):
        super().__init__('must', *conds, **kwargs)


class Or(LogicalCond):

    def __init__(self, *conds, **kwargs):
        kwargs.setdefault('minimum_should_match', 1)
        super().__init__('should', *conds, **kwargs)


class Not(LogicalCond):

    def __init__(self, *conds, **kwargs):
        super().__init__('must_not', *conds, **kwargs)
