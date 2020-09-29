#!/usr/bin/env python3

import unittest
import copy

from lxml import etree

from intermediate_to_xml import IntermediateToXml

class TestIntermediateToXml(unittest.TestCase):

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

    @classmethod
    def setUpClass(cls):
        cls.intermediate_to_xml = IntermediateToXml(
            intermediate_representation=cls.INTERMEDIATE)
        cls.xml_tree = etree.fromstring(cls.intermediate_to_xml.xml)

    def test_domain_element(self):
        self.assertEqual(self.xml_tree.tag, 'domain')
        domain_type = self.xml_tree.get('type')
        self.assertEqual(domain_type, 'kvm')

    def test_domain_name_element(self):
        query = '/domain/name'
        query_result = self.xml_tree.xpath(query)
        self.assertEqual(len(query_result), 1)
        name_element = query_result[0]
        self.assertEqual(name_element.tag, 'name')
        self.assertEqual(name_element.text, 'vm-foo')

    def test_with_uuid(self):
        query = '/domain/uuid'
        query_result = self.xml_tree.xpath(query)
        self.assertEqual(len(query_result), 1)
        element = query_result[0]
        self.assertEqual(element.tag, 'uuid')
        self.assertEqual(element.text, '6404f873-9fae-5bd4-b141-5d1b1bd27df9')

    def test_null_uuid(self):
        intermediate = copy.deepcopy(self.INTERMEDIATE)
        uuid_element_index = 1
        intermediate['children'][uuid_element_index]['text'] = None
        intermediate_to_xml = IntermediateToXml(
            intermediate_representation=intermediate)
        tree = etree.fromstring(intermediate_to_xml.xml)
        query = '/domain/uuid'
        query_result = tree.xpath(query)
        self.assertEqual(len(query_result), 1)
        element = query_result[0]
        self.assertEqual(element.tag, 'uuid')
        self.assertEqual(element.text, None)

    def test_without_uuid(self):
        intermediate = copy.deepcopy(self.INTERMEDIATE)
        uuid_element_index = 1
        intermediate['children'].pop(uuid_element_index)
        intermediate_to_xml = IntermediateToXml(
            intermediate_representation=intermediate)
        xml_tree = etree.fromstring(intermediate_to_xml.xml)
        query = '/domain/uuid'
        query_result = xml_tree.xpath(query)
        self.assertFalse(query_result)

    def test_vcpu(self):
        query = '/domain/vcpu'
        query_result = self.xml_tree.xpath(query)
        self.assertEqual(len(query_result), 1)
        vcpu_element = query_result[0]
        self.assertEqual(vcpu_element.tag, 'vcpu')
        self.assertEqual(vcpu_element.text, '2')
        vcpu_current = vcpu_element.get('current')
        self.assertEqual(vcpu_current, '1')

    def test_memory(self):
        query = '/domain/memory'
        query_result = self.xml_tree.xpath(query)
        self.assertEqual(len(query_result), 1)
        memory_element = query_result[0]
        self.assertEqual(memory_element.tag, 'memory')
        self.assertEqual(memory_element.text, '1')
        memory_unit = memory_element.get('unit')
        self.assertEqual(memory_unit, 'GiB')

    def test_os_type(self):
        query = '/domain/os'
        query_result = self.xml_tree.xpath(query)
        self.assertEqual(len(query_result), 1)
        os_element = query_result[0]
        self.assertEqual(len(os_element), 1)
        type_element = os_element[0]
        self.assertEqual(type_element.tag, 'type')
        self.assertEqual(type_element.text, 'hvm')

if __name__ == '__main__':
    unittest.main()
