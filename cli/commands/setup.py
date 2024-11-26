import typer
from cli.src.epub3 import Epub3
from cli.src.utils import success,error
from cli.src.exceptions import ValidationError

class Setup:
    def __init__(self):
        self.epub: Epub3 = Epub3()
        
    def up(self, epub_path: str = typer.Argument(...,help="The path to the epub file")):
        """Setup an EPUB file for editing"""
        try:
            self.epub.init(epub_path)
            success(f"Workspace created from provided EPUB")
        except FileExistsError as e:
            error(f"{e}")
            raise typer.Exit(1)

    def down(self):
        """Clean the workspace"""
        try:
            self.epub.cleanup()
            success("Workspace cleaned")
        except FileNotFoundError as e:
            error(f"{e}")
            raise typer.Exit(1)

    def validate(self, epub_path: str = typer.Argument(...,help="The path to the epub file")):
        try:
            self.epub.validate_epub(epub_path)
            success("EPUB validated")
        except ValidationError as e:
            error(f"{e}")
            raise typer.Exit(1)