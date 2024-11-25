import os, typer
from lxml.etree import _Element
from cli.src.utils import unzip_file
from cli.src.xml import Xml

class Epub3:
    """Class to handle EPUB3 files"""
    WORKSPACE: str = "epub-unzipped"
    
    def __init__(self, workspace: str = WORKSPACE):
        self.workspace = workspace
        self.xml = Xml()
        
    def init(self, epub_path: str):
        if not os.path.exists(self.workspace):
            typer.secho(message="Creating Workspace...", fg='green')

            os.mkdir(self.workspace)
            unzip_file(epub_path, self.workspace)
            
            typer.secho(message="Setup complete", fg='green')
        else:
            typer.secho(message="Workspace already exists", fg='yellow')

    def load_content_opf(self, content_opf_path: str) -> _Element:
        """Load the content.opf file and return the tree"""
        self.xml.load_xml(content_opf_path)
        self.xml.get_tree_root()