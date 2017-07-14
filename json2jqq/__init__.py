import io
import sys

import ijson

from .version import __version__


def extract_queries_from_json(inp, internal_nodes=False):
    if isinstance(inp, str):
        inp = io.StringIO(inp)

    prefix_set = set()
    array_prefix_set = set()

    for prefix, event, value in ijson.parse(inp):
        if event == 'start_array':
            array_prefix_set.add((prefix + '.item') if prefix != '' else 'item')
        elif not internal_nodes and event in ('end_array', 'start_map', 'end_map', 'map_key'):
            pass
        else:
            # 'boolean', 'number', 'string', or 'null'
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

Usage: json2jqq [-a] < data.json

Options:
  -a    Show internal (non-leaf) nodes.
"""


def main():
    option_all_nodes = False
    for a in sys.argv[1:]:
        if a in ('-h', '--help'):
            print(__doc__)
            return
        elif a in ('-v', '--version'):
            print("json2qq %s" % __version__)
            return
        elif a == '-a':
            option_all_nodes = True
        else:
            sys.exit("error: too many command-line argument.")

    qs = extract_queries_from_json(sys.stdin, internal_nodes=option_all_nodes)
    print('\n'.join(qs))



if __name__ == '__main__':
    main()