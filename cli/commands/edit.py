from os import name
import typer, subprocess
from cli.src.epub3 import Epub3
class Edit:
    COVER = "cover"
    def __init__(self):
        self.cli = typer.Typer()
        self.epub3 = Epub3()

        # Register commands to the Typer instance
        @self.cli.command()
        def cover(cover_path: str = typer.Argument(..., help="The path to the cover image"), workspace: str = typer.Argument('epub-unzipped', help="Path to the epub")):
            """Add a cover image to an EPUB file"""
            subprocess.run(["mv", cover_path, workspace])
            cover_image = cover_path.split('/')[-1]

            self.epub3.load_content_opf(workspace + "/content.opf")
            self.epub3.xml.add_node("item", "manifest", {"id": self.COVER, "href": cover_image, "media-type": "image/jpeg"})
            self.epub3.xml.add_node("meta", "metadata", {"name": self.COVER, "content": self.COVER})
            self.epub3.xml.save_xml()

            subprocess.run(["zip", "-X0", "output.epub", "mimetype"], cwd=workspace)

            subprocess.run(["zip", "-Xr9D", "../output.epub", "."], cwd=workspace)



