import json
import random
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


ELASTIC_NOM_TYPE = 'nom'
ELASTIC_PRC_TYPE = 'nom_prices'


def get_elastic_uri():
    return 'http://localhost:9200'


def send_data(uri, method='GET', data=None):
    if not uri.startswith('http'):
        return

    header = {'Content-Type': 'application/json; charset=utf-8'}

    if data is not None:
        if isinstance(data, dict):
            data = json.dumps(data)
        data = data.encode('utf8') + b'\n'

    req = Request(uri, data=data, headers=header, method=method)
    try:
        f = urlopen(req)
        return f.read().decode('utf8')
    except URLError as e:
        print('elastic error: {}'.format(str(e)))
        return


def create_index(uri, index):
    index_options = {
        "mappings": {
            ELASTIC_NOM_TYPE: {
                "_all": {"enabled": False},
                "properties": {
                    "name": {"type": "string"},
                    "man_id": {"type": "integer"},
                    "man_name": {"type": "string"},
                    "man_code": {"type": "string"},
                    "actual": {"type": "boolean"},
                    "has_childs": {"type": "boolean"},
                    "code": {"type": "string"},
                    "parent": {"type": "integer"},
                }
            },
            ELASTIC_PRC_TYPE: {
                "_parent": {"type": ELASTIC_NOM_TYPE},
                "_all": {"enabled": False},
                "dynamic": False,
                "properties": {
                    "sup_id": {"type": "integer"},
                    "sup_name": {"type": "string"},
                    "regions": {
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "prices": {
                        "type": "nested",
                        "properties": {
                            "value": {"type": "float"},
                            "kind": {"type": "integer"},
                        }
                    }
                }
            }
        }
    }
    send_data(uri + '/' + index, 'PUT', index_options)


if __name__ == '__main__':

    def make_index(uri):
        index = 'test'
        create_index(uri, index)
        return index

    def drop_index(uri, index):
        send_data(uri + '/' + index, 'DELETE')

    def gen_noms(count=10, parent=None):
        mans = [
            (1, 'man1'),
            (2, 'man2'),
            (3, 'man3'),
        ]

        if parent:
            def make_name(idx):
                return '{}-nom-{}'.format(parent, idx)
        else:
            def make_name(idx):
                return 'nom-{}'.format(idx)

        for idx in range(count):
            name = make_name(idx)

            man_id, man_name = random.choice(mans)

            nom = {
                "name": name,
                "man_id": man_id,
                "man_name": man_name,
                "man_code": '{}-{}'.format(man_name, name),
                "actual": random.choice((True, False)),
                "has_childs": False,
                "code": 'nom-code-{}'.format(idx),
                "parent": parent or 0,
            }

            yield nom

    def make_prices():
        sups = [
            (1, 'sup1', 1, '1,2,3'),
            (2, 'sup2', 10, '4,5,6'),
        ]

        price = random.randint(10, 100)

        for sid, name, fac, regs in sups:
            doc = {
                "sup_id": sid,
                "sup_name": name,
                "regions": regs,
                "prices": [
                    {
                        'kind': 1,
                        'value': price*fac
                    },
                ]
            }
            yield doc

    def fill_index(uri, index):
        bulk = []

        for idx, doc in enumerate(gen_noms()):
            bulk.append(json.dumps({
                'index': {
                   '_index': index,
                   '_type': ELASTIC_NOM_TYPE,
                   '_id': idx
                }
            }))

            bulk.append(json.dumps(doc))

            for price in make_prices():
                bulk.append(json.dumps({
                    'index': {
                        '_index': index,
                        '_type': ELASTIC_PRC_TYPE,
                        '_id': '{}-{}'.format(idx, price['sup_id']),
                        '_parent': idx,
                    }
                }))
                bulk.append(json.dumps(price))

        send_data(uri + '/_bulk', 'POST', '\n'.join(bulk))

    def run_query(uri, index, query):
        return send_data(uri + '/' + index + '/_search', 'POST', query)

    def main():
        es_uri = get_elastic_uri()
        index = make_index(es_uri)

        print('filling...')
        fill_index(es_uri, index)

        while True:
            print('enter search request:')
            req = input().strip()
            if not req:
                break
            print('\nrunning:\n')
            resp = json.loads(run_query(es_uri, index, req))

            if resp['timed_out']:
                print('Timed-out :(')

            print(json.dumps(resp['hits'], indent=4))
            print()

        print('press enter to destroy index...')
        input()

        drop_index(es_uri, index)

        return

    main()
