import typer
import os
import subprocess
from cli.src.epub3 import Epub3
from cli.src.utils import move_file, success, error

class Edit:
    COVER = "cover"
    
    def __init__(self):
        self.cli = typer.Typer()
        self.epub3 = Epub3()

        # Register commands to the Typer instance
        @self.cli.command()
        def cover(cover_path: str = typer.Argument(..., help="The path to the cover image")):
            """Add a cover image to an EPUB file"""
            success(f"Adding cover image {cover_path} to the EPUB file")

            cover_image = cover_path.split('/')[-1]
            move_file(cover_path, self.epub3.workspace)

            self.epub3.load_content_opf()
            self.epub3.add_manifest_subnode("item", {"id": self.COVER, "href": cover_image, "media-type": "image/jpeg"})
            self.epub3.add_metadata_subnode("meta", {"name": self.COVER, "content": self.COVER})

            self.epub3.save_xml()
            self.epub3.package_epub()

        @self.cli.command(name="file")
        def file_command(
            target_file: str = typer.Argument(..., help="The file in the EPUB to be replaced"),
            updated_file: str = typer.Argument(..., help="The updated file to replace with")
        ):
            """Replace a chapter or file in the EPUB with updated content."""
            # Check if the updated file exists
            if not os.path.exists(updated_file):
                error(f"Updated file '{updated_file}' not found.")
                raise typer.Exit(1)

            # Construct the target file path in the EPUB workspace
            target_path = os.path.join(self.epub3.workspace, target_file)
            if not os.path.exists(target_path):
                error(f"Target file '{target_file}' not found in EPUB workspace '{self.epub3.workspace}'.")
                raise typer.Exit(1)

            # Remove the old target file
            try:
                os.remove(target_path)
                success(f"Removed existing file: {target_file}")
            except Exception as e:
                error(f"Error removing file '{target_file}': {e}")
                raise typer.Exit(1)

            # Move the updated file to the target path (renaming it appropriately)
            try:
                subprocess.run(["mv", updated_file, target_path], check=True)
                success(f"Replaced '{target_file}' with updated content from '{updated_file}'.")
            except subprocess.CalledProcessError as e:
                error(f"Error replacing file '{target_file}': {e}")
                raise typer.Exit(1)
