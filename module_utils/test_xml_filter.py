import unittest

class TestXmlFilter(unittest.TestCase):
    FILTER = {
        'domain': {
            '__attributes__': ['type']
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