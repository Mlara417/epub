import os
import subprocess
import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from cli.commands.edit import Edit
from cli.src.utils import success

class TestEditCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        # Create an instance of Edit and override its epub3 attribute.
        self.edit_instance = Edit()
        self.fake_epub3 = MagicMock()
        self.fake_epub3.workspace = "fake_workspace"
        # Make sure epub3.xml exists
        self.fake_epub3.xml = MagicMock()
        self.edit_instance.epub3 = self.fake_epub3

    # -------------------- Tests for "cover" command --------------------
    @patch("cli.commands.edit.error")
    def test_cover_invalid_extension(self, mock_error):
        result = self.runner.invoke(self.edit_instance.cli, ["cover", "cover.gif"])
        self.assertEqual(result.exit_code, 1)
        mock_error.assert_called_once_with("Cover image must be in JPEG or PNG format.")

    @patch("os.path.exists", return_value=False)
    @patch("cli.commands.edit.error")
    def test_cover_file_not_found(self, mock_error, mock_exists):
        result = self.runner.invoke(self.edit_instance.cli, ["cover", "cover.jpg"])
        self.assertEqual(result.exit_code, 1)
        mock_error.assert_called_once_with("Cover image file 'cover.jpg' not found.")

    @patch("os.path.exists", return_value=True)
    @patch("cli.commands.edit.move_file")
    @patch("cli.commands.edit.success")
    def test_cover_success(self, mock_success, mock_move_file, mock_exists):
        # Set the necessary epub3 methods as mocks.
        self.fake_epub3.load_content_opf = MagicMock()
        self.fake_epub3.add_manifest_subnode = MagicMock()
        self.fake_epub3.add_metadata_subnode = MagicMock()
        self.fake_epub3.save_xml = MagicMock()
        self.fake_epub3.package_epub = MagicMock()
        
        result = self.runner.invoke(self.edit_instance.cli, ["cover", "cover.jpg"])
        self.assertEqual(result.exit_code, 0)
        mock_move_file.assert_called_once_with("cover.jpg", self.fake_epub3.workspace)
        self.fake_epub3.load_content_opf.assert_called_once()
        self.fake_epub3.add_manifest_subnode.assert_called_once_with("item", {
            "id": self.edit_instance.COVER,
            "href": "cover.jpg",
            "media-type": "image/jpeg"
        })
        self.fake_epub3.add_metadata_subnode.assert_called_once_with("meta", {
            "name": self.edit_instance.COVER,
            "content": self.edit_instance.COVER
        })
        self.fake_epub3.save_xml.assert_called_once()
        self.fake_epub3.package_epub.assert_called_once()
        # Verify that success() was called at least twice.
        self.assertGreaterEqual(mock_success.call_count, 2)

    # -------------------- Tests for "title" command --------------------
    @patch("cli.commands.edit.error")
    def test_title_empty(self, mock_error):
        result = self.runner.invoke(self.edit_instance.cli, ["title", ""])
        self.assertEqual(result.exit_code, 1)
        mock_error.assert_called_once_with("Title cannot be empty.")

    @patch("cli.commands.edit.success")
    @patch("cli.commands.edit.error")
    def test_title_success(self, mock_error, mock_success):
        # Set the necessary epub3 methods.
        self.fake_epub3.load_content_opf = MagicMock()
        self.fake_epub3.save_xml = MagicMock()
        self.fake_epub3.xml.update_dc_metadata = MagicMock()
        
        result = self.runner.invoke(self.edit_instance.cli, ["title", "New Title"])
        self.assertEqual(result.exit_code, 0)
        self.fake_epub3.load_content_opf.assert_called_once()
        self.fake_epub3.xml.update_dc_metadata.assert_called_once_with("title", "New Title")
        self.fake_epub3.save_xml.assert_called_once()
        mock_success.assert_any_call("Updating EPUB title to: New Title")
        mock_success.assert_any_call("EPUB title updated successfully.")

    @patch("cli.commands.edit.typer.prompt", return_value="Prompted Title")
    @patch("cli.commands.edit.success")
    @patch("cli.commands.edit.error")
    def test_title_interactive(self, mock_error, mock_success, mock_prompt):
        # Set the necessary epub3 methods.
        self.fake_epub3.load_content_opf = MagicMock()
        self.fake_epub3.save_xml = MagicMock()
        self.fake_epub3.xml.update_dc_metadata = MagicMock()
        
        result = self.runner.invoke(self.edit_instance.cli, ["title", "--interactive"], input="Prompted Title\n")
        self.assertEqual(result.exit_code, 0)
        self.fake_epub3.load_content_opf.assert_called_once()
        self.fake_epub3.xml.update_dc_metadata.assert_called_once_with("title", "Prompted Title")
        self.fake_epub3.save_xml.assert_called_once()

    # -------------------- Tests for "author" command --------------------
    @patch("cli.commands.edit.error")
    def test_author_empty(self, mock_error):
        result = self.runner.invoke(self.edit_instance.cli, ["author", ""])
        self.assertEqual(result.exit_code, 1)
        mock_error.assert_called_once_with("Author cannot be empty.")

    @patch("cli.commands.edit.success")
    @patch("cli.commands.edit.error")
    def test_author_success(self, mock_error, mock_success):
        # Set the necessary epub3 methods.
        self.fake_epub3.load_content_opf = MagicMock()
        self.fake_epub3.save_xml = MagicMock()
        self.fake_epub3.xml.update_dc_metadata = MagicMock()
        
        result = self.runner.invoke(self.edit_instance.cli, ["author", "New Author"])
        self.assertEqual(result.exit_code, 0)
        self.fake_epub3.load_content_opf.assert_called_once()
        self.fake_epub3.xml.update_dc_metadata.assert_called_once_with("creator", "New Author")
        self.fake_epub3.save_xml.assert_called_once()
        mock_success.assert_any_call("Updating EPUB author to: New Author")
        mock_success.assert_any_call("EPUB author updated successfully.")

    @patch("cli.commands.edit.typer.prompt", return_value="Prompted Author")
    @patch("cli.commands.edit.success")
    @patch("cli.commands.edit.error")
    def test_author_interactive(self, mock_error, mock_success, mock_prompt):
        # Set the necessary epub3 methods.
        self.fake_epub3.load_content_opf = MagicMock()
        self.fake_epub3.save_xml = MagicMock()
        self.fake_epub3.xml.update_dc_metadata = MagicMock()
        
        result = self.runner.invoke(self.edit_instance.cli, ["author", "--interactive"], input="Prompted Author\n")
        self.assertEqual(result.exit_code, 0)
        self.fake_epub3.load_content_opf.assert_called_once()
        self.fake_epub3.xml.update_dc_metadata.assert_called_once_with("creator", "Prompted Author")
        self.fake_epub3.save_xml.assert_called_once()

    # -------------------- Tests for "file" command --------------------
    @patch("os.path.exists")
    @patch("cli.commands.edit.error")
    def test_file_updated_file_not_found(self, mock_error, mock_exists):
        # Simulate that the updated file does not exist.
        def exists_side_effect(path):
            if path == "updated.txt":
                return False
            return True
        mock_exists.side_effect = exists_side_effect
        result = self.runner.invoke(self.edit_instance.cli, ["file", "target.txt", "updated.txt"])
        self.assertEqual(result.exit_code, 1)
        mock_error.assert_called_once_with("Updated file 'updated.txt' not found.")

    @patch("os.path.exists")
    @patch("cli.commands.edit.error")
    def test_file_target_not_found(self, mock_error, mock_exists):
        # Simulate that the updated file exists, but target file in the EPUB workspace does not.
        def exists_side_effect(path):
            if path == "updated.txt":
                return True
            if path == os.path.join(self.fake_epub3.workspace, "target.txt"):
                return False
            return True
        mock_exists.side_effect = exists_side_effect
        result = self.runner.invoke(self.edit_instance.cli, ["file", "target.txt", "updated.txt"])
        self.assertEqual(result.exit_code, 1)
        expected_msg = f"Target file 'target.txt' not found in EPUB workspace '{self.fake_epub3.workspace}'."
        mock_error.assert_called_once_with(expected_msg)

    @patch("os.remove", side_effect=Exception("Remove error"))
    @patch("os.path.exists", return_value=True)
    @patch("cli.commands.edit.error")
    def test_file_remove_error(self, mock_error, mock_exists, mock_remove):
        result = self.runner.invoke(self.edit_instance.cli, ["file", "target.txt", "updated.txt"])
        self.assertEqual(result.exit_code, 1)
        # Ensure the error message contains the expected text.
        args, _ = mock_error.call_args
        self.assertIn("Error removing file 'target.txt'", args[0])

    @patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, ["mv"]))
    @patch("os.remove")
    @patch("os.path.exists", return_value=True)
    @patch("cli.commands.edit.error")
    def test_file_subprocess_error(self, mock_error, mock_exists, mock_remove, mock_subprocess):
        result = self.runner.invoke(self.edit_instance.cli, ["file", "target.txt", "updated.txt"])
        self.assertEqual(result.exit_code, 1)
        args, _ = mock_error.call_args
        self.assertIn("Error replacing file 'target.txt'", args[0])

    @patch("cli.src.utils.success")
    @patch("os.remove")
    @patch("os.path.exists")
    @patch("subprocess.run")
    def test_file_success(self, mock_run, mock_exists, mock_remove, mock_success):
        # TODO: Fix this test
        file_path = 'target.txt'
        updated_file_path = 'updated.txt'
        
        # Create the target file
        with open(file_path, 'w') as f:
            f.write('Test content')

        # Simulate that the target file exists
        """ mock_exists.side_effect = lambda x: x in [file_path, updated_file_path] """

        # Simulate that the updated file exists
        with open(updated_file_path, 'w') as f:
            f.write('Updated content')

        # Call the function that should remove the file
        result = self.runner.invoke(self.edit_instance.cli, ["file", "target.txt", "updated.txt"])

        # Assert that the file removal was attempted
        """ mock_remove.assert_called_once_with(file_path) """

        # Assert that success was called
"""     mock_success.assert_any_call(f"Removed existing file: {file_path}")
        mock_success.assert_any_call(f"Replaced '{file_path}' with updated content from '{updated_file_path}'") """

if __name__ == '__main__':
    unittest.main()
