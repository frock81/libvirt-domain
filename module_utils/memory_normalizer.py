class MemoryNormalizer():
    """Normalizer memory in an intermediate representation"""
    def __init__(self, intermediate):
        self._normalize(intermediate=intermediate)

    def _normalize(self, intermediate):
        memory_element = self._get_memory_element(intermediate=intermediate)
        self._normalized = intermediate

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

    @property
    def normalized(self):
        return self._normalized
    