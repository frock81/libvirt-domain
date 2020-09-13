#!/usr/bin/env python3

import unittest

from lxml import etree

from xml_to_intermediate import XmlToIntermediate

class TestXmlToIntermediate(unittest.TestCase):

    NODE_NAME = 'node_name'
    NODE_ATTRIBUTES = {'key1': 'value1', 'key2': 'value2', 'a_key': 'a_value'}
    ELEMENT_ATTRIBUTES = [{
        'attribute_name': 'a_key',
        'attribute_value': 'a_value'
    },{
        'attribute_name': 'key1',
        'attribute_value': 'value1'
    },{
        'attribute_name': 'key2',
        'attribute_value': 'value2'
    }]

    @classmethod
    def setUpClass(cls):
        xml_string = '<domain />'
        cls.xml_to_intermediate = XmlToIntermediate(xml_string=xml_string)

    def test_get_node_name(self):
        node = etree.Element(self.NODE_NAME)
        node_name_gotten = (self.xml_to_intermediate
            ._XmlToIntermediate__get_node_name(node=node))
        self.assertEqual(self.NODE_NAME, node_name_gotten)

    def test_parse_name(self):
        element = (self.xml_to_intermediate._XmlToIntermediate__parse_name(
            name=self.NODE_NAME))
        self.assertIsInstance(element, dict)
        self.assertIn('element_name', element)
        self.assertEqual(element['element_name'], self.NODE_NAME)

    def test_get_node_attributes(self):
        node = etree.Element(self.NODE_NAME, **self.NODE_ATTRIBUTES)
        node_attributes_gotten = (self.xml_to_intermediate
            ._XmlToIntermediate__get_node_attributes(node=node))
        self.assertEqual(self.NODE_ATTRIBUTES, node_attributes_gotten)

    def test_parse_attributes_dictionary(self):
        attributes_sorted_list = (self.xml_to_intermediate
            ._XmlToIntermediate__parse_attributes_dictionary(
            attributes_dictionary=self.NODE_ATTRIBUTES))
        self.assertIsInstance(attributes_sorted_list, list)
        self.assertEqual(len(attributes_sorted_list), len(self.NODE_ATTRIBUTES))
        self.assertIsInstance(attributes_sorted_list[0], dict)
        self.assertEqual(attributes_sorted_list, self.ELEMENT_ATTRIBUTES)

    def test_add_attributes_to_element(self):
        pass

    # def test_child(self):

    # def test_tree(self):

if __name__ == '__main__':
    unittest.main()

