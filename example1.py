
import json
import esqb as Q


if __name__ == '__main__':
    q = Q.Query()

    q.Where(
        Q.Or(
            Q.Match('foo', 'bar'),
            Q.And(
                Q.HasChild(
                    'child_type',
                    Q.And(
                        Q.Term('doo', 'daz'),
                        Q.Match('mee', 'moo'),
                        Q.Range('price', (100, 500)),
                        Q.Not(
                            Q.Term('my', 'val'),
                        ),
                    ),
                ),
                Q.Term('foo', 'bar'),
                Q.Fuzzy('foozy', 'whoozy'),
                Q.Range('key', (0, 10)),
                Q.IsTrue('bool_key'),
                Q.IsFalse('bool_key2'),
                Q.Exists('foo'),
            )
        )
    )

    q.Where(
        Q.And(
            Q.HasParent(
                'parent_type',
                Q.Or(
                    Q.Term('biz', 'buz'),
                    Q.Match('you', 'me'),
                )
            )
        )
    )

    q.Sort(
        'name',
        'id',
        date='desc',
        key='asc'
    )

    print(json.dumps(
        json.loads(repr(q)),
        indent=4,
        sort_keys=True
    ))
