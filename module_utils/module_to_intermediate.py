import uuid

class ModuleToIntermediate:
    """Convert libvirt_domain module to an intermediate representation

    I'm worried if the order will affect any intermediate representation
    comparison. I guess it will. Perhaps it would be best to use a set
    instead of a list and, perhaps, an ordered dict.
    """

    # Copied and adapted from core.py
    UUID_NAMESPACE_ANSIBLE = uuid.UUID('361E6D51-FAEC-444A-9079-341386DA8E2E')

    def __init__(self, libvirt_domain_module):
        """Class constructor"""
        self.libvirt_domain_module = libvirt_domain_module
        self.__parse_domain_element()
        self.parse_current_memory()
        self.parse_description()
        self.parse_memory()
        self.parse_name()
        self.parse_os_type()
        self.parse_title()
        self.parse_uuid()
        self.parse_vcpu()

    def __parse_domain_element(self):
        self.__representation = {
            'element_name': 'domain',
            'attributes': [{
                'attribute_name': 'type',
                'attribute_value': (self.libvirt_domain_module.params
                    ['resources']['domain_type']),
            }],
            'children': []
        }

    def parse_name(self):
        self.__representation['children'].append({
            'element_name': 'name',
            'text': self.libvirt_domain_module.params['name']
        })

    def parse_uuid(self):
        domain_uuid = self.to_uuid(
            string=self.libvirt_domain_module.params['name'])
        if ('uuid' in self.libvirt_domain_module.params['resources']
            and self.libvirt_domain_module.params['resources']['uuid']):
            domain_uuid = self.libvirt_domain_module.params['resources']['uuid']
        self.__representation['children'].append({
            'element_name': 'uuid',
            'text': domain_uuid
        })

    def parse_title(self):
        if ('title' in self.libvirt_domain_module.params['resources']
            and self.libvirt_domain_module.params['resources']['title']):
            self.__representation['children'].append({
                'element_name': 'title',
                'text': self.libvirt_domain_module.params['resources']['title']
            })

    def parse_description(self):
        if ('description' in self.libvirt_domain_module.params['resources']
            and self.libvirt_domain_module.params['resources']['description']):
            self.__representation['children'].append({
                'element_name': 'description',
                'text': (self.libvirt_domain_module.params['resources']
                    ['description'])
            })

    # We must pay attention for int/string conversions and decide if
    # we're gonna do this here, in the libvirt_domain_xml or the
    # module will do.
    def parse_vcpu(self):
        self.__representation['children'].append({
            'element_name': 'vcpu',
            'text': str(self.libvirt_domain_module.params['resources']
                ['vcpus_max']),
            'attributes': [{
                'attribute_name': 'current',
                'attribute_value': str(self.libvirt_domain_module.params
                    ['resources']['vcpus_current'])
            }]
        })

    def parse_memory(self):
        """Parses memory element

        Libvirt convert units to KiB when dumping XML information.
        Because of this, if we want to maintain comparison simple,
        we need to convert unit to KiB, though it is not strictly
        needed for definition/creation.
        """
        self.__representation['children'].append({
            'element_name': 'memory',
            'text': str(self.libvirt_domain_module.params['resources']
                ['memory_max']),
            'attributes': [{
                'attribute_name': 'unit',
                'attribute_value': (self.libvirt_domain_module.params
                    ['resources']['memory_max_unit'])
            }]
        })

    def parse_current_memory(self):
        """Parses current memory element

        Libvirt convert units to KiB when dumping XML information.
        Because of this, if we want to maintain comparison simple,
        we need to convert unit to KiB, though it is not strictly
        needed for definition/creation.
        """
        self.__representation['children'].append({
            'element_name': 'currentMemory',
            'text': str(self.libvirt_domain_module.params['resources']
                ['memory_current']),
            'attributes': [{
                'attribute_name': 'unit',
                'attribute_value': (self.libvirt_domain_module.params
                    ['resources']['memory_current_unit'])
            }]
        })

    def parse_os_type(self):
        self.__representation['children'].append({
            'element_name': 'os',
            'children': [{
                'element_name': 'type',
                'text': (self.libvirt_domain_module.params['resources']
                    ['os_type'])
            }]
        })

    # Copied and adapted from core.py
    def to_uuid(self, string):
        return str(uuid.uuid5(self.UUID_NAMESPACE_ANSIBLE, str(string)))

    @property
    def representation(self):
        return self.__representation
