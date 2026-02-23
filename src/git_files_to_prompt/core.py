import subprocess
import sys
import os
from typing import Literal


def files_to_prompt(
    input_dir: str = ".",
    patterns_incl: list[str] = None,
    patterns_excl: list[str] = None,
    output_dir: str = None,
    output_name: str = None,
    output_ext: Literal["txt", "xml"] = "xml",
) -> str:
    """Concatenate git-tracked files into a single file with optional XML wrapping.

    Args:
        patterns_incl: Git glob patterns to include (e.g. ['*.py', '*.md']). None = all tracked files.
        patterns_excl: Git glob patterns to exclude (e.g. ['*.lock', '*.min.js']).
        output_dir: Directory for output file. Defaults to <git-root>/__local__/.
        output_name: Output filename without extension.
        output_ext: 'xml' wraps each file in <source> tags, 'txt' uses plain separators.

    Returns:
        Path to the generated output file.
    """
    if not os.path.isdir(input_dir):
        print(f"Error: '{input_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    cmd = ["git", "ls-files"]
    if patterns_incl:
        cmd += ["--"] + patterns_incl
    if patterns_excl:
        for pat in patterns_excl:
            cmd += [f":!:{pat}"]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=input_dir)
    file_list = [f for f in result.stdout.strip().split("\n") if f]

    if not file_list:
        print("No files matched the given patterns.")
        sys.exit(1)

    parts = []
    for fpath in file_list:
        full_path = os.path.join(input_dir, fpath)
        try:
            with open(full_path, "r") as f:
                content = f.read()
        except UnicodeDecodeError:
            continue

        if output_ext == "xml":
            parts.append(f'<source path="{fpath}">')
            parts.append(content)
            parts.append("</source>")
        else:
            parts.append(f"=== {fpath} ===")
            parts.append(content)
        parts.append("")

    output = "\n".join(parts)

    git_root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True, cwd=input_dir
    ).stdout.strip()
    out_dir = output_dir or os.path.join(git_root, "__local__")
    output_name = output_name or os.path.basename(os.path.realpath(input_dir))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{output_name}.{output_ext}")

    with open(out_path, "w") as f:
        f.write(output)

    num_chars = len(output)
    num_lines = output.count("\n")
    num_tokens = num_chars // 4
    print(f"Packed {len(file_list)} files → {out_path}")
    print(f"  {num_lines:,} lines | {num_chars:,} chars | ~{num_tokens:,} tokens")

    return out_path
