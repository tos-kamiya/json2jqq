import sys

import ijson

from .version import __version__


def extract_queries_from_json(inp):
    prefix_set = set()
    array_prefix_set = set()

    for prefix, event, value in ijson.parse(inp):
        if event == 'start_array':
            array_prefix_set.add((prefix + '.item') if prefix != '' else 'item')
        elif event == 'end_array':
            pass
        elif event not in ('start_map', 'end_map', 'map_key'):
            prefix_set.add(prefix)

    array_prefixes = list(array_prefix_set)
    array_prefixes.sort(key=len, reverse=True)

    queries = []
    for p in sorted(prefix_set):
        for ap in array_prefixes:
            if p == ap or p.startswith(ap) and p[len(ap)] == '.':
                p = ap[:-4] + '[]' + p[len(ap):]
        p = '.' + p.replace('.[]', '[]')
        queries.append(p)

    return queries


__doc__ = """Extract query templates for jq tool from json data.

Usage: json2jqq < data.json
"""


def main():
    if len(sys.argv) >= 2:
        if sys.argv[1] in ('-h', '--help'):
            print(__doc__)
            return
        elif sys.argv[1] in ('-v', '--version'):
            print("json2qq %s" % __version__)
            return

    qs = extract_queries_from_json(sys.stdin)
    print('\n'.join(qs))



if __name__ == '__main__':
    main()