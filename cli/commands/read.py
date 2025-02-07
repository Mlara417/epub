import typer
from cli.src.epub3 import Epub3
from cli.src.utils import success, error, task, warning

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

        @self.cli.command()
        def info():
            """Read information about the EPUB file"""
            try:
                metadata = self.epub3.get_opf_metadata_info()
                for key, value in metadata.items():
                    task(f"{key.title()}: {value}")
            except ValueError as e:
                error(f"{e}")
                raise typer.Exit(1)

        @self.cli.command()
        def toc():
            """List the table of contents of the EPUB file"""
            try:
                toc_items = self.epub3.get_toc()
                if not toc_items:
                    warning("No table of contents found")
                    return
                
                task("Table of Contents:")
                for item in toc_items:
                    # Indent based on level
                    indent = "  " * item["level"]
                    task(f"{indent}• {item['label']} ({item['content']})")
            except ValueError as e:
                error(f"{e}")
                raise typer.Exit(1)
