import typer
from cli.src.epub3 import Epub3
from cli.src.utils import success, error
class Read:
    def __init__(self):
        self.cli = typer.Typer()
        self.epub3 = Epub3()

        # Register commands to the Typer instance
        @self.cli.command()
        def meta(data: str = typer.Argument(..., help="The metadata tag to read value from")):
            """Read metadata from the EPUB file"""
            try:
                meta_value = self.epub3.get_opf_metadata_value(data)
                success(meta_value)
            except ValueError as e:
                error(f"{e}")
                raise typer.Exit(1)
                
