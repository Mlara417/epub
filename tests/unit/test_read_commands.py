from typer.testing import CliRunner
from unittest.mock import patch
from cli.main import get_app

class TestReadCommands:
    GET_METADATA_VALUE = "cli.src.epub3.Epub3.get_opf_metadata_value"
    GET_METADATA_INFO = "cli.src.epub3.Epub3.get_opf_metadata_info"
    GET_TOC = "cli.src.epub3.Epub3.get_toc"
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

    @patch(GET_METADATA_INFO, return_value={
        'title': 'Test meta value',
        'creator': 'Test meta value',
        'language': 'Test meta value',
        'identifier': 'Test meta value',
        'contributor': 'Test meta value'
    })
    def test_read_info_command_success(self, mock_read_info):
        info_result = self.runner.invoke(self.app, ["read", "info"])

        assert info_result.exit_code == 0
        assert "Title: Test meta value" in info_result.stdout
        assert "Creator: Test meta value" in info_result.stdout
        assert "Language: Test meta value" in info_result.stdout
        assert "Identifier: Test meta value" in info_result.stdout
        assert "Contributor: Test meta value" in info_result.stdout
        mock_read_info.assert_called_once_with()

    @patch(GET_METADATA_INFO, side_effect=ValueError("Error reading metadata"))
    def test_read_info_command_failure(self, mock_read_info):
        info_result = self.runner.invoke(self.app, ["read", "info"])

        assert info_result.exit_code == 1
        assert "Error reading metadata" in info_result.stdout
        mock_read_info.assert_called_once_with()

    @patch(GET_TOC, return_value=[{"label": "Test Chapter", "content": "chapter1.html", "level": 0}])
    def test_read_toc_command_success(self, mock_get_toc):
        toc_result = self.runner.invoke(self.app, ["read", "toc"])

        assert toc_result.exit_code == 0
        # "Table of Contents:" should be printed first.
        assert "Table of Contents:" in toc_result.stdout
        # The TOC item should be printed with its bullet and content.
        assert "• Test Chapter (chapter1.html)" in toc_result.stdout
        mock_get_toc.assert_called_once_with()

    @patch(GET_TOC, return_value=[])
    def test_read_toc_command_empty(self, mock_get_toc):
        toc_result = self.runner.invoke(self.app, ["read", "toc"])

        assert toc_result.exit_code == 0
        # Expected output when no TOC items are found.
        assert "No table of contents found" in toc_result.stdout
        mock_get_toc.assert_called_once_with()

    @patch(GET_TOC, side_effect=ValueError("Error reading toc"))
    def test_read_toc_command_failure(self, mock_get_toc):
        toc_result = self.runner.invoke(self.app, ["read", "toc"])

        assert toc_result.exit_code == 1
        # Ensure the error message is included in the output.
        assert "Error reading toc" in toc_result.stdout
        mock_get_toc.assert_called_once_with()
