import typer
from cli.commands.edit import Edit
from cli.commands.setup import Setup

class EpubCLI:
    def __init__(self):
        self.cli = typer.Typer()
        self._register_commands()

    def _register_commands(self):
        # Initialize commands
        edit_commands = Edit()
        setup_commands= Setup()

        # Register commands
        self.cli.command(name="setup")(setup_commands.main)

        # Register nested commands
        self.cli.add_typer(edit_commands.cli, name="edit")

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
