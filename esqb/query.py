import json


class BaseQuery(object):
    '''
    Base for all queries
    '''

    def __init__(self, name, constant=False, has_filter=True, **kwargs):
        '''
        `name` - root key
        `constant` - adds 'constant_score' in query
        `has_filter` - adds filter section
        key-word params going as-is to dest query
        '''
        self._query = kwargs
        r = self._query.setdefault(name, {})
        if constant:
            r = r.setdefault('constant_score', {})
        if has_filter:
            r = r.setdefault('filter', {})
        self._root = r

    def Where(self, cond, **kwargs):
        '''
        Attaches given `cond` to self root path,
        and updates it with given kwargs
        '''
        cond.attach(self._root)
        self._root.update(kwargs)
        return self

    def Sort(self, *args, **kwargs):
        '''
        Adds sorting to query
        '''
        s = self._query.setdefault('sort', [])
        for a in args:
            s.append(a)
        for k, v in kwargs.items():
            s.append({k: v})
        return self

    def Size(self, size):
        self._query['size'] = int(size)
        return self

    def From(self, offset):
        self._query['from'] = int(offset)
        return self

    def __repr__(self):
        return json.dumps(self._query)


class Query(BaseQuery):

    def __init__(self, **kwargs):
        super().__init__('query', **kwargs)


class QueryConst(BaseQuery):

    def __init__(self, **kwargs):
        super().__init__('query', True, **kwargs)


class QueryAgg(BaseQuery):

    def __init__(self, **kwargs):
        super().__init__('aggs', False, False, **kwargs)
