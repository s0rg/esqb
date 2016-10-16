
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
        subq.append(Q.Term('sup_id', suppliers))

    if regions:
        subq.append(Q.Or(
            Q.Term('regions', regions),
            # or
            Q.Not(
                Q.Exists('regions')
            )
        ))

    prange = parse_range(price)

    if (not subq) and (not prange):
        return None

    q = Q.HasChild('nom_prices')

    if subq:
        q.set_query(Q.And(*subq))

    if prange:
        q.set_filter(
            Q.Nested('prices').set_filter(
                Q.Range('prices.value', prange)
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
        conds.append(Q.Term('man_id', mnfs))

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
        #'supplier': 2,
        'price': {
            'min': 1,
            'max': 30
        },
        #'regions': [10, 15, 60],
        'manufacturer': 3,
        #'par1': 'val1',
        #'par2': True,
        #'par3': 'val3',
        #'par4': 100,
        #'par5': [1, 2, 3],
        #'actual': False,
    }
    search_string = None  # 'foo'
    parent = 0

    filter_conds = build_conds(filters)

    if search_string:
        filter_conds.append(
            Q.Or(*[
                Q.Match(n, search_string) for n in ('name', 'man_code', 'code')
            ])
        )

    else:
        filter_conds.append(
            Q.Term('parent', parent)
        )

    q.Where(
        Q.Or(
            Q.And(
                Q.Term('parent', parent),
                Q.IsTrue('is_parent'),
            ),
            # or
            Q.And(
                *filter_conds
            )
        )
    )

    q.Sort('name')

    '''
    print(json.dumps(
        json.loads(repr(q)),
        indent=4)
    )
    '''
    print(repr(q))
