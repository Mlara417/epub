import typer
import subprocess

class Edit:
    def __init__(self):
        self.cli = typer.Typer()  # Create a Typer app inside this class

        # Register commands to the Typer instance
        @self.cli.command()
        def cover(cover_path: str = typer.Argument(..., help="The path to the cover image")):

            # TODO: Add code to replace the cover image
            subprocess.run(["mv", cover_path, "epub-unzipped"])
            
            
