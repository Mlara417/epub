import os, typer, subprocess
from lxml import etree
from lxml.etree import _ElementTree, parse, _Element

class Epub3:
    def __init__(self, workspace: str = "epub-unzipped"):
        self.workspace = workspace
        
    def init(self, epub_path: str):
        workspace = "epub-unzipped"
        if not os.path.exists(workspace):
            os.mkdir(workspace)
            typer.secho(message="Workspace created", fg='green')
            try:
                subprocess.run(["unzip", "-oq", epub_path, "-d", workspace], check=True)
                typer.secho(message="EPUB file extracted", fg='green')
            except subprocess.CalledProcessError as e:
                typer.secho(message=f"Error unzipping file: {e}", fg='red')

            typer.secho(message="Setup complete", fg='green')
        else:
            typer.secho(message="Workspace already exists", fg='yellow')

    def load_xml(self, file_path: str) -> _ElementTree:
        """Load an XML file and return the tree"""
        tree= parse(file_path)
        return tree

    def process_tree(self, tree: _ElementTree) -> _Element:
        """Process the tree and return the root element"""
        root = tree.getroot()
        return root

    def load_content_opf(self, content_opf_path: str) -> _Element:
        """Load the content.opf file and return the tree"""
        tree = self.load_xml(content_opf_path + "/content.opf")
        root = self.process_tree(tree)
        return root