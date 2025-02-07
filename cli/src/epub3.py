import os, shutil
from lxml.etree import _Element
from cli.src.utils import unzip_file, zip_file, success, warning, error
from cli.src.xml import Xml
from epubcheck import EpubCheck
import json
from cli.src.exceptions import ValidationError

class Epub3:
    """Class to handle EPUB3 files"""
    CONTENT_OPF: str = "/content.opf"
    DC: str = ".//dc:"
    MANIFEST: str = "manifest"
    METADATA: str = "metadata"
    OUTPUT_EPUB: str = "output.epub"
    SPINE: str = "spine"
    WORKSPACE: str = "epub-unzipped"
    
    def __init__(self, workspace: str = WORKSPACE):
        self.workspace = workspace
        self.xml = Xml()
        
    def init(self, epub_path: str):
        os.mkdir(self.workspace)
        unzip_file(epub_path, self.workspace)

    def load_content_opf(self, content_opf_path: str = WORKSPACE + CONTENT_OPF) -> _Element:
        """Load the content.opf file tree"""
        self.xml.load_xml(content_opf_path)
        self.xml.get_tree_root()

    def add_manifest_subnode(self, node_name, attributes: dict):
        """Add manifest subnode to the content.opf file"""
        success(f"Adding manifest subnode: {node_name}")
        self.xml.add_node(node_name, self.MANIFEST, attributes)
        
    def add_metadata_subnode(self, node_name, attributes: dict):
        """Add metadata subnode to the content.opf file"""
        success(f"Adding metadata subnode: {node_name}")
        self.xml.add_node(node_name, self.METADATA, attributes)

    def add_spine_subnode(self, node_name, attributes: dict):
        """Add spine subnode to the content.opf file"""
        success(f"Adding spine subnode: {node_name}")
        self.xml.add_node(node_name, self.SPINE, attributes)

    def get_opf_manifest(self):
        """Get the manifest from the content.opf file"""
        success("Getting manifest from content.opf")
        self.load_content_opf()
        return self.xml.get_node(self.MANIFEST)
    
    def get_opf_metadata(self):
        """Get the metadata from the content.opf file"""
        success("Getting metadata from content.opf")
        self.load_content_opf()
        return self.xml.get_node(self.METADATA)

    def get_opf_metadata_value(self, search: str):
        """Get the value of a metadata tag"""
        self.load_content_opf()
        value = self.xml.get_node_value(f"{self.DC}{search}")
        if value is None:
            warning(f"Metadata tag '{search}' not found")
            raise ValueError(f"Metadata tag '{search}' not found")
        return value

    def get_opf_metadata_info(self):
        """Get the information about the metadata from the content.opf file"""
        tags = ['title', 'creator', 'language', 'identifier', 'contributor']
        metadata = {}
        for tag in tags:
            try:
                value = self.get_opf_metadata_value(tag)
                metadata[tag] = value
            except ValueError as e:
                raise ValueError(f"{e}")
        return metadata

    def get_opf_spine(self):
        """Get the spine from the content.opf file"""
        success("Getting spine from content.opf")
        self.load_content_opf()
        return self.xml.get_node(self.SPINE)

    def package_epub(self, output_file: str = OUTPUT_EPUB):
        """Package the EPUB file"""
        success("Packaging EPUB file...")
        zip_file("-X0", output_file, "mimetype", self.workspace)
        zip_file("-Xr9D", f"..{output_file}", ".", self.workspace)
        success(f"EPUB file packaged: {output_file}")

    def save_xml(self):
        """Save the loaded XML tree"""
        success("Saving XML tree...")
        self.xml.save()

    def validate_epub(self, output_epub: str = "/" + OUTPUT_EPUB):
        """Validate the EPUB file"""
        epubcheck = EpubCheck(output_epub)
        if epubcheck.messages:
            error("EPUB file has validation issues")
            print(json.dumps(epubcheck.messages, indent=4))
            raise ValidationError(message="Validation issues found")
            
        
    def cleanup(self):
        """Remove the workspace directory"""
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)
        else:
            raise FileNotFoundError("Workspace doesn't exist")
            
    def __str__(self):
        return f"EPUB3 workspace: {self.workspace}"

    def get_toc(self):
        """Get the table of contents from the NAV section in toc.xhtml."""
        toc_path = f"{self.workspace}/toc.xhtml"
        if not os.path.exists(toc_path):
            warning(f"TOC file '{toc_path}' does not exist")
            return []

        try:
            from lxml import etree
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(toc_path, parser)
            root = tree.getroot()
            if root is None:
                warning(f"Failed to retrieve root element from '{toc_path}'")
                return []

            # Define namespaces for XHTML and epub
            ns = {'x': 'http://www.w3.org/1999/xhtml', 'epub': 'http://www.idpf.org/2007/ops'}
            # Find the <nav> element with epub:type="toc" or role="doc-toc"
            nav_elements = root.xpath('.//x:nav[@epub:type="toc"] | .//x:nav[@role="doc-toc"]', namespaces=ns)
            if not nav_elements:
                warning("No <nav> element with toc found")
                return []
            nav = nav_elements[0]

            # Find all <li> elements inside the <ol> within the nav element
            li_elements = nav.xpath('.//ol/li')
            toc = []
            for li in li_elements:
                a_tag = li.find('.//{http://www.w3.org/1999/xhtml}a')
                if a_tag is None:
                    continue
                label = a_tag.text or "Untitled"
                target = a_tag.get('href', '')
                toc.append({"label": label, "content": target, "level": 0})
            return toc
        except Exception as e:
            raise ValueError(f"Error reading table of contents: {e}")
    