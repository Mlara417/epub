from typer.testing import CliRunner
from unittest.mock import patch
from cli.main import get_app
from cli.src.exceptions import ValidationError

class TestSetupCommands:
    CLEANUP_FUNCTION = "cli.src.epub3.Epub3.cleanup"
    INIT_FUNCTION = "cli.src.epub3.Epub3.init"
    VALIDATE_FUNCTION = "cli.src.epub3.Epub3.validate_epub"
    
    def setup_method(self):
        self.runner = CliRunner()
        self.app = get_app()
        self.epub_path = "tests/data/output.epub"
    
    def test_setup_command_success(self):
        with patch(self.INIT_FUNCTION, return_value=None) as mock_init:
            result = self.runner.invoke(self.app, ["setup", self.epub_path])

            assert result.exit_code == 0
            assert "Workspace created from provided EPUB" in result.stdout

            mock_init.assert_called_once_with(self.epub_path)

    def test_setup_command_workspace_exists(self):
        with patch(self.INIT_FUNCTION, side_effect=FileExistsError("[Errno 17] File exists:")) as mock_init:
            result = self.runner.invoke(self.app, ["setup", self.epub_path])

            assert result.exit_code == 1
            assert "[Errno 17] File exists:" in result.stdout

    def test_clean_command_success(self) -> None:
        with patch(self.CLEANUP_FUNCTION, return_value=None) as mock_init:
            result = self.runner.invoke(self.app, ["clean"])

            assert result.exit_code == 0
            assert "Workspace cleaned" in result.stdout

            mock_init.assert_called_once_with()

    def test_clean_command_file_doesnt_exist(self) -> None:
        with patch(self.CLEANUP_FUNCTION, side_effect=FileNotFoundError("Workspace doesn't exist")) as mock_init:
            result = self.runner.invoke(self.app, ["clean"])

            assert result.exit_code == 1
            assert "Workspace doesn't exist" in result.stdout

            mock_init.assert_called_once_with()

    def test_validate_command_success(self) -> None:
        with patch(self.VALIDATE_FUNCTION, return_value=None) as mock_validate:
            result = self.runner.invoke(self.app, ["validate", self.epub_path])

            assert result.exit_code == 0
            assert "EPUB validated" in result.stdout

            mock_validate.assert_called_once_with(self.epub_path)

    def test_validate_command_failure(self) -> None:
        with patch(self.VALIDATE_FUNCTION, side_effect=ValidationError("Validation issues found")) as mock_validate:
            result = self.runner.invoke(self.app, ["validate", self.epub_path])

            assert result.exit_code == 1
            assert "Validation issues found" in result.stdout

            mock_validate.assert_called_once_with(self.epub_path)
