import sys
from unittest.mock import patch, call
import pytest
from git_files_to_prompt.cli import main


def run_cli(*args):
    """Invoke main() with the given CLI args."""
    with patch("sys.argv", ["git-files-to-prompt", *args]):
        main()


# --- argument mapping ---

def test_dir_positional(git_repo, tmp_path):
    with patch("git_files_to_prompt.cli.files_to_prompt") as mock:
        run_cli(str(git_repo), "-o", str(tmp_path / "out"))
    mock.assert_called_once_with(input_dir=str(git_repo), output_dir=str(tmp_path / "out"))


def test_include_flag(git_repo, tmp_path):
    with patch("git_files_to_prompt.cli.files_to_prompt") as mock:
        run_cli(str(git_repo), "-i", "*.py", "*.md", "-o", str(tmp_path / "out"))
    mock.assert_called_once_with(input_dir=str(git_repo), patterns_incl=["*.py", "*.md"], output_dir=str(tmp_path / "out"))


def test_exclude_flag(git_repo, tmp_path):
    with patch("git_files_to_prompt.cli.files_to_prompt") as mock:
        run_cli(str(git_repo), "-e", "*.lock", "-o", str(tmp_path / "out"))
    mock.assert_called_once_with(input_dir=str(git_repo), patterns_excl=["*.lock"], output_dir=str(tmp_path / "out"))


def test_format_flag(git_repo, tmp_path):
    with patch("git_files_to_prompt.cli.files_to_prompt") as mock:
        run_cli(str(git_repo), "-f", "txt", "-o", str(tmp_path / "out"))
    mock.assert_called_once_with(input_dir=str(git_repo), output_ext="txt", output_dir=str(tmp_path / "out"))


def test_name_flag(git_repo, tmp_path):
    with patch("git_files_to_prompt.cli.files_to_prompt") as mock:
        run_cli(str(git_repo), "-n", "my_context", "-o", str(tmp_path / "out"))
    mock.assert_called_once_with(input_dir=str(git_repo), output_name="my_context", output_dir=str(tmp_path / "out"))


def test_no_args_passed_for_unset_flags(git_repo):
    # unset optional flags must not appear in kwargs (core handles defaults)
    with patch("git_files_to_prompt.cli.files_to_prompt") as mock:
        run_cli(str(git_repo))
    called_kwargs = mock.call_args.kwargs
    assert "patterns_incl" not in called_kwargs
    assert "patterns_excl" not in called_kwargs
    assert "output_ext" not in called_kwargs
    assert "output_name" not in called_kwargs
    assert "output_dir" not in called_kwargs


def test_invalid_format_exits():
    with patch("sys.argv", ["git-files-to-prompt", "-f", "csv"]):
        with pytest.raises(SystemExit):
            main()


# --- integration ---

def test_cli_end_to_end(git_repo, tmp_path):
    out_dir = str(tmp_path / "out")
    run_cli(str(git_repo), "-o", out_dir, "-f", "txt", "-n", "result")

    import os
    out_path = os.path.join(out_dir, "result.txt")
    assert os.path.isfile(out_path)
    content = open(out_path).read()
    assert "=== hello.py ===" in content
