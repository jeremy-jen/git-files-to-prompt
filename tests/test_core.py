import os
import pytest
from git_files_to_prompt.core import files_to_prompt


# --- output format ---

def test_xml_structure(git_repo, tmp_path):
    out_path = files_to_prompt(input_dir=str(git_repo), output_dir=str(tmp_path / "out"), output_ext="xml")
    content = open(out_path).read()

    assert '<source path="hello.py">' in content
    assert '<source path="notes.md">' in content
    assert "</source>" in content
    assert "print('hello')" in content
    assert "# notes" in content


def test_txt_structure(git_repo, tmp_path):
    out_path = files_to_prompt(input_dir=str(git_repo), output_dir=str(tmp_path / "out"), output_ext="txt")
    content = open(out_path).read()

    assert "=== hello.py ===" in content
    assert "=== notes.md ===" in content
    assert "print('hello')" in content
    assert "# notes" in content


# --- filters ---

def test_include_filter(git_repo, tmp_path):
    out_path = files_to_prompt(input_dir=str(git_repo), output_dir=str(tmp_path / "out"), patterns_incl=["*.py"])
    content = open(out_path).read()

    assert "hello.py" in content
    assert "notes.md" not in content


def test_exclude_filter(git_repo, tmp_path):
    out_path = files_to_prompt(input_dir=str(git_repo), output_dir=str(tmp_path / "out"), patterns_excl=["*.md"])
    content = open(out_path).read()

    assert "hello.py" in content
    assert "notes.md" not in content


def test_binary_files_are_skipped(git_repo, tmp_path):
    out_path = files_to_prompt(input_dir=str(git_repo), output_dir=str(tmp_path / "out"))
    content = open(out_path).read()

    assert "data.bin" not in content
    assert "hello.py" in content  # text files still present


# --- output file ---

def test_returns_existing_path(git_repo, tmp_path):
    out_path = files_to_prompt(input_dir=str(git_repo), output_dir=str(tmp_path / "out"))
    assert os.path.isfile(out_path)


def test_output_extension_matches_format(git_repo, tmp_path):
    for ext in ("xml", "txt"):
        out_path = files_to_prompt(input_dir=str(git_repo), output_dir=str(tmp_path / ext), output_ext=ext)
        assert out_path.endswith(f".{ext}")


def test_custom_output_name(git_repo, tmp_path):
    out_path = files_to_prompt(input_dir=str(git_repo), output_dir=str(tmp_path / "out"), output_name="my_context")
    assert os.path.basename(out_path) == "my_context.xml"


def test_default_output_name_is_input_dir_basename(git_repo, tmp_path):
    out_path = files_to_prompt(input_dir=str(git_repo), output_dir=str(tmp_path / "out"))
    expected_name = os.path.basename(os.path.realpath(str(git_repo))) + ".xml"
    assert os.path.basename(out_path) == expected_name


def test_default_output_dir_is_git_root(git_repo):
    # no output_dir passed — should land in <git_root>/__local__/
    out_path = files_to_prompt(input_dir=str(git_repo), output_name="test_output")
    assert out_path.startswith(str(git_repo / "__local__"))
    assert os.path.isfile(out_path)


def test_output_dir_is_created_if_missing(git_repo, tmp_path):
    nested = tmp_path / "a" / "b" / "c"
    assert not nested.exists()
    out_path = files_to_prompt(input_dir=str(git_repo), output_dir=str(nested))
    assert os.path.isfile(out_path)


# --- error handling ---

def test_no_match_exits(git_repo, tmp_path):
    with pytest.raises(SystemExit):
        files_to_prompt(input_dir=str(git_repo), output_dir=str(tmp_path / "out"), patterns_incl=["*.nonexistent"])
