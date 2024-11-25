import typer
from cli.src.epub3 import Epub3
from cli.src.utils import move_file, success
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
