# Evidently API Reference Documentation

Tools for generating API reference documentation using [pdoc](https://pdoc.dev/docs/pdoc.html). Documentation can be built from local source code or git revisions (branch, tag, or commit).

## Quick Start

**Prerequisites:** Python 3.11+, [uv](https://github.com/astral-sh/uv), Node.js/npm

Generate documentation:
   ```bash
   ./api-reference/generate.py --local-source-code
   ```


## Local Development

```bash
./api-reference/local-dev.sh
```

Starts a local development server with live reloading:
- Serves generated documentation at `http://localhost:8080` (or next available port)
- Watches for Python file changes and regenerates documentation with `./api-reference/generate.py --local-source-code`

## Use Cases

### Local Development

```bash
# Generate static files
./api-reference/generate.py --local-source-code
```

### Git Revisions

```bash
# Branch, tag, or commit
./api-reference/generate.py --git-revision feature/new-metrics
./api-reference/generate.py --git-revision v0.7.17
./api-reference/generate.py --git-revision abc1234
```

### Additional Modules

Add modules beyond the defaults (`evidently`, `evidently.core`):

```bash
./api-reference/generate.py --local-source-code --additional-modules "evidently.metrics,evidently.guardrails"
```

### Additional Options

```bash
# View all options
./api-reference/generate.py --help

# Clean build without cache
./api-reference/generate.py --local-source-code --no-cache

# Custom uv run flags
./api-reference/generate.py --local-source-code --uv-run-flags "--python 3.11"
```

## Output Structure

Documentation is saved to `api-reference/dist/`:
- Local: `dist/<path-to-repo-with-dashes>/`
- Git: `dist/<revision>/` (e.g. `dist/v0.7.17/`, `dist/feature-new-metrics/`, `dist/abc1234/`)


## Troubleshooting

- **Changes not updating:** Use `--no-cache` or clear `dist/`
- **Import errors:** Verify paths and dependencies, use `--no-cache`
- **Watch mode:** Requires `--local-source-code`
