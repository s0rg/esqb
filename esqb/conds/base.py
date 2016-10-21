

class Cond(object):
    '''
    Conditional base
    '''
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def fill(self, d=None):
        '''
        fills the given dict (or new if none given) with self.kwargs
        returns updated dict
        '''
        d = d or {}
        d.update(self.kwargs)
        return d

    def attach(self, tree=None):
        '''
        virtual ;)

        Insert self in dict `tree`
        returns changed tree back
        '''
        raise NotImplemented('Cond.attach()')


class CompoundCond(Cond):
    '''
    Compound mixin, contains 'filter' and/or 'query' conditionals
    '''
    _filter = None
    _query = None

    def set_filter(self, cond=None):
        self._filter = cond
        return self

    def set_query(self, cond=None):
        self._query = cond
        return self

    def join(self, upper):
        '''
        'inject' self components (query and/or filter)
        into `upper` dict
        returns changed (or not) dict
        '''
        if self._query:
            self._query.attach(
                upper.setdefault('query', {})
            )

        if self._filter:
            self._filter.attach(
                upper.setdefault('filter', {})
            )
        return self.fill(upper)


class KVCond(Cond):
    '''
    Base for most conditionals
    '''
    term = None

    def __init__(self, key, val, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.val = val

    def attach(self, tree):
        tree[self.term] = self.fill({
            self.key: self.val
        })
        return tree


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


class KVMeta(type):
    '''
    Helper meta to build simple queries, creates child of KVCond,
    with term set to lowercase class name
    '''

    def __new__(cls, name, bases, attrs):
        bases += (KVCond,)
        attrs['term'] = name.lower()
        return super(KVMeta, cls).__new__(cls, name, bases, attrs)
