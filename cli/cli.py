import typer
from cli.commands.edit import Edit
from cli.commands.setup import Setup

class EpubCLI:
	def __init__(self):
		self.cli = typer.Typer()
  
		edit_commands = Edit()
		setup_commands= Setup()

		self.cli.command(name="setup")(setup_commands.main)

		self.cli.add_typer(edit_commands.cli, name="edit")

	def run(self):
		self.cli()

def main():
	app = EpubCLI()
	app.run()
 
if __name__ == "__main__":
	main()
