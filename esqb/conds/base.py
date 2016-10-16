

class Cond(object):

    def attach(self, tree=None):
        raise NotImplemented('Cond.attach()')


class KVCond(Cond):

    def __init__(self, key, val):
        self.key = key
        self.val = val


class HasRelationCond(Cond):

    def __init__(self, who, wtype, cond):
        self.who = who
        self.wtype = wtype
        self.cond = cond
        self._filter = None

    def attach(self, tree):
        d = {
            'type': self.wtype,
            'query': self.cond.attach({}),
        }
        if self._filter:
            self._filter.attach(
                d.setdefault('filter', {})
            )

        tree[self.who] = d
        return tree

    def set_filter(self, cond):
        self._filter = cond
        return self
