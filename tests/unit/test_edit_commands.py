import re
import subprocess
from unittest import mock
from more_itertools import side_effect
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from cli.main import get_app
from cli.src.epub3 import Epub3
from cli.src.xml import Xml

#TODO: Fix unit test for edit command
class TestEditCommands:
    GET_METADATA_VALUE = "cli.src.epub3.Epub3.get_opf_metadata_value"
    
    def setup_method(self):
        self.runner = CliRunner()
        self.app = get_app()
        self.epub_path = "tests/data/output.epub"

    @patch("cli.commands.edit.move_file", return_value=None)
    @patch("cli.commands.edit.Edit")
    def test_edit_cover_command_success(self, edit_mock, move_file_mock):
        pass
        edit_mock_instance = edit_mock.return_value

        # Define a custom constructor for Epub3
        def custom_epub3_constructor(workspace):
            epub3_instance = MagicMock(spec=Epub3)
            epub3_instance.workspace = workspace

            # Mock the xml attribute and its methods
            epub3_instance.xml = MagicMock(spec=Xml)
            epub3_instance.xml.load_xml.return_value = None
            epub3_instance.xml.tree = None
            
            epub3_instance.xml.get_tree_root = MagicMock(return_value=MagicMock())  # Prevent actual file loading

            # Mock load_content_opf to ensure no actual file interaction
            epub3_instance.load_content_opf = MagicMock(return_value=MagicMock())

            return epub3_instance

        # Mock Epub3 with the custom constructor
        epub3_mock = MagicMock(side_effect=custom_epub3_constructor)
        edit_mock_instance.epub3 = epub3_mock

        # Configure other mocked methods
        epub3_instance = epub3_mock("tests/data/epub-unzipped")
        epub3_instance.add_manifest_subnode = MagicMock(return_value=None)
        epub3_instance.add_metadata_subnode = MagicMock(return_value=None)
        epub3_instance.save_xml = MagicMock(return_value=None)
        epub3_instance.package_epub = MagicMock(return_value=None)

        # Patch any other points of failure for file I/O
        with patch("cli.src.epub3.Epub3.CONTENT_OPF", "/mocked-content.opf"), \
            patch("cli.src.epub3.Epub3.WORKSPACE", "tests/data/epub-unzipped"):

            # Run the CLI command
            result = self.runner.invoke(self.app, ["edit", "cover", "tests/data/cover.jpg"])

            # Debugging outputs
            print(f"Result Output: {result.output}")
            print(f"Result Exception: {result.exception}")
            print(f"TEST CLASS EDIT: {edit_mock_instance}")
            print(f"TEST EDIT.EPUB3: {edit_mock_instance.epub3}")

