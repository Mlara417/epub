from os import name
import xml
import typer, subprocess
from cli.src.epub3 import Epub3
from lxml import etree
from lxml.etree import _Element, _ElementTree
class Edit:
    def __init__(self):
        self.cli = typer.Typer()
        self.epub3 = Epub3()

        # Register commands to the Typer instance
        @self.cli.command()
        def cover(cover_path: str = typer.Argument(..., help="The path to the cover image"), workspace: str = typer.Argument('epub-unzipped', help="Path to the epub")):
            namespaces = {
                "opf": "http://www.idpf.org/2007/opf",  # For elements like 'package', 'manifest', etc.
                "dc": "http://purl.org/dc/elements/1.1/"  # For elements like 'title', 'creator', etc.
            }
            subprocess.run(["mv", cover_path, workspace])

            # Load the content.opf file
            content_opf_tree: _ElementTree  = self.epub3.load_xml(workspace + "/content.opf")
            content_opf_element: _Element  = self.epub3.process_tree(content_opf_tree)

            # Get the manifest node
            manifest_node: list[_Element] = content_opf_element.xpath("//opf:package", namespaces=namespaces)[0].xpath("//opf:manifest", namespaces=namespaces)[0]

            # Create a new item element
            new_item: _Element = etree.Element(
                "item", 
                attrib={
                    "id": "cover", 
                    "href": "header-cool.jpg", 
                    "media-type": "image/jpeg"
                }
            )

            # Append the new item to the manifest node
            manifest_node.append(new_item)

            # Get the metadata node
            metadata_node: list[_Element] = content_opf_element.xpath("//opf:package", namespaces=namespaces)[0].xpath("//opf:metadata", namespaces=namespaces)[0]

            # Create a new meta element
            new_meta: _Element = etree.Element(
                "meta", 
                attrib={
                    "name": "cover", 
                    "content": "cover",
                }
            )

            # Append the new meta to the metadata node
            metadata_node.append(new_meta)
            #print(etree.tostring(metadata_node, pretty_print=True).decode())

            content_opf_tree.write(workspace + "/content.opf", pretty_print=True, xml_declaration=True, encoding="utf-8")

            subprocess.run(["zip", "-X0", "output.epub", "mimetype"], cwd=workspace)

            subprocess.run(["zip", "-Xr9D", "../output.epub", "."], cwd=workspace)



