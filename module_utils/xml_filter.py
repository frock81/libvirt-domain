from lxml import etree

class XmlFilter:
    """Class that converts a XML to another XML based on a filter

    Attributes:
        filter_spec (dict): filter specification
        input_xml (str): input xml string
        output_xml (str): xml output string
    """
    def __init__(self, filter_spec, input_xml):
        self.__output_xml = ''
        for root_key in filter_spec:
            output_xml_tree = etree.Element(root_key)
        self.__output_xml = etree.tostring(output_xml_tree)

    @property
    def output_xml(self):
        return self.__output_xml
