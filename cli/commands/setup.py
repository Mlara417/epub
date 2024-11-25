import typer, os
from cli.src.epub3 import Epub3

class Setup:
    def main(self, epub_path: str = typer.Argument(
        ...,
        help="The path to the epub file"
        )
    ):
        Epub3().init(epub_path)