import unittest

from json2jqq import extract_paths_from_json_iter, extract_path_value_pairs_from_json_iter


class TestStringMethods(unittest.TestCase):
    def test_empty(self):
        json_data = '{}'
        queries = list(extract_paths_from_json_iter(json_data))
        self.assertEqual(queries, ['.'])

    def test_single_map(self):
        json_data = '{"first": 1, "second": 2}'
        path_value_pairs = list(extract_path_value_pairs_from_json_iter(json_data))
        self.assertEqual(path_value_pairs, [('.first', 1), ('.second', 2)])
        paths = list(extract_paths_from_json_iter(json_data))
        self.assertEqual(paths, ['.', '.first', '.second'])

    def test_map_of_map(self):
        json_data = '''{
    "first": {"first-first": 11, "first-second": 12},
    "second": {"second-first": 21, "second-second": 22}
}'''
        path_value_pairs = list(extract_path_value_pairs_from_json_iter(json_data))
        self.assertEqual(path_value_pairs, [
            ('.first.first-first', 11), ('.first.first-second', 12),
            ('.second.second-first', 21), ('.second.second-second', 22)])
        paths = list(extract_paths_from_json_iter(json_data))
        self.assertEqual(paths, [
            '.',
                '.first',
                    '.first.first-first', '.first.first-second',
                '.second',
                    '.second.second-first', '.second.second-second'
        ])

    def test_single_array(self):
        json_data = '[1, 2, 3]'
        path_value_pairs = list(extract_path_value_pairs_from_json_iter(json_data))
        self.assertEqual(path_value_pairs, [('.[]', 1)])
        paths = list(extract_paths_from_json_iter(json_data))
        self.assertEqual(paths, ['.', '.[]'])

    def test_array_of_array(self):
        json_data = '[[1, 2, 3],[10,20,30]]'
        path_value_pairs = list(extract_path_value_pairs_from_json_iter(json_data))
        self.assertEqual(path_value_pairs, [('.[][]', 1)])
        paths = list(extract_paths_from_json_iter(json_data))
        self.assertEqual(paths, ['.', '.[]', '.[][]'])

    def test_array_of_map(self):
        json_data = '''[
  { "author": "Toshihiro Kamiya", "url": "https://github.com/tos-kamiya/json2jqq/" },
  { "author": "Toshihiro Kamiya", "url": "https://github.com/tos-kamiya/giftplayer/" }
]
'''
        path_value_pairs = list(extract_path_value_pairs_from_json_iter(json_data))
        self.assertEqual(path_value_pairs, [
            ('.[].author', "Toshihiro Kamiya"), ('.[].url', "https://github.com/tos-kamiya/json2jqq/")])
        paths = list(extract_paths_from_json_iter(json_data))
        self.assertEqual(paths, ['.', '.[]', '.[].author', '.[].url'])

    def test_null_value(self):
        json_data = '''{
    "first": {"first-first": 11, "first-second": null}
}'''
        path_value_pairs = list(extract_path_value_pairs_from_json_iter(json_data))
        self.assertEqual(path_value_pairs, [
            ('.first.first-first', 11), ('.first.first-second', None)])


if __name__ == '__main__':
    unittest.main()
