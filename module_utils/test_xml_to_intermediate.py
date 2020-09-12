#!/usr/bin/env python3

import unittest

from lxml import etree

from xml_to_intermediate import XmlToIntermediate

class TestXmlToIntermediate(unittest.TestCase):

    def test_parse_name(self):
        xml_string = '<domain />'
        xml_to_intermediate = XmlToIntermediate(xml_string=xml_string)
        node_name = 'name'
        node = etree.Element(node_name)
        element = xml_to_intermediate._XmlToIntermediate__parse_name(node=node)
        self.assertIsInstance(element, dict)
        self.assertIn('element_name', element)
        self.assertEqual(element['element_name'], node_name)

    # def test_attributes(self):

    # def test_test(self):

    # def test_child(self):

    # def test_tree(self):

if __name__ == '__main__':
    unittest.main()

