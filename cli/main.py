import typer
from cli.commands.edit import Edit
from cli.commands.setup import Setup
from cli.commands.read import Read

class EpubCLI:
    def __init__(self):
        self.cli = typer.Typer()
        self._register_commands()

    def _register_commands(self):
        # Initialize commands
        edit_commands = Edit()
        setup_commands= Setup()
        read_commands = Read()

        # Register commands
        self.cli.command(name="setup")(setup_commands.main)
        self.cli.command(name="clean")(setup_commands.teardown)
        self.cli.command(name="validate")(setup_commands.validate)

        # Register nested commands
        self.cli.add_typer(edit_commands.cli, name="edit")
        self.cli.add_typer(read_commands.cli, name="read")

    def run(self):
        self.cli()

def main():
    """
    Main entry point for the CLI application.
    """
    app = EpubCLI()
    app.run()
 
if __name__ == "__main__":
	main()
