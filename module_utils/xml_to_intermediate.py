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
