from contextlib import contextmanager
import gzip
import sys

"""
uni_open, a unified file opener for file on filesystem, gzip archive file, 
standard in/out.

A function `uni_open` returns a file object.

>>> outp = uni_open('tmp.gz', 'wb')
>>> outp.write('I'm here.'.encode('utf-8'))
>>> outp.close()

A function `uni_open_c` works as a context of file object including closing it.

>>> with uni_open_c('tmp.gz', 'r', encoding='utf-8') as inp:
...     text = inp.read()
>>> text
I'm here.
"""

_MODE_TO_STD = {
    'a': sys.stdout,
    'ab': sys.stdout.buffer,
    'r': sys.stdin,
    'rb': sys.stdin.buffer,
    'w': sys.stdout,
    'wb': sys.stdout.buffer,
}


_MODE_TO_STD_OPEN_DATA = {
    'a': ('/dev/stdout', 'w'),
    'ab': ('/dev/stdout', 'wb'),
    'r': ('/dev/stdin', 'r'),
    'rb': ('/dev/stdin', 'rb'),
    'w': ('/dev/stdout', 'w'),
    'wb': ('/dev/stdout', 'wb'),
}


_MODE_TO_GZIP_MODE = {
    'a': 'at',
    'ab': 'a',
    'r': 'rt',
    'rb': 'r',
    'w': 'wt',
    'wb': 'w',
}


@contextmanager
def uni_open_c(fn, mode='r', encoding=None, extra_gzip_extensions=()):
    gzip_exts = ['.gz']
    gzip_exts.extend(extra_gzip_extensions)
    if fn == '-':
        assert mode in _MODE_TO_STD
        yield _MODE_TO_STD[mode]
    else:
        if any(fn.endswith(ge) for ge in gzip_exts):
            assert mode in _MODE_TO_GZIP_MODE
            m = _MODE_TO_GZIP_MODE[mode]
            f = gzip.open(fn, mode=m, encoding=encoding)
        else:
            f = open(fn, mode=mode, encoding=encoding)
        try:
            yield f
        finally:
            f.close()


def uni_open(fn, mode='r', encoding=None, extra_gzip_extensions=()):
    gzip_exts = ['.gz']
    gzip_exts.extend(extra_gzip_extensions)
    if fn == '-':
        assert mode in _MODE_TO_STD_OPEN_DATA
        fn, m = _MODE_TO_STD_OPEN_DATA[mode]
        f = open(fn, mode=m, encoding=encoding)
    elif any(fn.endswith(ge) for ge in gzip_exts):
        assert mode in _MODE_TO_GZIP_MODE
        m = _MODE_TO_GZIP_MODE[mode]
        f = gzip.open(fn, mode=m, encoding=encoding)
    else:
        f = open(fn, mode=mode, encoding=encoding)
    return f
