from lxml import etree
from lxml.etree import _ElementTree, parse, _Element

class Xml:
    """Class to handle XML files"""
    NAMESPACES = {
        "opf": "http://www.idpf.org/2007/opf",  # For elements like 'package', 'manifest', etc.
        "dc": "http://purl.org/dc/elements/1.1/"  # For elements like 'title', 'creator', etc.
    }
    ROOT_ELEMENT: str = "package"
    OPF = "//opf:"

    def __init__(self):
        self.file_path: str = None
        self.tree: _ElementTree = None
        self.root: _Element = None

    def load_xml(self, file_path: str) -> _ElementTree:
        """Load an XML file and return the tree"""
        self.file_path = file_path
        self.tree= parse(file_path)

    def get_tree_root(self) -> _Element:
        """Process the tree and return the root element"""
        self.root = self.tree.getroot()

    def get_node(self, search_node: str) -> list[_Element]:
        """Search for a top-level node in the XML tree"""
        return self.root.xpath(f"{self.OPF}{self.ROOT_ELEMENT}", namespaces=self.NAMESPACES)[0].xpath(f"{self.OPF}{search_node}", namespaces=self.NAMESPACES)[0]

    def get_node_value(self, search: str) -> str:
        """Get the value of an XML node"""
        return(self.root.find(search, namespaces=self.NAMESPACES).text)

    def add_node(self,node_name, target_node_name, attributes: dict):
        """Add a new node to the XML tree"""
        target_node = self.get_node(target_node_name)
        new_node: _Element = etree.Element(
            node_name, 
            attrib=attributes
        )
        target_node.append(new_node)

    def save(self):
        """Write the tree to a file"""
        self.tree.write(self.file_path, pretty_print=True, xml_declaration=True, encoding="utf-8")

    def get_nodes(self, xpath_expr: str) -> list[_Element]:
        """Return a list of nodes matching the given XPath expression."""
        return self.root.xpath(xpath_expr, namespaces=self.NAMESPACES)

    def update_dc_metadata(self, tag: str, value: str) -> None:
        """Update or create a Dublin Core metadata element.
           tag: e.g., "title" or "creator"
           value: new content for the tag
        """
        # Build the fully namespaced tag using the dc namespace.
        full_tag = f"{{{self.NAMESPACES['dc']}}}{tag}"

        # Attempt to find the element.
        elem = self.root.find(f".//{full_tag}")
        if elem is not None:
            elem.text = value
        else:
            # Look for the metadata element inside the opf document.
            metadata = self.root.find(".//{http://www.idpf.org/2007/opf}metadata")
            if metadata is None:
                raise ValueError("Metadata element not found in content.opf.")
            from lxml import etree
            new_elem = etree.Element(full_tag)
            new_elem.text = value
            metadata.append(new_elem)