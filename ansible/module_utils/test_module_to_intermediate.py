#!/usr/bin/env python3

import unittest

from mock_ansible_module import MockAnsibleModule
from module_to_intermediate import ModuleToIntermediate

class TestModuleToIntermediate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ansible_module_defaults = MockAnsibleModule.DEFAULT_PARAMETERS
        cls.ansible_module_defaults['name'] = \
            MockAnsibleModule.DEFAULT_DOMAIN_NAME
        ansible_module = MockAnsibleModule(
            parameters=cls.ansible_module_defaults)
        cls.module_to_intermediate = ModuleToIntermediate(
            libvirt_domain_module=ansible_module)

    def test_domain_representation(self):
        self.assertIsInstance(self.module_to_intermediate.representation,
            dict)
        self.assertEqual(self.module_to_intermediate.representation
            ['element_name'], 'domain')
        self.assertIsInstance(self.module_to_intermediate.representation
            ['attributes'], list)
        self.assertEqual(self.module_to_intermediate.representation
            ['attributes'][0]['attribute_name'], 'type')
        self.assertEqual(self.module_to_intermediate.representation
            ['attributes'][0]['attribute_value'], 'kvm')

    def test_domain_children(self):
        self.assertIn('children', self.module_to_intermediate.representation)
        self.assertIsInstance(self.module_to_intermediate.representation
            ['children'], list)
        self.assertTrue(len(self.module_to_intermediate.representation
            ['children']) > 0)

    def test_domain_name(self):
        name_dict = list(filter(lambda x: x['element_name'] == 'name',
            self.module_to_intermediate.representation['children']))[0]
        self.assertIn('element_name', name_dict)
        self.assertEqual(name_dict['element_name'], 'name')
        self.assertIn('text', name_dict)
        self.assertEqual(name_dict['text'], 'vm-foo')

    def test_with_uuid(self):
        ansible_module_parameters = self.ansible_module_defaults
        sample_uuid = '4b77c8d5-61d8-45e9-a132-86f4d1f6f2f9'
        ansible_module_parameters['resources']['uuid'] = sample_uuid
        ansible_module = MockAnsibleModule(parameters=ansible_module_parameters)
        module_to_intermediate = ModuleToIntermediate(
            libvirt_domain_module=ansible_module)
        uuid_filter_list = list(filter(lambda x: x['element_name'] == 'uuid',
            module_to_intermediate.representation['children']))
        self.assertEqual(len(uuid_filter_list), 1)
        uuid_dict = uuid_filter_list[0]
        self.assertIn('element_name', uuid_dict)
        self.assertEqual(uuid_dict['element_name'], 'uuid')
        self.assertIn('text', uuid_dict)
        self.assertEqual(uuid_dict['text'], sample_uuid)

    def test_null_uuid(self):
        ansible_module_parameters = self.ansible_module_defaults
        ansible_module_parameters['resources']['uuid'] = None
        ansible_module = MockAnsibleModule(parameters=ansible_module_parameters)
        module_to_intermediate = ModuleToIntermediate(
            libvirt_domain_module=ansible_module)
        uuid_filter_list = list(filter(lambda x: x['element_name'] == 'uuid',
            module_to_intermediate.representation['children']))
        self.assertEqual(len(uuid_filter_list), 1)
        uuid_dict = uuid_filter_list[0]
        self.assertIn('element_name', uuid_dict)
        self.assertEqual(uuid_dict['element_name'], 'uuid')
        self.assertIn('text', uuid_dict)
        self.assertEqual(uuid_dict['text'],
            MockAnsibleModule.DEFAULT_AUTO_GENERATED_UUID)

    def test_without_uuid(self):
        uuid_filter_list = list(filter(lambda x: x['element_name'] == 'uuid',
            self.module_to_intermediate.representation['children']))
        self.assertEqual(len(uuid_filter_list), 1)
        uuid_dict = uuid_filter_list[0]
        self.assertIn('element_name', uuid_dict)
        self.assertEqual(uuid_dict['element_name'], 'uuid')
        self.assertIn('text', uuid_dict)
        self.assertEqual(uuid_dict['text'],
            MockAnsibleModule.DEFAULT_AUTO_GENERATED_UUID)

    def test_with_title(self):
        ansible_module_parameters = self.ansible_module_defaults
        ansible_module_parameters['resources']['title'] = ('domain short '
            'description')
        ansible_module = MockAnsibleModule(parameters=ansible_module_parameters)
        module_to_intermediate = ModuleToIntermediate(
            libvirt_domain_module=ansible_module)
        title_filter_list = list(filter(lambda x: x['element_name'] == 'title',
            module_to_intermediate.representation['children']))
        self.assertEqual(len(title_filter_list), 1)
        title_dict = title_filter_list[0]
        self.assertIn('element_name', title_dict)
        self.assertEqual(title_dict['element_name'], 'title')
        self.assertIn('text', title_dict)
        self.assertEqual(title_dict['text'], 'domain short description')

    def test_null_title(self):
        ansible_module_parameters = self.ansible_module_defaults
        ansible_module_parameters['resources']['title'] = None
        ansible_module = MockAnsibleModule(parameters=ansible_module_parameters)
        module_to_intermediate = ModuleToIntermediate(
            libvirt_domain_module=ansible_module)
        title_filter_list = list(filter(lambda x: x['element_name'] == 'title',
            module_to_intermediate.representation['children']))
        self.assertFalse(title_filter_list)

    def test_without_title(self):
        title_filter_list = list(filter(lambda x: x['element_name'] == 'title',
            self.module_to_intermediate.representation['children']))
        self.assertFalse(title_filter_list)

    def test_with_description(self):
        ansible_module_parameters = {
            'domain_type': 'kvm',
            'name': 'vm-foo',
            'resources': {
                'description': ('Some long human readable description for the '
                    'domain.')
            }
        }
        ansible_module_parameters = self.ansible_module_defaults
        ansible_module_parameters['resources']['description'] = ('Some long '
            'human readable description for the domain.')
        ansible_module = MockAnsibleModule(parameters=ansible_module_parameters)
        module_to_intermediate = ModuleToIntermediate(
            libvirt_domain_module=ansible_module)
        description_filter_list = list(filter(
            lambda x: x['element_name'] == 'description',
            module_to_intermediate.representation['children']
        ))
        self.assertEqual(len(description_filter_list), 1)
        description_dict = description_filter_list[0]
        self.assertIn('element_name', description_dict)
        self.assertEqual(description_dict['element_name'], 'description')
        self.assertIn('text', description_dict)
        self.assertEqual(description_dict['text'], 'Some long human readable '
            'description for the domain.')

    def test_null_description(self):
        ansible_module_parameters = self.ansible_module_defaults
        ansible_module_parameters['resources']['description'] = None
        ansible_module = MockAnsibleModule(parameters=ansible_module_parameters)
        module_to_intermediate = ModuleToIntermediate(
            libvirt_domain_module=ansible_module)
        description_filter_list = list(filter(
            lambda x: x['element_name'] == 'description',
            module_to_intermediate.representation['children']
        ))
        self.assertFalse(description_filter_list)

    def test_without_description(self):
        description_filter_list = list(filter(
            lambda x: x['element_name'] == 'description',
            self.module_to_intermediate.representation['children']
        ))
        self.assertFalse(description_filter_list)

    def test_vcpus(self):
        vcpu_filter_list = list(filter(lambda x: x['element_name'] == 'vcpu',
            self.module_to_intermediate.representation['children']))
        self.assertEqual(len(vcpu_filter_list), 1)
        vcpu_dict = vcpu_filter_list[0]
        self.assertIn('element_name', vcpu_dict)
        self.assertEqual(vcpu_dict['element_name'], 'vcpu')
        self.assertIn('text', vcpu_dict)
        self.assertEqual(vcpu_dict['text'], str(
            MockAnsibleModule.DEFAULT_VCPUS_MAX))
        self.assertIn('attributes', vcpu_dict)
        self.assertEqual(len(vcpu_dict['attributes']), 1)
        vcpus_current_dict = vcpu_dict['attributes'][0]
        self.assertIn('attribute_name', vcpus_current_dict)
        self.assertEqual(vcpus_current_dict['attribute_name'], 'current')
        self.assertIn('attribute_value', vcpus_current_dict)
        self.assertEqual(vcpus_current_dict['attribute_value'],
            str(MockAnsibleModule.DEFAULT_VCPUS_CURRENT))

    def test_memory_max(self):
        memory_filter_list = list(filter(
            lambda x: x['element_name'] =='memory',
            self.module_to_intermediate.representation['children']))
        self.assertEqual(len(memory_filter_list), 1)
        memory_dict = memory_filter_list[0]
        self.assertIn('element_name', memory_dict)
        self.assertEqual(memory_dict['element_name'], 'memory')
        self.assertIn('text', memory_dict)
        self.assertEqual(memory_dict['text'], str(MockAnsibleModule
            .DEFAULT_MEMORY_MAX))
        self.assertIn('attributes', memory_dict)
        self.assertEqual(len(memory_dict['attributes']), 1)
        memory_unit_dict = memory_dict['attributes'][0]
        self.assertIn('attribute_name', memory_unit_dict)
        self.assertEqual(memory_unit_dict['attribute_name'], 'unit')
        self.assertIn('attribute_value', memory_unit_dict)
        self.assertEqual(memory_unit_dict['attribute_value'],
            str(MockAnsibleModule.DEFAULT_MEMORY_MAX_UNIT))

    def test_memory_current(self):
        current_memory_filter_list = list(filter(
            lambda x: x['element_name'] == 'currentMemory',
            self.module_to_intermediate.representation['children']))
        self.assertEqual(len(current_memory_filter_list), 1)
        current_memory_dict = current_memory_filter_list[0]
        self.assertIn('element_name', current_memory_dict)
        self.assertEqual(current_memory_dict['element_name'], 'currentMemory')
        self.assertIn('text', current_memory_dict)
        self.assertEqual(current_memory_dict['text'], str(MockAnsibleModule
            .DEFAULT_MEMORY_CURRENT))
        self.assertIn('attributes', current_memory_dict)
        self.assertEqual(len(current_memory_dict['attributes']), 1)
        current_memory_unit_dict = current_memory_dict['attributes'][0]
        self.assertIn('attribute_name', current_memory_unit_dict)
        self.assertEqual(current_memory_unit_dict['attribute_name'], 'unit')
        self.assertIn('attribute_value', current_memory_unit_dict)
        self.assertEqual(current_memory_unit_dict['attribute_value'],
            str(MockAnsibleModule.DEFAULT_MEMORY_CURRENT_UNIT))

    def test_os_type(self):
        os_filter_list = list(filter(lambda x: x['element_name'] == 'os',
            self.module_to_intermediate.representation['children']))
        self.assertEqual(len(os_filter_list), 1)
        os_dict = os_filter_list[0]
        self.assertIn('element_name', os_dict)
        self.assertEqual(os_dict['element_name'], 'os')
        self.assertIn('children', os_dict)
        os_children = os_dict['children']
        self.assertEqual(len(os_children), 1)
        type_dict = os_children[0]
        self.assertIn('element_name', type_dict)
        self.assertEqual(type_dict['element_name'], 'type')
        self.assertIn('text', type_dict)
        self.assertEqual(type_dict['text'], MockAnsibleModule.DEFAULT_OS_TYPE)

if __name__ == '__main__':
    unittest.main()