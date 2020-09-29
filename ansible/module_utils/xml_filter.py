from lxml import etree

class XmlFilter:
    """Class that converts a XML to another XML based on a filter

    Attributes:
        output_xml (str): xml output string
    """
    def __init__(self, filter_spec, input_xml):
        output_xml = ''
        self.__input_xml_tree = etree.fromstring(input_xml)
        self.__process_filter(filter_spec=filter_spec)
        self.__output_xml = etree.tostring(self.__output_xml_tree)

    def __process_filter(
        self,
        filter_spec,
        parent_output_node=None,
        parent_xpath=''
    ):
        for node_name in filter_spec:
            xpath = '{0}/{1}'.format(parent_xpath, node_name)
            xpath_query_result = self.__input_xml_tree.xpath(xpath)
            self.__process_from_input_nodes(result_list=xpath_query_result,
                parent_output_node=parent_output_node,
                filter_spec=filter_spec[node_name],
                xpath=xpath)

    def __process_from_input_nodes(
        self,
        result_list,
        parent_output_node,
        filter_spec,
        xpath=''
    ):
        for input_node in result_list:
            output_node = self.__create_output_node(node_name=input_node.tag,
                parent_output_node=parent_output_node)
            self.__process_attributes(input_node=input_node,
                output_node=output_node, filter_spec=filter_spec)
            self.__process_text(input_node=input_node, output_node=output_node)
            self.__process_filter(filter_spec=filter_spec,
                parent_output_node=output_node,
                parent_xpath=xpath)

    def __create_output_node(self, node_name, parent_output_node):
        if parent_output_node is None:
            self.__output_xml_tree = etree.Element(node_name)
            return self.__output_xml_tree
        return etree.SubElement(parent_output_node, node_name)

    def __process_attributes(self, input_node, output_node, filter_spec):
        if '__attributes__' in filter_spec:
            self.__get_and_set_attributes(
                attributes_list=filter_spec['__attributes__'],
                input_node=input_node, output_node=output_node)

    def __get_and_set_attributes(self, attributes_list, input_node, output_node):
        for attribute_name in attributes_list:
            attribute_value = input_node.get(attribute_name)
            if attribute_value:
                output_node.set(attribute_name, attribute_value)

    def __process_text(self, input_node, output_node):
        if input_node.text:
            output_node.text = input_node.text

    @property
    def output_xml(self):
        return self.__output_xml
