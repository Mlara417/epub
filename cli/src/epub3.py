import os, typer, subprocess
from cli.src.xml import Xml
from lxml.etree import _Element

class Epub3:
    """Class to handle EPUB3 files"""
    def __init__(self, workspace: str = "epub-unzipped"):
        self.workspace = workspace
        self.xml = Xml()
        
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

    def load_content_opf(self, content_opf_path: str) -> _Element:
        """Load the content.opf file and return the tree"""
        self.xml.load_xml(content_opf_path)
        self.xml.get_tree_root()