from .base import CompoundCond


class HasRelationCond(CompoundCond):
    '''
    Base for relation conditionals
    '''

    def __init__(self, who, wtype, cond, **kwargs):
        super().__init__(**kwargs)
        self.who = who
        self.wtype = wtype
        self.set_query(cond)

    def attach(self, tree):
        tree[self.who] = self.join({
            'type': self.wtype,
        })
        return tree


class HasChild(HasRelationCond):

    def __init__(self, child, cond=None, **kwargs):
        super().__init__('has_child', child, cond, **kwargs)


class HasParent(HasRelationCond):

    def __init__(self, parent, cond=None, **kwargs):
        super().__init__('has_parent', parent, cond, **kwargs)
