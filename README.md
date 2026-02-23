# git-files-to-prompt

Pack all git-tracked files in a repo into a single file for feeding into AI models.

## Install

**From PyPI:**
```sh
uv tool install git-files-to-prompt
```

**From GitHub:**
```sh
# HTTPS (public)
uv tool install "git+https://github.com/jeremy-jen/utils#subdirectory=utils/git_files_to_prompt"

# SSH (Host github alias)
uv tool install "git+ssh://github/jeremy-jen/utils#subdirectory=utils/git_files_to_prompt"
```

**Run without installing:**
```sh
uvx git-files-to-prompt
```

## Usage

```
git-files-to-prompt [-d DIR] [-i PATTERN ...] [-e PATTERN ...] [-o OUTPUT_DIR] [-n NAME] [-f {txt,xml}]
```

| Flag | Description |
|------|-------------|
| `-d`, `--dir` | Input directory (must be a git repo). Defaults to `.` |
| `-i`, `--include` | Glob patterns to include (e.g. `*.py *.md`) |
| `-e`, `--exclude` | Glob patterns to exclude (e.g. `*.lock`) |
| `-o`, `--output-dir` | Output directory. Defaults to `<git-root>/__local__/` |
| `-n`, `--name` | Output filename without extension. Defaults to the repo directory name |
| `-f`, `--format` | `xml` (default) or `txt` |

## Examples

```sh
# Pack everything in the current repo
git-files-to-prompt

# Pack only Python and Markdown files, excluding tests
git-files-to-prompt -i '*.py' '*.md' -e 'tests/*'

# Pack a specific repo, write to a custom location
git-files-to-prompt -d ~/projects/myapp -o ~/Desktop -n myapp-snapshot
```

## Output formats

XML (default) — wraps each file in `<source>` tags:
```xml
<source path="src/main.py">
...file content...
</source>
```

Text (`-f txt`) — uses plain separators:
```
=== src/main.py ===
...file content...
```

After writing the file, prints a summary: `Packed N files → path/to/output.xml` with line, character, and estimated token counts.

## Library usage

```python
from git_files_to_prompt import files_to_prompt

out_path = files_to_prompt(
    input_dir=".",
    patterns_incl=["*.py"],
    patterns_excl=["tests/*"],
    output_ext="xml",
)
```
