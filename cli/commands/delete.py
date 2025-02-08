import typer
import os
import shutil
from cli.src.epub3 import Epub3
from cli.src.utils import success, error

class Delete:
    def __init__(self):
        self.cli = typer.Typer()
        self.epub3 = Epub3()

        @self.cli.command()
        def file(target_file: str = typer.Argument(..., help="The target file or chapter in the EPUB workspace to delete")):
            """Delete a chapter or file from the EPUB workspace."""
            target_path = os.path.join(self.epub3.workspace, target_file)
            if not os.path.exists(target_path):
                error(f"Target file/directory '{target_file}' not found in EPUB workspace '{self.epub3.workspace}'.")
                raise typer.Exit(1)

            try:
                if os.path.isdir(target_path):
                    shutil.rmtree(target_path)
                    success(f"Deleted directory: {target_file}")
                else:
                    os.remove(target_path)
                    success(f"Deleted file: {target_file}")
            except Exception as e:
                error(f"Error deleting file/directory '{target_file}': {e}")
                raise typer.Exit(1) 