

class Cond(object):

    def attach(self, tree=None):
        raise NotImplemented('Cond.attach()')


class CompoundCond(Cond):
    _filter = None
    _query = None

    def set_filter(self, cond=None):
        self._filter = cond
        return self

    def set_query(self, cond=None):
        self._query = cond
        return self

    def join(self, upper):
        if self._query:
            self._query.attach(
                upper.setdefault('query', {})
            )

        if self._filter:
            self._filter.attach(
                upper.setdefault('filter', {})
            )
        return upper


class KVCond(Cond):

    def __init__(self, key, val):
        self.key = key
        self.val = val


class HasRelationCond(CompoundCond):

    def __init__(self, who, wtype, cond):
        self.who = who
        self.wtype = wtype
        self.set_query(cond)

    def attach(self, tree):
        tree[self.who] = self.join({
            'type': self.wtype,
        })
        return tree
