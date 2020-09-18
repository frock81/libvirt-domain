class MemoryNormalizer():
    """Normalizer memory in an intermediate representation"""
    def __init__(self, intermediate):
        self._normalize(intermediate)

    def _normalize(self, intermediate):
        self._normalized = intermediate

    @property
    def normalized(self):
        return self._normalized
    