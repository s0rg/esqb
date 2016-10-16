import json


class Query(object):

    def __init__(self):
        self._query = {
            'query': {
                'constant_score': {
                }
            }
        }

    def Where(self, cond):
        cond.attach(
            self._query['query']['constant_score']
        )
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
