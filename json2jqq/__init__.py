import io
import sys

import ijson

from .version import __version__


def extract_queries_from_json(inp, internal_nodes=False, sample_values=False):
    if isinstance(inp, str):
        inp = io.StringIO(inp)

    prefix_set = set()
    array_prefix_set = set()
    sample_value_table = {}

    for prefix, event, value in ijson.parse(inp):
        if event == 'start_array':
            array_prefix_set.add((prefix + '.item') if prefix != '' else 'item')
        elif not internal_nodes and event in ('end_array', 'start_map', 'end_map', 'map_key'):
            pass
        else:
            # 'boolean', 'number', 'string', or 'null'
            if sample_values and (value is not None or event == 'null') and prefix not in prefix_set:
                sample_value_table[prefix] = value
            prefix_set.add(prefix)

    array_prefixes = list(array_prefix_set)
    array_prefixes.sort(key=len, reverse=True)

    queries = []
    svt = {}
    for p in sorted(prefix_set):
        q = p
        for ap in array_prefixes:
            if q == ap or q.startswith(ap) and q[len(ap)] == '.':
                q = ap[:-4] + '[]' + q[len(ap):]
        q = '.' + q.replace('.[]', '[]')
        queries.append(q)
        if sample_values and p in sample_value_table:
            svt[q] = sample_value_table[p]

    if sample_values:
        return queries, svt
    else:
        return queries


__doc__ = """Extract query templates for jq tool from json data.

Usage: json2jqq [options] < data.json

Options:
  -a    Show internal (non-leaf) nodes.
  -s    Show samples (the first values for keys). 
"""


def main():
    option_all_nodes = False
    option_samples = False
    for a in sys.argv[1:]:
        if a in ('-h', '--help'):
            print(__doc__)
            return
        elif a in ('-v', '--version'):
            print("json2qq %s" % __version__)
            return
        elif a.startswith('-'):
            for op in a[1:]:
                if op == 'a':
                    option_all_nodes = True
                elif op == 's':
                    option_samples = True
                else:
                    sys.exit("error: unknown option: %s" % repr(op))
        else:
            sys.exit("error: too many command-line argument.")

    r = extract_queries_from_json(sys.stdin, internal_nodes=option_all_nodes,
            sample_values=option_samples)
    if option_samples:
        queries, sample_value_dict = r
        for q in queries:
            if q in sample_value_dict:
                v = sample_value_dict[q]
                vstr = 'null' if v is None else str(v)
                print('%s\t%s' % (q, vstr))
            else:
                print('%s\t' % q)
    else:
        queries = r
        print('\n'.join(queries))


if __name__ == '__main__':
    main()