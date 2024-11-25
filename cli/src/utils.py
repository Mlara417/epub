import subprocess, typer

def move_file(src: str, dest: str):
    """Move a file from the source to the destination"""
    subprocess.run(["mv", src, dest])

def unzip_file(file_path: str, dest_path: str):
    """Unzip a file to the destination path"""
    try:
        subprocess.run(["unzip", "-oq", file_path, "-d", dest_path], check=True)
        typer.secho(message="EPUB file extracted", fg='green')
    except subprocess.CalledProcessError as e:
        typer.secho(message=f"Error unzipping file: {e}", fg='red')
