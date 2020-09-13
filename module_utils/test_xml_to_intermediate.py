#!/usr/bin/env python3

import unittest
import copy

from lxml import etree

from xml_to_intermediate import XmlToIntermediate

class TestXmlToIntermediate(unittest.TestCase):

    NODE_NAME = 'node_name'
    NODE_ATTRIBUTES = {'key1': 'value1', 'key2': 'value2', 'a_key': 'a_value'}
    NODE_TEXT = 'Some random text.'
    ELEMENT = {'element_name': NODE_NAME}
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
    XML_STRING = ('<root>'
        '   <child1 />'
        '   <child2>'
        '       Child2 text.'
        '   </child2>'
        '   <child3 interisting="yes" />'
        '</root>')

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
        self.assertIsInstance(node_attributes_gotten, dict)
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
        element = copy.deepcopy(self.ELEMENT)
        element = (self.xml_to_intermediate
            ._XmlToIntermediate__add_attributes_to_element(element=element,
            attributes_list=self.ELEMENT_ATTRIBUTES))
        self.assertIsInstance(element, dict)
        self.assertIn('attributes', element)
        self.assertIsInstance(element['attributes'], list)
        self.assertEqual(len(element['attributes']),
            len(self.ELEMENT_ATTRIBUTES))

    def test_get_node_text(self):
        node = etree.Element(self.NODE_NAME)
        node.text = self.NODE_TEXT
        node_text = (self.xml_to_intermediate
            ._XmlToIntermediate__get_node_text(node=node))
        self.assertIsInstance(node_text, str)
        self.assertEqual(node_text, self.NODE_TEXT)

    def test_add_text_to_element(self):
        element = copy.deepcopy(self.ELEMENT)
        (self.xml_to_intermediate._XmlToIntermediate__add_text_to_element(
            element=element, text=self.NODE_TEXT))
        self.assertIn('text', element)
        self.assertIsInstance(element['text'], str)
        self.assertEqual(element['text'], self.NODE_TEXT)

    def test_get_node_children(self):
        xml_tree = etree.fromstring(self.XML_STRING)
        node_children = (self.xml_to_intermediate
            ._XmlToIntermediate__get_node_children(node=xml_tree))
        self.assertIsInstance(node_children, list)
        self.assertEqual(len(node_children), 3)
        self.assertEqual(node_children[0].tag, 'child1')

    def test_add_element_to_children_list(self):
        element = copy.deepcopy(self.ELEMENT)
        children_list = []
        (self.xml_to_intermediate
            ._XmlToIntermediate__add_element_to_children_list(
            element=element, children_list=children_list))
        self.assertEqual(len(children_list), 1)
        self.assertEqual(children_list[0], element)

    def test_sort_children_list(self):
        children_list = []
        first_element = {'element_name': 'banana', 'element_value': '6'}
        second_element = {'element_name': 'orange', 'element_value': '7'}
        third_element = {'element_name': 'apple', 'element_value': '8'}
        children_list.append(first_element)
        children_list.append(second_element)
        children_list.append(third_element)
        new_children_list = (self.xml_to_intermediate._XmlToIntermediate__sort_children_list(
            children_list=children_list))
        self.assertEqual(new_children_list[0]['element_name'], 'apple')
        self.assertEqual(new_children_list[1]['element_name'], 'banana')
        self.assertEqual(new_children_list[2]['element_name'], 'orange')

    def test_add_children_list_to_parent_element(self):
        element = copy.deepcopy(self.ELEMENT)
        children_list = [{'element_name': 'child1', 'text': 'Child text'}]
        (self.xml_to_intermediate
            ._XmlToIntermediate__add_children_list_to_parent_element(
            parent_element=element, children_list=children_list))
        self.assertIn('children', element)
        self.assertEqual(len(element['children']), 1)
        self.assertEqual(element['children'][0]['element_name'], 'child1')

    # def test_tree(self):

if __name__ == '__main__':
    unittest.main()

