import math

class MemoryNormalizer():
    """Normalizer memory in an intermediate representation

    Attributes:
        normalized (dict): the intermediate representation with the
            memory entries normalized to KiB.
    """
    def __init__(self, intermediate):
        self._normalize(intermediate=intermediate)

    def _normalize(self, intermediate):
        memory_element = self._get_memory_element(intermediate=intermediate)
        self._normalized = intermediate

    def _normalize_element(self, element):
        """Receives an element and normalizes its memory"""
        if 'attributes' in element:
            for attribute in element['attributes']:
                if attribute['attribute_name'] == 'unit':
                    element['text'] = str(self._convert_to_kibibyte(
                        value=int(element['text']),
                        unit=attribute['attribute_value'])
                    )
                    attribute['attribute_value'] = 'KiB'
                    return element
        raise Exception('Element has {0} no attributes key'.format(
            element['element_name']))

    def _get_memory_element(self, intermediate):
        return self._get_element_from_list(element_list=
            intermediate['children'], element_name='memory')

    def _get_element_from_list(self, element_list, element_name):
        try:
            return next(filter(lambda element : element['element_name'] ==
                element_name, element_list))
        except StopIteration as e:
            return None
        return None

    def _get_attribute_from_element(self, element, attribute_name):
        if 'attributes' in element:
            try:
                return next(filter(lambda child : child['attribute_name'] ==
                    attribute_name, element['attributes']))
            except StopIteration as e:
                return None
        return None

    def _get_memory_value(self, memory_element):
        if 'text' in memory_element:
            return memory_element['text']
        return None

    def _get_memory_unit(self, unit_attribute):
        if 'attribute_value' in unit_attribute:
            return unit_attribute['attribute_value']
        return None

    def _convert_to_kibibyte(self, value, unit):
        """Conver to kibibyte

        As Libvirt may round up kibibytes, so will this.

        Args:
            value (int): The value to be converted
            unit (str): The unit for the value. Allowed values are:
                b|B for bytes, KB|kb for 1000 bytes, KiB|K|k for 1024
                bytes, MB|mb, MiB|M|m, GB|gb, GiB|G|g, TB|tb, TiB|T|t
        Returns:
            int: kibibyte value rounded up.
        """
        if unit.upper() == 'B':
            return int(math.ceil(value/1024))
        if unit.upper() == 'KIB' or unit.upper() == 'K':
            return value
        if unit.upper() == 'KB':
            return int(math.ceil((value*1000)/1024))
        if unit.upper() == 'MIB' or unit.upper() == 'M':
            return value*1024
        if unit.upper() == 'MB':
            return int(math.ceil((value*1000*1000)/1024))
        if unit.upper() == 'GIB' or unit.upper() == 'G':
            return value*1024*1024
        if unit.upper() == 'GB':
            return int(math.ceil((value*1000*1000*1000)/1024))
        if unit.upper() == 'TIB' or unit.upper() == 'T':
            return value*1024*1024*1024
        if unit.upper() == 'TB':
            return int(math.ceil((value*1000*1000*1000*1000)/1024))
        raise Exception('Unit now allowed: {0}'.format(unit))

    @property
    def normalized(self):
        return self._normalized
    