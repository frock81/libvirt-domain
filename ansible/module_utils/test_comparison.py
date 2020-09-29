#!/usr/bin/env python3

import unittest

from lxml import etree

from mock_ansible_module import MockAnsibleModule
from xml_filter import XmlFilter
from module_to_intermediate import ModuleToIntermediate
from xml_to_intermediate import XmlToIntermediate

class TestComparison(unittest.TestCase):

    FILTER_SPEC = {
        'domain': {
            '__attributes__': ['type'],
            'name': {},
            'uuid': {},
            'title': {'required': False},
            'description': {'required': False},
            'memory': {'__attributes__': ['unit']},
            'currentMemory': {'__attributes__': ['unit']},
            'vcpu': {
                '__attributes__': ['current']
            },
            'os': {
                'type': {}
            }
        }
    }

    def test_xml_and_module_comparison(self):
        ansible_module = self.get_anisble_module()
        module_intermediate = ModuleToIntermediate(
            libvirt_domain_module=ansible_module)
        filtered_xml = self.get_filtered_xml()
        domain_intermediate = XmlToIntermediate(xml_string=filtered_xml)
        self.assertEqual(module_intermediate.representation, domain_intermediate.representation)

    def get_anisble_module(self):
        module_parameters = {
            'name': 'vm-algol',
            'resources': {
                'domain_type': 'kvm',
                'uuid': 'bfbd7e3a-8b7e-5591-a73f-831f4e162627',
                'title': 'cn-croquidigital2',
                'memory_max': 8388608,
                'memory_max_unit': 'KiB',
                'memory_current': 8388608,
                'memory_current_unit': 'KiB',
                'vcpus_max': 2,
                'vcpus_current': 1,
                'os_type': 'hvm'
            }
        }
        return MockAnsibleModule(parameters=module_parameters)

    def get_filtered_xml(self):
        parser = etree.XMLParser()
        domain_xml_tree = etree.parse('domain.xml', parser)
        xml_string = etree.tostring(domain_xml_tree.getroot())
        filtered_xml = XmlFilter(filter_spec=self.FILTER_SPEC, input_xml=xml_string)
        return filtered_xml.output_xml

if __name__ == '__main__':
    unittest.main()
