from lxml import etree

class XmlToIntermediate:
    """Convert a XML to an intermediate representation

    Attributes:
        representation (dict): the xml equivalent intermediate
            representation.
    """

    def __init__(self, xml_string):
        self.__xml_tree = etree.fromstring(xml_string)
        self.__parse_node(node=self.__xml_tree)

    def __parse_node(self, node, children_list=None):
        element = self.__parse_name(name=self.__get_node_name(node=node))
        self.__parse_text(node=node, element=element)
        self.__parse_attributes(node=node, element=element)
        self.__parse_children(node=node, parent_element=element)
        if children_list is None:
            self.__representation = element
            return
        children_list.append(element)

    def __get_node_name(self, node):
        return node.tag

    def __parse_name(self, name):
        return {'element_name': name}

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

    def __get_node_children(self, node):
        return list(node)

    def __add_element_to_children_list(self, element, children_list):
        children_list.append(element)
        return children_list

    def __sort_children_list(self, children_list):
        return sorted(children_list, key=lambda x: x['element_name'])

    def __parse_text(self, node, element):
        if node.text:
            element['text'] = node.text

    def __parse_attributes(self, node, element):
        attributes_list = []
        for attribute_name, attribute_value in node.items():
            if attribute_value:
                attributes_list.append({
                    'attribute_name': attribute_name,
                    'attribute_value': attribute_value
                })
        if attributes_list:
            element['attributes'] = attributes_list

    def __parse_children(self, node, parent_element):
        # If it has children (I know, not intuitive)
        if len(node):
            if not parent_element['children']:
                parent_element['children'] = []
            for child in node:
                self.__parse_node(node=child,
                    children_list=parent_element['children'])

    @property
    def representation(self):
        return self.__representation
