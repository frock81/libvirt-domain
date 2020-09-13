from lxml import etree

class XmlToIntermediate:
    """Convert a XML to an intermediate representation

    Attributes:
        representation (dict): the xml equivalent intermediate
            representation.
    """

    def __init__(self, xml_string):
        parser = etree.XMLParser(remove_blank_text=True)
        xml_tree = etree.fromstring(xml_string, parser)
        self.__representation = self.__create_node_representation(node=xml_tree)

    def __get_node_name(self, node):
        return node.tag

    def __parse_name(self, name):
        return {'element_name': name}

    def __create_base_element(self, node):
        node_name = self.__get_node_name(node=node)
        return self.__parse_name(name=node_name)

    def __get_node_attributes(self, node):
        return dict(node.attrib)

    def __parse_attributes_dictionary(self, attributes_dictionary):
        """Parse an attributes dictionary

        Should pass an attributes dictionary and receive a sorted list

        Args:
            attributes_dictionary (dict): an attributes dictionary with
                the key being the attribute name and the value being
                the attribute value.
        Returns:
            list: a list of dictionaries with 'attribute_name' and
                'attribute_value' keys, sorted by the attribute name.
        """
        attributes_list = []
        for key, value in attributes_dictionary.items():
            item = {'attribute_name': key, 'attribute_value': value}
            attributes_list.append(item)
        return sorted(attributes_list, key=lambda x: x['attribute_name'])

    def __add_attributes_to_element(self, element, attributes_list):
        if attributes_list:
            element['attributes'] = attributes_list
        return element

    def __get_node_text(self, node):
        return node.text

    def __add_text_to_element(self, element, text):
        if text:
            element['text'] = text
        return element

    def __parse_text(self, node, element):
        node_text = self.__get_node_text(node=node)
        return self.__add_text_to_element(element=element, text=node_text)

    def __has_children(self, node):
        if list(node):
            return True
        return False

    def __get_node_children(self, node):
        return list(node)

    def __add_element_to_children_list(self, element, children_list):
        if element is not None:
            children_list.append(element)
        return children_list

    def __sort_children_list(self, children_list):
        return sorted(children_list, key=lambda x: x['element_name'])

    def __add_children_list_to_parent_element(
        self,
        parent_element,
        children_list
    ):
        if children_list:
            parent_element['children'] = children_list

    def __parse_attributes(self, node, element):
        node_attributes = self.__get_node_attributes(node=node)
        attributes_list = self.__parse_attributes_dictionary(
            attributes_dictionary=node_attributes)
        element = self.__add_attributes_to_element(element=element,
            attributes_list=attributes_list)
        return element

    def __parse_children(self, node, element):
        node_children_list = self.__get_node_children(node=node)
        element_children_list = []
        for child_node in node_children_list:
            child_element = self.__create_node_representation(node=child_node)
            self.__add_element_to_children_list(element=child_element,
                children_list=element_children_list)
        sorted_children_list = self.__sort_children_list(
            children_list=element_children_list)
        self.__add_children_list_to_parent_element(parent_element=element,
            children_list=sorted_children_list)
        return element

    def __create_node_representation(self, node):
        element = self.__create_base_element(node=node)
        element = self.__parse_attributes(node=node, element=element)
        if self.__has_children(node=node):
            return self.__parse_children(node=node, element=element)
        return self.__parse_text(node=node, element=element)

    @property
    def representation(self):
        return self.__representation
