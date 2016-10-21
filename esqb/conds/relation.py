from .base import HasRelationCond


class HasChild(HasRelationCond):

    def __init__(self, child, cond=None, **kwargs):
        super().__init__('has_child', child, cond, **kwargs)


class HasParent(HasRelationCond):

    def __init__(self, parent, cond=None, **kwargs):
        super().__init__('has_parent', parent, cond, **kwargs)
