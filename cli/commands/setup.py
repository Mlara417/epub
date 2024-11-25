import typer
from cli.src.epub3 import Epub3
from cli.src.utils import success

class Setup:
    def __init__(self):
        self.epub: Epub3 = Epub3()
        
    def main(self, epub_path: str = typer.Argument(
        ...,
        help="The path to the epub file"
        )
    ):
        """Setup an EPUB file for editing"""
        success(f"Setting up the EPUB file for editing...")
        self.epub.init(epub_path)

    def teardown(self):
        self.epub.cleanup()