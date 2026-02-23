#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pdoc>=16.0.0",
#     "tracely>=0.2.12",
#     "typer>=0.3",
# ]
# ///

"""
CLI script to generate api reference documentation for Evidently.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

from typer import BadParameter
from typer import Option
from typer import Typer
from typer import echo

# Constants
EVIDENTLY_GITHUB_REPO = "evidentlyai/evidently"
THEME_DIR = "evidently-theme"
OUTPUT_DIR = "dist"
SQL_EXTRAS = "[sql]"

# Get the script's directory (api-reference directory) to ensure paths are always correct
SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_DIR = SCRIPT_DIR.parent.resolve()
THEME_DIR_PATH = SCRIPT_DIR / THEME_DIR
OUTPUT_DIR_PATH = SCRIPT_DIR / OUTPUT_DIR
MAIN_MODULES = ["evidently", "evidently.core"]


# pdoc flags (will be set dynamically to use absolute paths)
def get_pdoc_flags(output_path: str, github_blob_url: str) -> list[str]:
    """Get pdoc flags with correct theme path."""

    blob_flags = ["-e", f"evidently={github_blob_url}"] if github_blob_url else []
    output_flags = ["-o", output_path]

    return [
        # "--no-include-undocumented",
        "--no-show-source",
        "-t",
        str(THEME_DIR_PATH),
        "--logo",
        "https://demo.evidentlyai.com/static/img/evidently-ai-logo.png",
        "--favicon",
        "https://demo.evidentlyai.com/favicon.ico",
        *blob_flags,
        *output_flags,
    ]


def becho(message: str) -> None:
    """Print blue message."""
    print(f"\033[36m{message}\033[0m")


def yecho(message: str) -> None:
    """Print yellow message."""
    print(f"\033[33m{message}\033[0m")


def merge_additional_modules_with_defaults(modules: list[str]) -> list[str]:
    return list(set([*MAIN_MODULES, *modules]))


def build_uv_run_flags(uv_run_flags: str = "", no_cache: bool = False) -> list[str]:
    """Build uv run flags list with defaults."""
    DEFAULT_FLAGS = ["--no-project"]

    flags = []
    flags.extend(DEFAULT_FLAGS)

    if uv_run_flags:
        flags.extend(uv_run_flags.split())
    if no_cache:
        flags.append("--no-cache")

    return flags


def add_extras_to_ref(ref: str) -> str:
    extras = SQL_EXTRAS

    if extras in ref:
        return ref

    # Result: "git+...@v0.7.16[sql]" or "/path/to/evidently[sql]"
    return f"{ref}{extras}"


def build_with_flag_for_evidently(evidently_ref: str) -> list[str]:
    """Build dependency flags list with the appropriate flag and ref pair."""
    evidently_ref = add_extras_to_ref(evidently_ref)

    is_local_path = evidently_ref.startswith("/")
    flag = "--with-editable" if is_local_path else "--with"

    return [flag, evidently_ref]


def get_revision_info(revision: str) -> tuple[str, str]:
    # Check if it's a hash (hexadecimal string, typically 7-40 characters)
    revision = revision.lower()
    if re.match(r"^[0-9a-f]{7,40}$", revision):
        return (revision, f"hash: {revision}")
    # Check if it's a semver version (e.g., v1.2.3, 1.2.3)
    elif re.match(r"^v?\d+\.\d+\.\d+$", revision):
        return (revision, revision)

    return (revision.replace("/", "-"), f"branch: {revision}")


def format_local_path(path: Path) -> str:
    """Format a local file system path into a clean directory name format."""
    path_str = str(path).lower()

    if path_str.startswith("/"):
        return path_str[1:].replace("/", "-")

    return path_str.replace("/", "-")


def build_github_repo_url(github_repo: str) -> str:
    """Build full GitHub repository URL from repo identifier (e.g., 'owner/repo')."""
    return f"https://github.com/{github_repo}"


def generate_docs_impl(
    *,
    revision: str | None,
    local_source: bool,
    no_cache: bool,
    uv_run_flags: str,
    modules: list[str],
    github_repo: str,
    api_reference_index_href: str,
    output_prefix: str = "",
) -> None:
    repo_url = build_github_repo_url(github_repo)
    github_blob_prefix = f"{repo_url}/blob"

    github_blob_url = ""
    output_path = OUTPUT_DIR_PATH / (output_prefix + format_local_path(REPO_DIR))
    version = f"Local: {REPO_DIR}"

    if revision:
        path_to_artifact, version = get_revision_info(revision)
        github_blob_url = f"{github_blob_prefix}/{revision}/src/evidently/"
        output_path = OUTPUT_DIR_PATH / (output_prefix + path_to_artifact)
        evidently_ref = f"git+{repo_url}.git@{revision}"

    if local_source:
        evidently_ref = str(REPO_DIR)
        becho("Generating documentation for local path...")
        yecho(evidently_ref)
    else:
        becho("Generating documentation for git revision...")
        yecho(revision)

    run_pdoc(
        version=version,
        evidently_ref=evidently_ref,
        github_blob_url=github_blob_url,
        output_path=str(output_path),
        no_cache=no_cache,
        uv_run_flags=uv_run_flags,
        modules=modules,
        api_reference_index_href=api_reference_index_href,
    )


def run_pdoc(
    *,
    version: str,
    evidently_ref: str,
    github_blob_url: str,
    output_path: str,
    no_cache: bool = False,
    uv_run_flags: str = "",
    modules: list[str],
    api_reference_index_href: str = "/",
) -> None:
    """Run pdoc command with the given parameters."""

    # Set environment variables
    env = os.environ.copy()
    env["VERSION"] = version
    env["API_REFERENCE_INDEX_HREF"] = api_reference_index_href

    cmd = [
        "uv",
        "run",
        *build_uv_run_flags(uv_run_flags, no_cache),
        *build_with_flag_for_evidently(evidently_ref),
        "pdoc",
        *get_pdoc_flags(output_path, github_blob_url),
        *modules,
    ]

    becho(" ".join(cmd))

    result = subprocess.run(cmd, env=env, check=False)

    if result.returncode != 0:
        echo(f"Error: Command failed with exit code {result.returncode}", err=True)
        sys.exit(result.returncode)


app = Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=False,
)


@app.callback(invoke_without_command=True)
def generate_docs(
    github_repo: str = Option(
        EVIDENTLY_GITHUB_REPO,
        "--github-repo",
        help="GitHub repository identifier (e.g., 'owner/repo', default: evidentlyai/evidently)",
    ),
    git_revision: str = Option(
        None,
        "--git-revision",
        help="Git revision (branch, tag, or commit). Required unless --local-source-code is used. "
        "When used with --local-source-code, sets the GitHub blob URL and output directory name.",
    ),
    local_source_code: bool = Option(
        False,
        "--local-source-code",
        help="Generate documentation from local source code instead of fetching from git. "
        "Can be combined with --git-revision for output naming.",
    ),
    # Additional flags
    no_cache: bool = Option(False, "--no-cache", help="Disable cache for uv run"),
    uv_run_flags: str = Option("", "--uv-run-flags", help="Additional flags to pass to uv run (space-separated)"),
    additional_modules: str = Option(
        "", "--additional-modules", help="Comma-separated list of additional modules to document"
    ),
    api_reference_index_href: str = Option(
        "/", "--api-reference-index-href", help="Href path for the 'All versions' link (default: '/')"
    ),
    output_prefix: str = Option("", "--output-prefix", help="Prefix to add to output directory path (default: '')"),
):
    """Generate documentation for Evidently.

    Usage modes:
      --git-revision <rev>                    Build from git revision
      --local-source-code                     Build from local source (output named by local path)
      --local-source-code --git-revision <rev> Build from local source (output named by revision)
    """
    # Validate: at least one of git_revision or local_source_code must be provided
    if not git_revision and not local_source_code:
        raise BadParameter("You must specify --git-revision and/or --local-source-code")

    additional_modules_list = [m.strip() for m in additional_modules.split(",") if m.strip()]
    modules = merge_additional_modules_with_defaults(additional_modules_list)

    generate_docs_impl(
        revision=git_revision,
        local_source=local_source_code,
        no_cache=no_cache,
        uv_run_flags=uv_run_flags,
        modules=modules,
        github_repo=github_repo,
        api_reference_index_href=api_reference_index_href,
        output_prefix=output_prefix,
    )

    becho("Done")


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
