# Evidently API Reference Documentation

Tools for generating API reference documentation using [pdoc](https://pdoc.dev/docs/pdoc.html). Documentation can be built from local source code, git revisions, or published PyPI versions.

> **To serve the generated documentation artifacts:**
> ```bash
> # cd ./docs
> npx http-server -p 3000 -c-1 ./dist
> # `-c-1` disables caching
> # you can also use other static file servers
> ```

## Quick Start

**Prerequisites:** Python 3.11+, [uv](https://github.com/astral-sh/uv), Node.js/npm

1. Generate documentation:
   ```bash
   ./api-reference/generate.py --local-source-code
   ```

2. View at `http://localhost:3000`

## Use Cases

### Local Development

```bash
# Generate static files
./api-reference/generate.py --local-source-code

# Watch mode (live updates)
./api-reference/generate.py --local-source-code --watch
```

### Git Revisions

```bash
# Branch, tag, or commit
./api-reference/generate.py --git-revision feature/new-metrics
./api-reference/generate.py --git-revision v0.7.17
./api-reference/generate.py --git-revision abc1234
```

### PyPI Versions

```bash
./api-reference/generate.py --pypi-version 0.7.17
```

### Custom Modules

```bash
./api-reference/generate.py --local-source-code --modules "evidently.metrics,evidently.guardrails"
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

Documentation is saved to `docs/dist/`:
- Local: `dist/users-<path-to-repo>/`
- Git: `dist/branch-<name>/` or `dist/hash-<hash>/`
- PyPI: `dist/<version>/`

## Troubleshooting

- **Changes not updating:** Use `--no-cache` or clear `dist/`
- **Import errors:** Verify paths and dependencies, use `--no-cache`
- **Watch mode:** Requires `--local-source-code`
