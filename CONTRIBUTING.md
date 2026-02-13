# Contributing to hx-requests-lsp

## Development Setup

```bash
# Clone the repository
git clone https://github.com/jordannpenn/hx-requests-lsp
cd hx-requests-lsp

# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

## Running Tests

```bash
poetry run pytest
```

## Testing the Server Manually

```bash
# Test that the server responds to LSP initialize
msg='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"processId":null,"rootUri":"file:///app","capabilities":{}}}'
printf "Content-Length: ${#msg}\r\n\r\n${msg}" | poetry run hx-requests-lsp --stdio
```

## Code Style

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting. Run before committing:

```bash
poetry run ruff check .
poetry run ruff format .
```

## Commit Messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automatic versioning:

- `feat:` - New features (triggers minor version bump)
- `fix:` - Bug fixes (triggers patch version bump)
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks
- `ci:` - CI/CD changes

## Release Process

Releases are automated via GitHub Actions:

1. Push commits to `main` with conventional commit messages
2. `semantic-release` automatically creates a new version based on commit types
3. The package is published to PyPI
4. The VS Code extension repo is notified to update its bundled LSP
