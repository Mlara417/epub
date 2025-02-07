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

    @patch("cli.commands.edit.subprocess.run")
    @patch("cli.commands.edit.os.remove")
    @patch("cli.commands.edit.os.path.exists")
    def test_replace_command_success(self, mock_os_path_exists, mock_os_remove, mock_subprocess_run):
        # Define the fake file paths and workspace 
        updated_file = "tests/data/new_chapter1.xhtml"
        target_file = "chapter1.xhtml"
        # The default workspace for Epub3 (see Epub3.__init__) is "epub-unzipped"
        workspace = "epub-unzipped"
        target_path = f"{workspace}/{target_file}"
 
        # Define side effect function for os.path.exists:
        # Return True only for our known files (updated file and the target file path)
        def exists_side_effect(path):
            if path in [updated_file, target_path]:
                return True
            return False
        mock_os_path_exists.side_effect = exists_side_effect
 
        # Simulate os.remove succeeding
        mock_os_remove.return_value = None
 
        # Simulate subprocess.run returning success
        mock_subprocess_run.return_value = subprocess.CompletedProcess(args=["mv"], returncode=0)
 
        # Invoke the replace command. We do not need to patch Epub3.WORKSPACE because the instance
        # already holds the default workspace "epub-unzipped".
        result = self.runner.invoke(self.app, ["edit", "file", target_file, updated_file])
 
        # Make sure the command executed successfully.
        assert result.exit_code == 0
 
        # Check that os.path.exists was called for both the updated file and the target file.
        mock_os_path_exists.assert_any_call(updated_file)
        mock_os_path_exists.assert_any_call(target_path)
 
        # Check that the file removal and moving were invoked with the correct paths.
        mock_os_remove.assert_called_with(target_path)
        mock_subprocess_run.assert_called_with(["mv", updated_file, target_path], check=True)
 
        # Optionally, check that the expected success messages are in the output.
        assert f"Removed existing file: {target_file}" in result.output
        replaced_pattern = rf"Replaced '{target_file}' with updated content from\s+'?{re.escape(updated_file)}'?\."
        assert re.search(replaced_pattern, result.output)

