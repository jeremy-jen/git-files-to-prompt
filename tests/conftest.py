import subprocess
import pytest


@pytest.fixture
def git_repo(tmp_path):
    """A minimal git repo with tracked text and binary files."""
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True, capture_output=True)

    (tmp_path / "hello.py").write_text("print('hello')\n")
    (tmp_path / "notes.md").write_text("# notes\n")
    (tmp_path / "data.bin").write_bytes(bytes(range(256)))

    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, check=True, capture_output=True)

    return tmp_path
