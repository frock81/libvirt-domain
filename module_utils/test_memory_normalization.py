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

    def test_get_memory_element(self):
        method = getattr(self.memory_normalizer, '_get_memory_element', None)
        self.assertIsNotNone(method)
        memory_element = self.memory_normalizer._get_memory_element(
            intermediate=self.INTERMEDIATE)
        self.assertIsInstance(memory_element, dict)
        self.assertIn('element_name', memory_element)
        self.assertEqual(memory_element['element_name'], 'memory')
        self.assertIn('attributes', memory_element)
        self.assertIsInstance(memory_element['attributes'], list)

    def test_get_attribute_from_element(self):
        element = {
            'element_name': 'memory',
            'text': '1',
            'attributes': [{'attribute_name': 'unit', 'attribute_value': 'GiB'}]
        }
        method = getattr(self.memory_normalizer, '_get_attribute_from_element',
            None)
        self.assertIsNotNone(method)
        self.assertTrue(self.memory_normalizer,
            '._get_attribute_from_element()')
        attribute_name = 'unit'
        attribute_value = 'GiB'
        attribute = self.memory_normalizer._get_attribute_from_element(
            element=element, attribute_name=attribute_name)
        self.assertIsNotNone(attribute)
        self.assertIn('attribute_name', attribute)
        self.assertEqual(attribute['attribute_name'], attribute_name)
        self.assertIn('attribute_value', attribute)
        self.assertEqual(attribute['attribute_value'], attribute_value)

    def test_get_memory_value(self):
        method = getattr(self.memory_normalizer, '_get_memory_value',
            None)
        self.assertIsNotNone(method)
        element = {
            'element_name': 'memory',
            'text': '1',
            'attributes': [{'attribute_name': 'unit', 'attribute_value': 'GiB'}]
        }
        memory_value = self.memory_normalizer._get_memory_value(memory_element=
            element)
        self.assertIsNotNone(memory_value)
        self.assertEqual(memory_value, '1')

    def test_get_memory_unit(self):
        method = getattr(self.memory_normalizer, '_get_memory_unit',
            None)
        self.assertIsNotNone(method)
        unit_attribute = {'attribute_name': 'unit', 'attribute_value': 'GiB'}
        unit_value = self.memory_normalizer._get_memory_unit(unit_attribute=
            unit_attribute)
        self.assertIsNotNone(unit_value)
        self.assertEqual(unit_value, 'GiB')

    def test_convert_to_kibibyte(self):
        method = getattr(self.memory_normalizer, '_convert_to_kibibyte',
            None)
        self.assertIsNotNone(method)
        self._test_kibibyte_conversion(value=1, unit='b', expected=1)
        self._test_kibibyte_conversion(value=1, unit='B', expected=1)
        self._test_kibibyte_conversion(value=1, unit='KiB', expected=1)
        self._test_kibibyte_conversion(value=1, unit='k', expected=1)
        self._test_kibibyte_conversion(value=1, unit='K', expected=1)
        self._test_kibibyte_conversion(value=1, unit='KB', expected=1)
        self._test_kibibyte_conversion(value=1, unit='kb', expected=1)
        self._test_kibibyte_conversion(value=1000, unit='kb', expected=977)
        self._test_kibibyte_conversion(value=1, unit='MiB', expected=1024)
        self._test_kibibyte_conversion(value=1, unit='m', expected=1024)
        self._test_kibibyte_conversion(value=1, unit='M', expected=1024)
        self._test_kibibyte_conversion(value=1, unit='MB', expected=977)
        self._test_kibibyte_conversion(value=1, unit='mb', expected=977)
        self._test_kibibyte_conversion(value=1, unit='GiB', expected=1048576)
        self._test_kibibyte_conversion(value=1, unit='g', expected=1048576)
        self._test_kibibyte_conversion(value=1, unit='G', expected=1048576)
        self._test_kibibyte_conversion(value=1, unit='GB', expected=976563)
        self._test_kibibyte_conversion(value=1, unit='gb', expected=976563)
        self._test_kibibyte_conversion(value=1, unit='TiB', expected=1073741824)
        self._test_kibibyte_conversion(value=1, unit='t', expected=1073741824)
        self._test_kibibyte_conversion(value=1, unit='T', expected=1073741824)
        self._test_kibibyte_conversion(value=1, unit='TB', expected=976562500)
        self._test_kibibyte_conversion(value=1, unit='tb', expected=976562500)

    def _test_kibibyte_conversion(self, value, unit, expected):
        result = self.memory_normalizer._convert_to_kibibyte(value=value, unit=unit)
        self.assertEqual(result, expected)

    def test_normalize_element(self):
        method = getattr(self.memory_normalizer, '_normalize_element',
            None)
        self.assertIsNotNone(method)
        element = {
            'element_name': 'memory',
            'text': '1',
            'attributes': [{
                'attribute_name': 'unit',
                'attribute_value': 'GiB'
            }]
        }
        element = self.memory_normalizer._normalize_element(element=element)
        element_attributes = element['attributes']
        unit_attribute = element_attributes[0]
        self.assertIn('attribute_value', unit_attribute)
        self.assertEqual(unit_attribute['attribute_value'], 'KiB')
        self.assertIn('text', element)
        self.assertEqual(element['text'], str(1*1024*1024))

    # def test_is_memory_normalized(self):
    #     memory_element = next(filter(lambda x: x['element_name'] == 'memory',
    #         self.memory_normalizer.normalized['children']))
    #     self.assertEqual(memory_element['text'], 1*1024*1024)

if __name__ == '__main__':
    unittest.main()