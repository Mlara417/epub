from typer.testing import CliRunner
from unittest.mock import patch
from cli.main import get_app

class TestReadCommands:
    GET_METADATA_VALUE = "cli.src.epub3.Epub3.get_opf_metadata_value"
    
    def setup_method(self):
        self.runner = CliRunner()
        self.app = get_app()
        self.epub_path = "tests/data/output.epub"

    @patch(GET_METADATA_VALUE, return_value="Test meta value")
    def test_read_meta_command_success(self, mock_read_meta):
        meta_result = self.runner.invoke(self.app, ["read", "meta", "title"])

        assert meta_result.exit_code == 0
        assert "Test meta value" in meta_result.stdout

        mock_read_meta.assert_called_once_with("title")

    @patch(GET_METADATA_VALUE, side_effect=ValueError("Metadata tag 'title' not found"))
    def test_read_meta_command_failure(self, mock_read_meta):
        meta_result = self.runner.invoke(self.app, ["read", "meta", "title"])

        assert meta_result.exit_code == 1
        assert "Metadata tag 'title' not found" in meta_result.stdout

        mock_read_meta.assert_called_once_with("title")
