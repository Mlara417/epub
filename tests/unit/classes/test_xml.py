import os
import tempfile
import unittest
from lxml import etree
from cli.src.xml import Xml

class TestXml(unittest.TestCase):
    def setUp(self):
        # Create a temporary file with sample XML content
        self.xml_instance = Xml()
        self.sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
<opf:package xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <opf:manifest>
         <opf:item id="item1"/>
    </opf:manifest>
    <opf:metadata>
         <dc:title>Original Title</dc:title>
         <dc:creator>Original Creator</dc:creator>
    </opf:metadata>
</opf:package>"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.xml')
        self.temp_file.write(self.sample_xml)
        self.temp_file.close()

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_load_xml_and_get_tree_root(self):
        self.xml_instance.load_xml(self.temp_file.name)
        self.xml_instance.get_tree_root()
        root = self.xml_instance.root
        # Verify that the root's local name is "package" and in the opf namespace
        qname = etree.QName(root)
        self.assertEqual(qname.localname, "package")
        self.assertEqual(qname.namespace, "http://www.idpf.org/2007/opf")

    def test_get_node(self):
        self.xml_instance.load_xml(self.temp_file.name)
        self.xml_instance.get_tree_root()
        # Get the manifest node using get_node
        node = self.xml_instance.get_node("manifest")
        qname = etree.QName(node)
        self.assertEqual(qname.localname, "manifest")
        self.assertEqual(qname.namespace, "http://www.idpf.org/2007/opf")

    def test_get_node_value(self):
        self.xml_instance.load_xml(self.temp_file.name)
        self.xml_instance.get_tree_root()
        # Retrieve the value of the dc:title node
        value = self.xml_instance.get_node_value(".//dc:title")
        self.assertEqual(value, "Original Title")

    def test_add_node(self):
        self.xml_instance.load_xml(self.temp_file.name)
        self.xml_instance.get_tree_root()
        # Capture the original children of the manifest element
        manifest = self.xml_instance.get_node("manifest")
        original_children = list(manifest)
        # Add a new node to the manifest element
        self.xml_instance.add_node("newnode", "manifest", {"attr": "value"})
        new_children = list(manifest)
        self.assertEqual(len(new_children), len(original_children) + 1)
        added_node = new_children[-1]
        self.assertEqual(added_node.tag, "newnode")
        self.assertEqual(added_node.get("attr"), "value")

    def test_save(self):
        self.xml_instance.load_xml(self.temp_file.name)
        self.xml_instance.get_tree_root()
        # Update the dc:title text
        title_node = self.xml_instance.root.find(".//{http://purl.org/dc/elements/1.1/}title")
        title_node.text = "Modified Title"
        # Save to a new temporary file
        new_temp_path = self.temp_file.name + ".saved.xml"
        self.xml_instance.file_path = new_temp_path
        self.xml_instance.save()
        # Parse the saved file and verify the change
        tree = etree.parse(new_temp_path)
        new_title = tree.find(".//{http://purl.org/dc/elements/1.1/}title").text
        self.assertEqual(new_title, "Modified Title")
        os.remove(new_temp_path)

    def test_get_nodes(self):
        self.xml_instance.load_xml(self.temp_file.name)
        self.xml_instance.get_tree_root()
        nodes = self.xml_instance.get_nodes(".//dc:title")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Original Title")

    def test_update_dc_metadata_existing(self):
        self.xml_instance.load_xml(self.temp_file.name)
        self.xml_instance.get_tree_root()
        # Update existing dc:title element
        self.xml_instance.update_dc_metadata("title", "New Title")
        title_node = self.xml_instance.root.find(".//{http://purl.org/dc/elements/1.1/}title")
        self.assertEqual(title_node.text, "New Title")

    def test_update_dc_metadata_new(self):
        self.xml_instance.load_xml(self.temp_file.name)
        self.xml_instance.get_tree_root()
        # Remove the dc:creator element to force creation
        creator_node = self.xml_instance.root.find(".//{http://purl.org/dc/elements/1.1/}creator")
        creator_node.getparent().remove(creator_node)
        # Now update dc:creator, which doesn't exist
        self.xml_instance.update_dc_metadata("creator", "New Creator")
        new_creator = self.xml_instance.root.find(".//{http://purl.org/dc/elements/1.1/}creator")
        self.assertIsNotNone(new_creator)
        self.assertEqual(new_creator.text, "New Creator")

    def test_update_dc_metadata_no_metadata(self):
        # Create XML without a metadata element
        no_metadata_xml = """<?xml version="1.0" encoding="UTF-8"?>
<opf:package xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <opf:manifest>
         <opf:item id="item1"/>
    </opf:manifest>
</opf:package>"""
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.xml') as f:
            f.write(no_metadata_xml)
            no_metadata_file = f.name

        new_xml_instance = Xml()
        new_xml_instance.load_xml(no_metadata_file)
        new_xml_instance.get_tree_root()
        with self.assertRaises(ValueError) as context:
            new_xml_instance.update_dc_metadata("title", "Should Fail")
        self.assertEqual(str(context.exception), "Metadata element not found in content.opf.")
        os.remove(no_metadata_file)

if __name__ == '__main__':
    unittest.main()
