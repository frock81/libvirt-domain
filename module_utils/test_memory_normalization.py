#!/usr/bin/env python3

import unittest

from memory_normalizer import MemoryNormalizer

class TestMemoryNormalizer(unittest.TestCase):

    INTERMEDIATE = {
        'element_name': 'domain',
        'attributes': [{'attribute_name': 'type', 'attribute_value': 'kvm'}],
        'children': [{
            'element_name': 'name',
            'text': 'vm-foo'
        },{
            'element_name': 'uuid',
            'text': '6404f873-9fae-5bd4-b141-5d1b1bd27df9'
        },{
            'element_name': 'title',
            'text': 'Domain short description'
        },{
            'element_name': 'description',
            'text': 'Some human readable long description for the domain.'
        },{
            'element_name': 'memory',
            'text': '1',
            'attributes': [{'attribute_name': 'unit', 'attribute_value': 'GiB'}]
        },{
            'element_name': 'currentMemory',
            'text': '512',
            'attributes': [{'attribute_name': 'unit', 'attribute_value': 'MiB'}]
        },{
            'element_name': 'vcpu',
            'text': '2',
            'attributes': [{
                'attribute_name': 'current', 'attribute_value': '1'
            }]
        },{
            'element_name': 'os',
            'children': [{
                'element_name': 'type',
                'text': 'hvm'
            }]
        }]
    }

    def setUp(self):
        self.memory_normalizer = MemoryNormalizer(intermediate=self.INTERMEDIATE)

    def test_foo(self):
        self.assertIsInstance(self.memory_normalizer.normalized, dict)
        self.assertIn('children', self.memory_normalizer.normalized)
        total_children = 8
        self.assertEqual(len(self.memory_normalizer.normalized['children']), 8)
        memory_element = next(filter(lambda child : child['element_name'] ==
            'memory', self.memory_normalizer.normalized['children']))
        self.assertIsNotNone(memory_element)

if __name__ == '__main__':
    unittest.main()