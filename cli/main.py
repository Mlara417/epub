import typer
from cli.commands.edit import Edit
from cli.commands.setup import Setup
from cli.commands.read import Read

class EpubCLI:
    def __init__(self):
        self.cli = typer.Typer()
        self.edit_commands = Edit()
        self.setup_commands= Setup()
        self.read_commands = Read()
        self._register_commands()

    def _register_commands(self):
        # Register commands
        self.cli.command(name="setup")(self.setup_commands.up)
        self.cli.command(name="clean")(self.setup_commands.down)
        self.cli.command(name="validate")(self.setup_commands.validate)

        # Register nested commands
        self.cli.add_typer(self.edit_commands.cli, name="edit")
        self.cli.add_typer(self.read_commands.cli, name="read")

    def run(self):
        self.cli()

def get_app():
    app = EpubCLI()
    return app.cli

def main():
    """
    Main entry point for the CLI application.
    """
    app = EpubCLI()
    app.run()
 
if __name__ == "__main__":
	main()
