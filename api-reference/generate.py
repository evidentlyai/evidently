#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pdoc>=16.0.0",
#     "sniffio>=1.3.1", # bump litestar and then remove sniffio from here
#     "tracely>=0.2.12",
#     "typer>=0.3",
#     "sqlalchemy>=2.0.0",
#     "alembic>=1.13.0",
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
GITHUB_REPO_URL = "https://github.com/evidentlyai/evidently"
THEME_DIR = "evidently-theme"
OUTPUT_DIR = "dist"

# Get the script's directory (api-reference directory) to ensure paths are always correct
SCRIPT_DIR = Path(__file__).parent.resolve()
THEME_DIR_PATH = SCRIPT_DIR / THEME_DIR
OUTPUT_DIR_PATH = SCRIPT_DIR / OUTPUT_DIR
PDOC_ENTRYPOINT = SCRIPT_DIR / "_pdoc_entrypoint.py"


# pdoc flags (will be set dynamically to use absolute paths)
def get_pdoc_flags() -> list[str]:
    """Get pdoc flags with correct theme path."""
    return [
        # "--no-include-undocumented",
        "--no-show-source",
        "-t",
        str(THEME_DIR_PATH),
        # "--logo",
        # "https://demo.evidentlyai.com/static/img/evidently-ai-logo.png",
        "--favicon",
        "https://demo.evidentlyai.com/favicon.ico",
    ]


def becho(message: str) -> None:
    """Print blue message."""
    print(f"\033[36m{message}\033[0m")


def yecho(message: str) -> None:
    """Print yellow message."""
    print(f"\033[33m{message}\033[0m")


def merge_modules_with_defaults(modules: list[str] | None = None) -> list[str]:
    # Standart modules to document
    DEFAULT_MODULES = [
        "evidently",
        # "evidently.guardrails",
        # "evidently.sdk",
        # "evidently.llm",
        # "evidently.metrics",
        # "evidently.ui.runner",
    ]

    if not modules:
        return DEFAULT_MODULES

    return modules


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


def build_with_flag_for_evidently(evidently_ref: str) -> list[str]:
    """Build dependency flags list with the appropriate flag and ref pair."""
    flag = "--with-editable" if evidently_ref.startswith("/") else "--with"
    return [flag, evidently_ref]


def format_revision_name(revision: str) -> str:
    """Format a git revision (branch, tag, or commit) into a clean directory name format."""
    # Check if it's a hash (hexadecimal string, typically 7-40 characters)
    if re.match(r"^[0-9a-f]{7,40}$", revision.lower()):
        prefix = "hash-"
    # Check if it's a branch (contains "/" which is common in branch names)
    elif "/" in revision:
        prefix = "branch-"
    else:
        # Leave as is (could be a tag or simple branch name)
        prefix = ""

    formatted = revision.replace("/", "-").lower()
    return f"{prefix}{formatted}" if prefix else formatted


def format_local_path(path: Path) -> str:
    """Format a local file system path into a clean directory name format."""
    path_str = str(path).lower()

    if path_str.startswith("/"):
        return path_str[1:].replace("/", "-")

    return path_str.replace("/", "-")


def generate_docs_by_git_revision(
    revision: str,
    no_cache: bool = False,
    uv_run_flags: str = "",
    modules: list[str] | None = None,
    repo_url: str | None = None,
    api_reference_index_href: str = "/",
) -> None:
    """Generate documentation from a git revision (branch, tag, or commit)."""
    github_repo_url = repo_url or GITHUB_REPO_URL
    github_blob_prefix = f"{github_repo_url}/blob"
    evidently_ref = f"git+{github_repo_url}.git@{revision}"

    becho("Generating documentation for git revision...")
    yecho(revision)

    version = format_revision_name(revision).replace("-", ": ", 1)
    github_blob_url = f"{github_blob_prefix}/{revision}/src/evidently/"
    output_path = OUTPUT_DIR_PATH / format_revision_name(revision)

    modules_to_use = merge_modules_with_defaults(modules)

    run_pdoc(
        version=version,
        evidently_ref=evidently_ref,
        github_blob_url=github_blob_url,
        output_path=str(output_path),
        no_cache=no_cache,
        uv_run_flags=uv_run_flags,
        modules=modules_to_use,
        api_reference_index_href=api_reference_index_href,
    )


def generate_docs_by_pypi_version(
    version: str,
    no_cache: bool = False,
    uv_run_flags: str = "",
    modules: list[str] | None = None,
    repo_url: str | None = None,
    api_reference_index_href: str = "/",
) -> None:
    """Generate documentation from a PyPI package version."""
    evidently_ref = f"evidently=={version}"

    becho(f"Generating documentation for PyPI version {version}...")

    github_repo_url = repo_url or GITHUB_REPO_URL
    github_blob_prefix = f"{github_repo_url}/blob"
    version_label = f"Version: {version}"
    github_blob_url = f"{github_blob_prefix}/v{version}/src/evidently/"
    output_path = OUTPUT_DIR_PATH / version

    modules_to_use = merge_modules_with_defaults(modules)

    run_pdoc(
        version=version_label,
        evidently_ref=evidently_ref,
        github_blob_url=github_blob_url,
        output_path=str(output_path),
        no_cache=no_cache,
        uv_run_flags=uv_run_flags,
        modules=modules_to_use,
        api_reference_index_href=api_reference_index_href,
    )


def generate_docs_from_local_source(
    no_cache: bool = False,
    uv_run_flags: str = "",
    modules: list[str] | None = None,
    watch: bool = False,
    repo_url: str | None = None,
    api_reference_index_href: str = "/",
) -> None:
    """Generate documentation from a local source."""
    path_to_evidently = Path(__file__).parent.parent.resolve()

    becho("Generating documentation for local path...")
    yecho(path_to_evidently)

    github_repo_url = repo_url or GITHUB_REPO_URL
    github_blob_prefix = f"{github_repo_url}/blob"
    version = f"Local file: {path_to_evidently}"
    github_blob_url = f"{github_blob_prefix}/main/src/evidently/"
    output_path = OUTPUT_DIR_PATH / format_local_path(path_to_evidently)

    modules_to_use = merge_modules_with_defaults(modules)

    run_pdoc(
        version=version,
        evidently_ref=str(path_to_evidently),
        github_blob_url=github_blob_url,
        output_path=str(output_path),
        no_cache=no_cache,
        uv_run_flags=uv_run_flags,
        modules=modules_to_use,
        watch=watch,
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
    watch: bool = False,
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
        "python",
        str(PDOC_ENTRYPOINT),
        *get_pdoc_flags(),
        "-e",
        f"evidently={github_blob_url}",
        *(["-o", output_path] if not watch else []),
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
    git_revision: str = Option(
        None, "--git-revision", help="Git revision (branch, tag, or commit) to generate documentation from"
    ),
    pypi_version: str = Option(None, "--pypi-version", help="PyPI package version to generate documentation from"),
    local_source_code: bool = Option(
        False, "--local-source-code", help="Generate documentation from local source code"
    ),
    # Additional flags
    watch: bool = Option(
        False,
        "--watch",
        help="Watch mode: run pdoc web server instead of generating output files (requires --local-source-code)",
    ),
    no_cache: bool = Option(False, "--no-cache", help="Disable cache for uv run"),
    uv_run_flags: str = Option("", "--uv-run-flags", help="Additional flags to pass to uv run (space-separated)"),
    modules: str = Option(
        None, "--modules", help="Comma-separated list of modules to document (default: just top level 'evidently')"
    ),
    repo_url: str = Option(
        None, "--repo-url", help="Custom GitHub repository URL (default: https://github.com/evidentlyai/evidently)"
    ),
    api_reference_index_href: str = Option(
        "/", "--api-reference-index-href", help="Href path for the 'All versions' link (default: '/')"
    ),
):
    """Generate documentation for Evidently.

    You must specify exactly one of: --git-revision, --pypi-version, or --local-source-code.
    """
    # Validate that exactly one source is provided
    provided_count = sum(
        [
            1 if git_revision else 0,
            1 if pypi_version else 0,
            1 if local_source_code else 0,
        ]
    )

    if provided_count == 0:
        raise BadParameter("You must specify exactly one of: --git-revision, --pypi-version, or --local-source-code")
    if provided_count > 1:
        raise BadParameter("You can only specify one of: --git-revision, --pypi-version, or --local-source-code")

    # Validate watch mode is only used with local source code
    if watch and not local_source_code:
        raise BadParameter("--watch mode can only be used with --local-source-code")

    modules_list = None
    if modules:
        modules_list = [m.strip() for m in modules.split(",") if m.strip()]

    if pypi_version:
        generate_docs_by_pypi_version(
            version=pypi_version,
            no_cache=no_cache,
            uv_run_flags=uv_run_flags,
            modules=modules_list,
            repo_url=repo_url,
            api_reference_index_href=api_reference_index_href,
        )
    elif git_revision:
        generate_docs_by_git_revision(
            revision=git_revision,
            no_cache=no_cache,
            uv_run_flags=uv_run_flags,
            modules=modules_list,
            repo_url=repo_url,
            api_reference_index_href=api_reference_index_href,
        )
    elif local_source_code:
        generate_docs_from_local_source(
            no_cache=no_cache,
            uv_run_flags=uv_run_flags,
            modules=modules_list,
            watch=watch,
            repo_url=repo_url,
            api_reference_index_href=api_reference_index_href,
        )

    becho("Done")


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
