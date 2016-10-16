

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

    def attach(self, tree):
        tree[self.who] = {
            'type': self.wtype,
            'query': self.cond.attach({}),
        }
        return tree
