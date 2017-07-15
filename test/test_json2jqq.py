import unittest

from json2jqq import extract_queries_from_json


class TestStringMethods(unittest.TestCase):
    def test_empty(self):
        json_data = '{}'
        queries = extract_queries_from_json(json_data)
        self.assertEqual(queries, [])
        queries = extract_queries_from_json(json_data, internal_nodes=True)
        self.assertEqual(queries, ['.'])

    def test_single_map(self):
        json_data = '{"first": 1, "second": 2}'
        queries = extract_queries_from_json(json_data)
        self.assertEqual(queries, ['.first', '.second'])
        queries = extract_queries_from_json(json_data, internal_nodes=True)
        self.assertEqual(queries, ['.', '.first', '.second'])

    def test_map_of_map(self):
        json_data = '''{
    "first": {"first-first": 11, "first-second": 12}, 
    "second": {"second-first": 21, "second-second": 22}
}'''
        queries = extract_queries_from_json(json_data)
        self.assertEqual(queries, ['.first.first-first', '.first.first-second', '.second.second-first', '.second.second-second'])
        queries = extract_queries_from_json(json_data, internal_nodes=True)
        self.assertEqual(queries, [
            '.',
                '.first',
                    '.first.first-first', '.first.first-second',
                '.second',
                    '.second.second-first', '.second.second-second'
        ])

    def test_single_array(self):
        json_data = '[1, 2, 3]'
        queries = extract_queries_from_json(json_data)
        self.assertEqual(queries, ['.[]'])
        queries = extract_queries_from_json(json_data, internal_nodes=True)
        self.assertEqual(queries, ['.', '.[]'])

    def test_array_of_array(self):
        json_data = '[[1, 2, 3],[10,20,30]]'
        queries = extract_queries_from_json(json_data)
        self.assertEqual(queries, ['.[][]'])
        queries = extract_queries_from_json(json_data, internal_nodes=True)
        self.assertEqual(queries, ['.', '.[]', '.[][]'])

    def test_null_value(self):
        json_data = '''{
    "first": {"first-first": 11, "first-second": null}, 
    "second": {"second-first": 21, "second-second": 22}
}'''
        queries = extract_queries_from_json(json_data)
        self.assertEqual(queries, ['.first.first-first', '.first.first-second', '.second.second-first', '.second.second-second'])
        queries = extract_queries_from_json(json_data, internal_nodes=True)
        self.assertEqual(queries, [
            '.',
                '.first',
                    '.first.first-first', '.first.first-second',
                '.second',
                    '.second.second-first', '.second.second-second'
        ])
        q, d = extract_queries_from_json(json_data, sample_values=True)
        self.assertEqual(q, ['.first.first-first', '.first.first-second', '.second.second-first', '.second.second-second'])
        self.assertEqual(d, {'.first.first-first': 11, '.first.first-second': None, '.second.second-first':21, '.second.second-second':22 })
        q, d = extract_queries_from_json(json_data, internal_nodes=True, sample_values=True)
        self.assertEqual(q, [
            '.',
                '.first',
                    '.first.first-first', '.first.first-second',
                '.second',
                    '.second.second-first', '.second.second-second'
        ])
        self.assertEqual(d, {'.first.first-first': 11, '.first.first-second': None, '.second.second-first':21, '.second.second-second':22 })


if __name__ == '__main__':
    unittest.main()
