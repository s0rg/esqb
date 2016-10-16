from esqb.conds.base import HasRelationCond


class HasChild(HasRelationCond):

    def __init__(self, child, cond):
        super().__init__('has_child', child, cond)


class HasParent(HasRelationCond):

    def __init__(self, parent, cond):
        super().__init__('has_parent', parent, cond)
