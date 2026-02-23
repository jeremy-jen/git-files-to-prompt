import argparse
from git_files_to_prompt.core import files_to_prompt


def main():
    parser = argparse.ArgumentParser(description="Pack git-tracked files into a single file.")
    parser.add_argument("-d", "--dir", dest="input_dir", help="Input directory (must be a git repo)")
    parser.add_argument("-i", "--include", nargs="+", dest="patterns_incl", help="Glob patterns to include")
    parser.add_argument("-e", "--exclude", nargs="+", dest="patterns_excl", help="Glob patterns to exclude")
    parser.add_argument("-o", "--output-dir", dest="output_dir", help="Output directory")
    parser.add_argument("-n", "--name", dest="output_name", help="Output filename (without extension)")
    parser.add_argument("-f", "--format", choices=["txt", "xml"], dest="output_ext", help="Output format")

    kwargs = {k: v for k, v in vars(parser.parse_args()).items() if v is not None}
    files_to_prompt(**kwargs)


if __name__ == "__main__":
    main()
