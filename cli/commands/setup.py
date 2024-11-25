import typer
from cli.src.epub3 import Epub3
from cli.src.utils import success

class Setup:
    def main(self, epub_path: str = typer.Argument(
        ...,
        help="The path to the epub file"
        )
    ):
        """Setup an EPUB file for editing"""
        success(f"Setting up the EPUB file for editing...")
        Epub3().init(epub_path)