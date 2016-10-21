import json


class BaseQuery(object):

    def __init__(self, name, constant=False, has_filter=True, **kwargs):
        self._query = kwargs
        r = self._query.setdefault(name, {})
        if constant:
            r = r.setdefault('constant_score', {})
        if has_filter:
            r = r.setdefault('filter', {})
        self._root = r

    def Where(self, cond, **kwargs):
        cond.attach(self._root)
        self._root.update(kwargs)
        return self

    def Sort(self, *args, **kwargs):
        s = self._query.setdefault('sort', [])
        for a in args:
            s.append(a)
        for k, v in kwargs.items():
            s.append({k: v})
        return self

    def Limit(self, limit):
        self._query['size'] = int(limit)
        return self

    def Offset(self, offset):
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
