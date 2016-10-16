
import json
import esqb as Q


CONST_FILTER_KEYS = frozenset([
    'supplier',
    'price',
    'regions',
])


def parse_range(rd):
    _min = int(rd.get('min', 0))
    _max = int(rd.get('max', 0))

    if _min == _max:
        return None

    return (
        min(_min, _max),
        max(_min, _max)
    )


def build_conds(filters):
    conds = []

    if any([k in CONST_FILTER_KEYS for k in filters.keys()]):

        subq = []

        sups = filters.pop('supplier', [])
        if sups:
            subq.append(Q.Term('supplier_id', sups))

        prcs = filters.pop('price', {})
        if prcs:
            prcs = parse_range(prcs)

        regs = filters.pop('regions', [])
        if regs:
            subq.append(Q.Or(
                Q.Term('region_id', regs),
                # or
                Q.Not(
                    Q.Exists('region_id')
                )
            ))

        if subq:
            childq = Q.HasChild(
                'price',
                Q.And(*subq)
            )

            if prcs:
                childq.set_filter(
                    Q.Nested('prices').set_filter(
                        Q.Range('price.value', prcs)
                    )
                )

            conds.append(childq)

    mnfs = filters.pop('manufacturer', [])
    if mnfs:
        conds.append(Q.Term('manufacturer_id', mnfs))

    for k, v in filters.items():
        n = k.lower()

        if isinstance(v, dict):
            rt = parse_range(v)
            if rt:
                conds.append(Q.Range(n, rt))
        elif isinstance(v, str):
            conds.append(Q.Match(n, v))
        else:
            conds.append(Q.Term(n, v))

    return conds


if __name__ == '__main__':
    q = Q.QueryConst()

    filters = {
        'supplier': [1, 2, 3],
        'price': {
            'min': 10,
            'max': 1000
        },
        'regions': [10, 15, 60],
        'manufacturer': [89, 90],
        'par1': 'val1',
        'par2': 'val2',
        'par3': 'val3',
    }
    search_string = 'foo'

    filter_conds = build_conds(filters)

    if search_string:
        filter_conds.append(
            Q.Or(*[
                Q.Match(n, search_string) for n in ('foo', 'bar', 'baz')
            ])
        )
    else:
        filter_conds.append(
            Q.Term('parent', 10)
        )

    q.Where(
        Q.Or(
            Q.And(
                Q.Term('parent', 10),
                Q.IsTrue('is_parent'),
            ),
            # or
            Q.And(
                *filter_conds
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
        indent=4)
    )
