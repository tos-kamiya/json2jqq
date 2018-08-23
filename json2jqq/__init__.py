import io
import sys

import ijson

from .version import __version__
from .uni_open import uni_open_c


def extract_paths_from_json_iter(inp):
    if isinstance(inp, str):
        inp = io.StringIO(inp)

    path_set = set()

    stack = []

    def get_path():
        q = ''.join(stack)
        if not q.startswith('.'):
            return '.' + q
        return q

    for prefix, event, value in ijson.parse(inp):
        if event == 'start_array':
            q = get_path()
            if q not in path_set:
                yield q
                path_set.add(q)
            stack.append('[]')
            q = get_path()
            if q not in path_set:
                yield q
                path_set.add(q)
        elif event == 'map_key':
            stack.pop()  # remove a previous key or a dummy (in case of the first element).
            stack.append('.' + value)
            q = get_path()
            if q not in path_set:
                yield q
                path_set.add(q)
        elif event == 'start_map':
            q = get_path()
            if q not in path_set:
                yield q
                path_set.add(q)
            stack.append(None)  # dummy
        elif event in ('end_array', 'end_map'):
            stack.pop()


def extract_path_value_pairs_from_json_iter(inp):
    if isinstance(inp, str):
        inp = io.StringIO(inp)

    path_set = set()

    stack = []

    def get_path():
        q = ''.join(stack)
        if not q.startswith('.'):
            return '.' + q
        return q

    for prefix, event, value in ijson.parse(inp):
        if event == 'start_array':
            stack.append('[]')
        elif event == 'map_key':
            stack.pop()  # remove a previous key or a dummy (in case of the first element).
            stack.append('.' + value)
        elif event == 'start_map':
            stack.append(None)  # dummy
        elif event in ('end_array', 'end_map'):
            stack.pop()
        else:
            assert event in ('boolean', 'number', 'string', 'null')
            q = get_path()
            if q not in path_set:
                yield q, value
                path_set.add(q)


__doc__ = """Extract query templates for jq tool from json data.

Usage: json2jqq [options] [<INPUT.JSON>]

Options:
  -a            Show internal (non-leaf) nodes.
  -s            Show samples.
"""


def main():
    option_all_nodes = False
    option_samples = False
    input_file = None
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
        elif input_file is None:
            input_file = a
        else:
            sys.exit("error: too many command-line argument.")
    if option_all_nodes and option_samples:
        sys.exit("error: options -a and -s are mutually exclusive.")
    if input_file is None:
        input_file = '-'

    with uni_open_c(input_file, 'r') as inp:
        if option_samples:
            for q, v in extract_path_value_pairs_from_json_iter(inp):
                vstr = 'null' if v is None else str(v)
                print('%s\t%s' % (q, vstr))
        else:
            if option_all_nodes:
                assert not option_samples
                for q in extract_paths_from_json_iter(inp):
                    print('%s\t' % q)
            else:
                for q, v in extract_path_value_pairs_from_json_iter(inp):
                    print('%s\t' % q)


if __name__ == '__main__':
    main()