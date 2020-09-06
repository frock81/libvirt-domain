class XmlFilter:
    """Class that converts a XML to another XML based on a filter

    Attributes:
        filter_spec (dict): filter specification
        input_xml (str): input xml string
        output_xml (str): xml output string
    """
    def __init__(self, filter_spec, input_xml):
        self.filter_spec = filter_spec
        self.input_xml = input_xml
        self.__output_xml = ''

    @property
    def output_xml(self):
        return self.__output_xml
