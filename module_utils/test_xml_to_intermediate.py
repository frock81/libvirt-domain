#!/usr/bin/env python3

import unittest
import libvirt
import copy

from lxml import etree
from io import StringIO, BytesIO

from libvirt_domain import LibvirtDomain
from libvirt_connector import LibvirtConnector
from xml_to_intermediate_converter import XmlToIntermediateConverter

class TestXmlToIntermediate(unittest.TestCase):

    XML_DOMAIN_NAME = 'vm-foo'
    XML_DOMAIN_UUID = '6404f873-9fae-5bd4-b141-5d1b1bd27df9'
    XML_DOMAIN_TITLE = 'Domain short description'
    XML_DOMAIN_DESCRIPTION = 'Some long human readable description for the domain.'
    XML_VCPU_MAX = '2'
    XML_VCPU_CURRENT = '1'
    XML_MEMORY_MAX = '1'
    XML_MEMORY_MAX_UNIT = 'GiB'
    XML_MEMORY_CURRENT = '512'
    XML_MEMORY_CURRENT_UNIT = 'MiB'

    @classmethod
    def setUpClass(cls):
        xml_file = 'domain_description.xml'
        cls.encoding = 'UTF-8'
        parser = etree.XMLParser(encoding=cls.encoding)
        cls.xml_tree = etree.parse(xml_file, parser)
        xml_string = etree.tostring(cls.xml_tree.getroot()).decode(cls.encoding)
        cls.xml_to_intermediate_converter = XmlToIntermediateConverter(
            xml_string=xml_string)

    def test_representation_property(self):
        self.assertTrue(hasattr(self.xml_to_intermediate_converter,
            'representation'))
        self.assertIsInstance(self.xml_to_intermediate_converter.representation,
            dict)

    def test_domain_element(self):
        self.assertIn('element_name',
            self.xml_to_intermediate_converter.representation)
        self.assertEqual(self.xml_to_intermediate_converter
            .representation['element_name'], 'domain')
        self.assertIn('attributes', self.xml_to_intermediate_converter
            .representation)
        attributes_list = (self.xml_to_intermediate_converter
            .representation['attributes'])
        self.assertIsInstance(attributes_list, list)
        self.assertEqual(len(attributes_list), 1)
        domain_type_dict = attributes_list[0]
        self.assertIsInstance(domain_type_dict, dict)
        self.assertIn('attribute_name', domain_type_dict)
        self.assertEqual(domain_type_dict['attribute_name'], 'type')
        self.assertIn('attribute_value', domain_type_dict)
        self.assertEqual(domain_type_dict['attribute_value'], 'kvm')
        self.assertIn('children',
            self.xml_to_intermediate_converter.representation)
        self.assertIsInstance(self.xml_to_intermediate_converter
            .representation['children'], list)

    def test_name(self):
        self.__test_domain_child_element(element_name='name',
            element_value=self.XML_DOMAIN_NAME)

    def test_uuid(self):
        self.__test_domain_child_element(element_name='uuid',
            element_value=self.XML_DOMAIN_UUID)

    def test_title(self):
        self.__test_domain_child_element(element_name='title',
            element_value=self.XML_DOMAIN_TITLE)

    def test_without_title(self):
        self.__test_domain_child_without_element(element_name='description')

    def test_with_description(self):
        self.__test_domain_child_element(element_name='description',
            element_value=self.XML_DOMAIN_DESCRIPTION)

    def test_without_description(self):
        self.__test_domain_child_without_element(element_name='description')

    def test_vcpus(self):
        element = self.__test_domain_child_element(element_name='vcpu',
            element_value=self.XML_VCPU_MAX)
        attribute_spec = [{'key': 'current', 'value': self.XML_VCPU_CURRENT}]
        self.__test_attributes(element=element, attribute_spec=attribute_spec)

    def __test_attributes(self, element, attribute_spec):
        self.assertIn('attributes', element)
        self.assertIsInstance(element['attributes'], list)
        self.assertEqual(len(element['attributes']), len(attribute_spec))
        i = 0
        for attribute_dict in element['attributes']:
            self.assertIn('attribute_name', attribute_dict)
            self.assertEqual(attribute_dict['attribute_name'],
                attribute_spec[0]['key'])
            self.assertIn('attribute_value', attribute_dict)
            self.assertEqual(attribute_dict['attribute_value'],
                attribute_spec[0]['value'])
            i += 1

    def test_memory_max(self):
        element = self.__test_domain_child_element(element_name='memory',
            element_value=self.XML_MEMORY_MAX)
        attribute_spec = [{'key': 'unit', 'value': self.XML_MEMORY_MAX_UNIT}]
        self.__test_attributes(element=element, attribute_spec=attribute_spec)

    def test_memory_current(self):
        element = self.__test_domain_child_element(element_name='currentMemory',
            element_value=self.XML_MEMORY_CURRENT)
        attribute_spec = [{'key': 'unit', 'value': self.XML_MEMORY_CURRENT_UNIT}]
        self.__test_attributes(element=element, attribute_spec=attribute_spec)

    # def test_os_type(self):

    def __test_domain_child_element(self, element_name, element_value):
        filter_list = list(filter(lambda x: x['element_name'] == element_name,
            self.xml_to_intermediate_converter.representation['children']))
        self.assertEqual(len(filter_list), 1)
        element = filter_list[0]
        self.assertIn('element_name', element)
        self.assertEqual(element['element_name'], element_name)
        self.assertIn('element_value', element)
        self.assertEqual(element['element_value'], element_value)
        return element

    def __test_domain_child_without_element(self, element_name):
        element_name = 'title'
        xml_tree_copy = copy.deepcopy(self.xml_tree)
        query = '/domain/{0}'.format(element_name)
        query_result = xml_tree_copy.xpath(query)
        for node in query_result:
            node.getparent().remove(node)
        xml_string = etree.tostring(xml_tree_copy.getroot()).decode(self
            .encoding)
        xml_to_intermediate_converter = XmlToIntermediateConverter(
            xml_string=xml_string)
        filter_list = list(filter(lambda x: x['element_name'] == element_name,
            xml_to_intermediate_converter.representation['children']))
        self.assertFalse(filter_list)

if __name__ == '__main__':
    unittest.main()

