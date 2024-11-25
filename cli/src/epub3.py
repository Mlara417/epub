import os, shutil
from re import M
from lxml.etree import _Element
from cli.src.utils import unzip_file, zip_file, success, warning
from cli.src.xml import Xml

class Epub3:
    """Class to handle EPUB3 files"""
    CONTENT_OPF: str = "/content.opf"
    MANIFEST: str = "manifest"
    METADATA: str = "metadata"
    SPINE: str = "spine"
    WORKSPACE: str = "epub-unzipped"
    
    def __init__(self, workspace: str = WORKSPACE):
        self.workspace = workspace
        self.xml = Xml()
        
    def init(self, epub_path: str):
        if not os.path.exists(self.workspace):
            success('Creating Workspace...')

            os.mkdir(self.workspace)
            unzip_file(epub_path, self.workspace)
        else:
            warning("Please remove the workspace before creating a new one")

    def load_content_opf(self, content_opf_path: str = WORKSPACE + CONTENT_OPF) -> _Element:
        """Load the content.opf file tree"""
        success(f"Loading content.opf file: {content_opf_path}")
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

    def get_opf_spine(self):
        """Get the spine from the content.opf file"""
        success("Getting spine from content.opf")
        self.load_content_opf()
        return self.xml.get_node(self.SPINE)

    def package_epub(self, output_file: str = "output.epub"):
        """Package the EPUB file"""
        success("Packaging EPUB file...")
        zip_file("-X0", output_file, "mimetype", self.workspace)
        zip_file("-Xr9D", f"../{output_file}", ".", self.workspace)
        success(f"EPUB file packaged: {output_file}")

    def save_xml(self):
        """Save the loaded XML tree"""
        success("Saving XML tree...")
        self.xml.save()
        
    def cleanup(self):
        """Remove the workspace directory"""
        success("Cleaning up workspace...")
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)
            success("Workspace removed")
        else:
            warning("Workspace does not exist")
            
    def __str__(self):
        return f"EPUB3 workspace: {self.workspace}"
    