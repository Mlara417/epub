import typer, subprocess
from cli.src.epub3 import Epub3
from cli.src.utils import move_file
class Edit:
    COVER = "cover"
    
    def __init__(self):
        self.cli = typer.Typer()
        self.epub3 = Epub3()

        # Register commands to the Typer instance
        @self.cli.command()
        def cover(cover_path: str = typer.Argument(..., help="The path to the cover image")):
            """Add a cover image to an EPUB file"""
            move_file(cover_path, self.epub3.workspace)
            
            cover_image = cover_path.split('/')[-1]

            self.epub3.load_content_opf(self.epub3.workspace + "/content.opf")
            self.epub3.xml.add_node("item", "manifest", {"id": self.COVER, "href": cover_image, "media-type": "image/jpeg"})
            self.epub3.xml.add_node("meta", "metadata", {"name": self.COVER, "content": self.COVER})
            self.epub3.xml.save_xml()

            subprocess.run(["zip", "-X0", "output.epub", "mimetype"], cwd=self.epub3.workspace)

            subprocess.run(["zip", "-Xr9D", "../output.epub", "."], cwd=self.epub3.workspace)



