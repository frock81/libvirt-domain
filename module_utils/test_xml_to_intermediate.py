#!/usr/bin/env python3

import unittest

from lxml import etree

from xml_to_intermediate import XmlToIntermediate

class TestXmlToIntermediate(unittest.TestCase):

    NODE_NAME = 'domain'

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
        node_attributes = {'key1': 'value1', 'key2': 'value2'}
        node = etree.Element(self.NODE_NAME, **node_attributes)
        node_attributes_gotten = (self.xml_to_intermediate
            ._XmlToIntermediate__get_node_attributes(node=node))
        self.assertEqual(node_attributes, node_attributes_gotten)

    # def test_parse_attributes(self):
    #     self.NODE_NAME = 'domain'
    #     attribute_set = 

    # def test_test(self):

    # def test_child(self):

    # def test_tree(self):

if __name__ == '__main__':
    unittest.main()

