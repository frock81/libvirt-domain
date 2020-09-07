#!/usr/bin/env python3

import unittest
from lxml import etree
from xml_filter import XmlFilter

class TestXmlFilter(unittest.TestCase):
    FILTER_SPEC = {
        'domain': {
            '__attributes__': ['type'],
            'name': {},
            'uuid': {},
            'title': {'required': False},
            'description': {'required': False},
            'description': {'required': False},
            'memory': {},
            'currentMemory': {},
            'vcpu': {
                '__attributes__': ['current']
            },
            'os': {
                'type': {}
            }
        }
    }

    @classmethod
    def setUpClass(cls):
        xml_file = 'domain.xml'
        with open(xml_file, 'r') as file:
            xml_string = file.read()
        xml_filter = XmlFilter(filter_spec=cls.FILTER_SPEC,
            input_xml=xml_string)
        cls.xml_tree = etree.fromstring(xml_filter.output_xml)

    @classmethod
    def tearDownClass(cls):
        print(etree.tostring(cls.xml_tree, pretty_print=True))

    def test_domain(self):
        self.assertEqual(self.xml_tree.tag, 'domain')
        self.assertEqual(self.xml_tree.get('type'), 'kvm')
        self.assertFalse(self.xml_tree.get('id'))

    def test_name(self):
        node_name = 'name'
        query = '/domain/{0}'.format(node_name)
        result = self.xml_tree.xpath(query)
        self.assertEqual(len(result), 1)
        node = result[0]
        self.assertEqual(node.tag, node_name)
        self.assertEqual(node.text, 'vm-algol')

    def test_features_out(self):
        node_name = 'features'
        query = '/domain/{0}'.format(node_name)
        result = self.xml_tree.xpath(query)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()