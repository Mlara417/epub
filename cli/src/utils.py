import subprocess

def move_file(src: str, dest: str):
    """Move a file from the source to the destination"""
    subprocess.run(["mv", src, dest])
