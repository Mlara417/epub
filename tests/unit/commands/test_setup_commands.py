from typer.testing import CliRunner
from unittest.mock import patch
from cli.main import get_app
from cli.src.exceptions import ValidationError

class TestSetupCommands:
    CLEANUP = "cli.src.epub3.Epub3.cleanup"
    INIT = "cli.src.epub3.Epub3.init"
    VALIDATE = "cli.src.epub3.Epub3.validate_epub"
    
    def setup_method(self):
        self.runner = CliRunner()
        self.app = get_app()
        self.epub_path = "tests/data/output.epub"

    @patch(INIT, return_value=None)
    def test_setup_command_success(self, mock_init):
        result = self.runner.invoke(self.app, ["setup", self.epub_path])

        assert result.exit_code == 0
        assert "Workspace created from provided EPUB" in result.stdout

        mock_init.assert_called_once_with(self.epub_path)

    @patch(INIT, side_effect=FileExistsError("[Errno 17] File exists:"))
    def test_setup_command_workspace_exists(self, mock_init):
        result = self.runner.invoke(self.app, ["setup", self.epub_path])

        assert result.exit_code == 1
        assert "[Errno 17] File exists:" in result.stdout

        mock_init.assert_called_once_with(self.epub_path)

    @patch(CLEANUP, return_value=None)
    def test_clean_command_success(self, mock_clean) -> None:
        result = self.runner.invoke(self.app, ["clean"])

        assert result.exit_code == 0
        assert "Workspace cleaned" in result.stdout

        mock_clean.assert_called_once_with()

    @patch(CLEANUP, side_effect=FileNotFoundError("Workspace doesn't exist"))
    def test_clean_command_file_doesnt_exist(self, mock_clean) -> None:
        result = self.runner.invoke(self.app, ["clean"])

        assert result.exit_code == 1
        assert "Workspace doesn't exist" in result.stdout

        mock_clean.assert_called_once_with()

    @patch(VALIDATE, return_value=None)
    def test_validate_command_success(self, mock_validate) -> None:
            result = self.runner.invoke(self.app, ["validate", self.epub_path])

            assert result.exit_code == 0
            assert "EPUB validated" in result.stdout

            mock_validate.assert_called_once_with(self.epub_path)

    @patch(VALIDATE, side_effect=ValidationError("Validation issues found"))
    def test_validate_command_failure(self, mock_validate) -> None:
            result = self.runner.invoke(self.app, ["validate", self.epub_path])

            assert result.exit_code == 1
            assert "Validation issues found" in result.stdout

            mock_validate.assert_called_once_with(self.epub_path)
