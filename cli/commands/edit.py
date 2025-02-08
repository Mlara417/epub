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

        # Command to replace the cover image (renamed to "set-cover")
        @self.cli.command("cover")
        def set_cover(cover_path: str = typer.Argument(..., help="The path to the new cover image")):
            """Replace the cover image of the EPUB file."""
            # Validate cover image format
            valid_extensions = [".jpg", ".jpeg", ".png"]
            ext = os.path.splitext(cover_path)[1].lower()
            if ext not in valid_extensions:
                error("Cover image must be in JPEG or PNG format.")
                raise typer.Exit(1)
            if not os.path.exists(cover_path):
                error(f"Cover image file '{cover_path}' not found.")
                raise typer.Exit(1)
            
            success(f"Replacing cover image with {cover_path}")
            cover_image = os.path.basename(cover_path)
            move_file(cover_path, self.epub3.workspace)
            
            self.epub3.load_content_opf()
            self.epub3.add_manifest_subnode("item", {
                "id": self.COVER,
                "href": cover_image,
                "media-type": "image/jpeg"  # Adjust media-type if needed based on the extension
            })
            self.epub3.add_metadata_subnode("meta", {"name": self.COVER, "content": self.COVER})
            self.epub3.save_xml()
            self.epub3.package_epub()
            success("Cover image replaced successfully.")
            
        # Command to update the EPUB title
        @self.cli.command("title")
        def set_title(new_title: str = typer.Argument(..., help="The new title for the EPUB file")):
            """Update the EPUB title."""
            if not new_title.strip():
                error("Title cannot be empty.")
                raise typer.Exit(1)
            success(f"Updating EPUB title to: {new_title}")
            self.epub3.load_content_opf()
            self.epub3.xml.update_dc_metadata("title", new_title)
            self.epub3.save_xml()
            success("EPUB title updated successfully.")

        # Command to update the EPUB author
        @self.cli.command("author")
        def set_author(author: str = typer.Argument(..., help="The new author for the EPUB file")):
            """Update the EPUB author."""
            if not author.strip():
                error("Author cannot be empty.")
                raise typer.Exit(1)
            success(f"Updating EPUB author to: {author}")
            self.epub3.load_content_opf()
            self.epub3.xml.update_dc_metadata("creator", author)
            self.epub3.save_xml()
            success("EPUB author updated successfully.")
            
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
