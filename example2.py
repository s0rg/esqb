
import json
import esqb as Q


CONST_FILTER_KEYS = frozenset([
    'supplier',
    'price',
    'regions',
])


def parse_range(rd):
    if not rd:
        return None

    _min = int(rd.get('min', 0))
    _max = int(rd.get('max', 0))

    if _min == _max:
        return None

    return (
        min(_min, _max),
        max(_min, _max)
    )


def build_child_conds(suppliers, regions, price):
    subq = []

    if suppliers:
        subq.append(Q.Term('supplier_id', suppliers))

    if regions:
        subq.append(Q.Or(
            Q.Term('region_id', regions),
            # or
            Q.Not(
                Q.Exists('region_id')
            )
        ))

    prange = parse_range(price)

    if (not subq) and (not prange):
        return None

    q = Q.HasChild('price')

    if subq:
        q.set_query(Q.And(*subq))

    if prange:
        q.set_filter(
            Q.Nested('prices').set_filter(
                Q.Range('price.value', prange)
            )
        )

    return q


def build_conds(filters):
    conds = []

    if any([k in CONST_FILTER_KEYS for k in filters.keys()]):
        subq = build_child_conds(
            filters.pop('supplier', None),
            filters.pop('regions', None),
            filters.pop('price', None),
        )
        if subq:
            conds.append(subq)

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
        'par2': True,
        'par3': 'val3',
        'par4': 100,
        'par5': [1, 2, 3]
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
