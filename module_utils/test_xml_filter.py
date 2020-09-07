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

    def test_domain(self):
        xml_file = 'domain.xml'
        with open(xml_file, 'r') as file:
            xml_string = file.read()
        xml_filter = XmlFilter(filter_spec=self.FILTER_SPEC,
            input_xml=xml_string)

if __name__ == '__main__':
    unittest.main()