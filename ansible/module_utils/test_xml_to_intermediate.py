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

    def test_create_base_element(self):
        node = etree.Element(self.NODE_NAME)
        element = (self.xml_to_intermediate
            ._XmlToIntermediate__create_base_element(node=node))
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

    def test_get_empty_node_children(self):
        node = etree.Element('root')
        node_children = (self.xml_to_intermediate
            ._XmlToIntermediate__get_node_children(node=node))
        self.assertIsInstance(node_children, list)
        self.assertFalse(node_children)

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

    def test_create_node_representation(self):
        node_xml_string = ('<root>'
            '   <z_child z_attrib="foo" a_attrib="bar" />'
            '   <a_child>Some random text.</a_child>'
            '   <nested_children>'
            '       <c />'
            '       <a />'
            '       <b />'
            '   </nested_children>'
            '</root>')
        parser = etree.XMLParser(remove_blank_text=True)
        xml_tree = etree.fromstring(node_xml_string, parser)
        representation = (self.xml_to_intermediate
            ._XmlToIntermediate__create_node_representation(node=xml_tree))
        self.assertIsInstance(representation, dict)
        self.assertIn('element_name', representation)
        self.assertEqual(representation['element_name'], 'root')
        self.assertIn('children', representation)

    def test_representation_attribute(self):
        node_xml_string = ('<root>'
            '   <z_child z_attrib="foo" a_attrib="bar" />'
            '   <a_child>Some random text.</a_child>'
            '   <nested_children>'
            '       <c />'
            '       <a />'
            '       <b />'
            '   </nested_children>'
            '</root>')
        xml_to_intermediate = XmlToIntermediate(xml_string=node_xml_string)
        root = xml_to_intermediate.representation
        self.assertIsInstance(root, dict)
        self.assertIn('element_name', root)
        self.assertEqual(root['element_name'],
            'root')
        self.assertNotIn('text', root)
        self.assertNotIn('attributes', root)
        self.assertIn('children', root)
        root_children = xml_to_intermediate.representation['children']
        root_total_children = 3
        self.assertEqual(len(root_children), root_total_children)
        a_child = root_children[0]
        self.assertEqual(a_child['element_name'], 'a_child')
        self.assertEqual(a_child['text'], 'Some random text.')
        z_child = root_children[2]
        self.assertIn('attributes', z_child)
        z_child_total_attributes = 2
        self.assertEqual(len(z_child['attributes']), z_child_total_attributes)
        self.assertIn('attribute_name', z_child['attributes'][0])
        self.assertEqual(z_child['attributes'][0]['attribute_name'], 'a_attrib')
        nested_children = root_children[1]
        self.assertNotIn('text', nested_children)
        self.assertNotIn('attributes', nested_children)
        self.assertIn('children', nested_children)
        nested_children_total_children = 3
        self.assertEqual(len(nested_children['children']),
            nested_children_total_children)

if __name__ == '__main__':
    unittest.main()

