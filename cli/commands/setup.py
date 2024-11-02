import typer
import subprocess
import os

class Setup:
    def main(self, epub_path: str = typer.Option(..., "-p", "--path", help="The path to the epub file")):
        workspace = "epub-unzipped"
        if not os.path.exists(workspace):
            os.mkdir(workspace)
            typer.secho(message="Workspace created", fg='green')
        else:
            typer.secho(message="Workspace already exists", fg='yellow')

        try:
            subprocess.run(["unzip", "-oq", epub_path, "-d", workspace], check=True)
            typer.secho(message="EPUB file extracted", fg='green')
        except subprocess.CalledProcessError as e:
            typer.secho(message=f"Error unzipping file: {e}", fg='red')

        typer.secho(message="Setup complete", fg='green')