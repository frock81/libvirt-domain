class MockAnsibleModule:
    """Mock for AnsibleModule"""

    DEFAULT_APPLY_CHANGES = True
    DEFAULT_AUTOSTART = True
    DEFAULT_DELAY = 1
    DEFAULT_PERSISTENT = True
    DEFAULT_POLL = 1
    DEFAULT_RESTART_METHOD = 'module'
    DEFAULT_SAVE_FILE = None
    DEFAULT_STATE = 'running'
    DEFAULT_STOP_METHOD = 'module'
    DEFAULT_TIMEOUT = 240
    DEFAULT_URI = 'qemu:///system'
    DEFAULT_DESCRIPTION = None
    DEFAULT_DOMAIN_TYPE='kvm'
    DEFAULT_MEMORY_CURRENT = 512
    DEFAULT_MEMORY_CURRENT_UNIT = 'MiB'
    DEFAULT_MEMORY_MAX = 1
    DEFAULT_MEMORY_MAX_UNIT = 'GiB'
    DEFAULT_OS_TYPE = 'hvm'
    DEFAULT_TITLE = None
    DEFAULT_UUID = None
    DEFAULT_VCPUS_CURRENT = 1
    DEFAULT_VCPUS_MAX = 2

    DEFAULT_PARAMETERS = {
        'apply_changes': DEFAULT_APPLY_CHANGES,
        'autostart': DEFAULT_AUTOSTART,
        'delay': DEFAULT_DELAY,
        'persistent': DEFAULT_PERSISTENT,
        'poll': DEFAULT_POLL,
        'restart_method': DEFAULT_RESTART_METHOD,
        'save_file': DEFAULT_SAVE_FILE,
        'state': DEFAULT_STATE,
        'stop_method': DEFAULT_STOP_METHOD,
        'timeout': DEFAULT_TIMEOUT,
        'uri': DEFAULT_URI,
        'resources': {
            'description': DEFAULT_DESCRIPTION,
            'domain_type': DEFAULT_DOMAIN_TYPE,
            'memory_current': DEFAULT_MEMORY_CURRENT,
            'memory_current_unit': DEFAULT_MEMORY_CURRENT_UNIT,
            'memory_max': DEFAULT_MEMORY_MAX,
            'memory_max_unit': DEFAULT_MEMORY_MAX_UNIT,
            'os_type': DEFAULT_OS_TYPE,
            'title': DEFAULT_TITLE,
            'uuid': DEFAULT_UUID,
            'vcpus_max': DEFAULT_VCPUS_MAX,
            'vcpus_current': DEFAULT_VCPUS_CURRENT
        }
    }

    DEFAULT_DOMAIN_NAME = 'vm-foo'

    # Auto-generated based on domain name (vm-foo). It will change
    # if domain name changes.
    DEFAULT_AUTO_GENERATED_UUID = '6404f873-9fae-5bd4-b141-5d1b1bd27df9'

    def __init__(self, parameters):
        self.params = parameters
