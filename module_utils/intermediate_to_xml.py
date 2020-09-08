from lxml import etree

class IntermediateToXml:
    """Convert an XML to an intermediate representation

    Properties:
        xml (str): the xml conversion result
    """

    def __init__(self, intermediate_representation):
        """Class constructor

        Args:
            intermediate (dict): intermediate representation dictionary
        """
        self.__xml_tree = None
        self.generate_xml_tree(
            element_definition=intermediate_representation,
            parent_element=self.__xml_tree
        )
        self.__xml = etree.tostring(self.__xml_tree)

    def generate_xml_tree(self, element_definition, parent_element):
        """Generate an XML tree from a dict definition

        Args:
            element_definition (dict): the element definition with
                element name, attributes, text, and others.
            parent_element (Element): the parent element
        """
        element = etree.Element(element_definition['element_name'])
        if 'attributes' in element_definition:
            self.parse_attributes(attributes=element_definition['attributes'],
                element=element)
        # In our case it will have either children or text.
        if 'text' in element_definition:
            # We must pay attention for int/string conversions and
            # decide if we're gonna do this in the domain,
            # representation in the libvirt_domain_xml or the module.
            element.text = element_definition['text']
        elif 'children' in element_definition:
            self.parse_children(children=element_definition['children'],
                parent_element=element)
        if parent_element is None:
            self.__xml_tree = element
            return
        parent_element.append(element)

    def parse_children(self, children, parent_element):
        """Parse children of an element

        Args:
            children (list): list of children definitions
            parent_element (Element): the parent element
        """
        for child_definition in children:
            self.generate_xml_tree(element_definition=child_definition,
                parent_element=parent_element)

    def parse_attributes(self, attributes, element):
        """Parse element attributes"""
        for attribute in attributes:
            # We must pay attention for int/string conversions and
            # decide if we're gonna do this in the domain,
            # representation in the libvirt_domain_xml or the module.
            element.set(attribute['attribute_name'],
                attribute['attribute_value'])
        
    @property
    def xml(self):
        return self.__xml
    