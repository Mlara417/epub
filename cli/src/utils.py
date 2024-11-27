import subprocess, typer
from rich.console import Console

error_console = Console(stderr=True)

def move_file(src: str, dest: str):
    """Move a file from the source to the destination"""
    success(f"Moving {src} to {dest}")
    subprocess.run(["mv", src, dest])

def unzip_file(file_path: str, dest_path: str):
    """Unzip a file to the destination path"""
    success(f"Extracting EPUB file: {file_path}...")
    try:
        subprocess.run(["unzip", "-oq", file_path, "-d", dest_path], check=True)
    except subprocess.CalledProcessError as e:
        error(f"Error extracting EPUB file: {e}")

def zip_file(flags: str, output_file: str, input_file: str, cwd: str):
    """Zip a file with the given arguments"""
    success(f"Zipping file: {input_file}")
    try:
        subprocess.run(["zip", flags, output_file, input_file], cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        error(f"Error zipping file: {e}")

def success(message: str):
    """Print a success message"""
    error_console.print(message, style="bold green")

def warning(message: str):
    """Print a warning message"""
    error_console.print(message, style="bold yellow")

def error(message: str):
    """Print an error message"""
    error_console.print(message, style="bold red")