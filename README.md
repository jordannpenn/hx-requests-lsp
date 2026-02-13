# hx-requests-lsp

Language Server Protocol implementation for the [hx-requests](https://github.com/yaakovLowenstein/hx-requests) Django library.

[![VS Code Extension](https://img.shields.io/visual-studio-marketplace/v/jordannpenn.hx-requests-lsp?label=VS%20Code%20Extension)](https://marketplace.visualstudio.com/items?itemName=jordannpenn.hx-requests-lsp)
[![PyPI](https://img.shields.io/pypi/v/hx-requests-lsp)](https://pypi.org/project/hx-requests-lsp/)

## Features

- **Autocomplete**: Get suggestions for hx_request names in Django templates (prioritizes current app, works with or without quotes)
- **Go-to-Definition**: Jump from template usage to the Python class definition
- **Find References**: Find all template usages of an hx_request
- **Diagnostics**: Warnings for undefined hx_request names
- **Hover Information**: View details about an hx_request on hover

## Installation

### VS Code (Recommended)

Install the [hx-requests-lsp extension](https://marketplace.visualstudio.com/items?itemName=jordannpenn.hx-requests-lsp) from the VS Code Marketplace. The extension bundles the language server - no additional setup required.

### Other Editors

Install the language server via pip:

```bash
pip install hx-requests-lsp
```

Then configure your editor to use `hx-requests-lsp --stdio`.

Example for Neovim with `nvim-lspconfig`:
```lua
require'lspconfig'.hx_requests_lsp.setup{
  cmd = {"hx-requests-lsp", "--stdio"},
  filetypes = {"html", "htmldjango", "python"},
  root_dir = require'lspconfig'.util.root_pattern("manage.py", ".git")
}
```

## Usage

Once installed, the LSP provides these features in your editor:

| Feature | Description |
|---------|-------------|
| **Go to Definition** | Jump to hx_request class from template usage |
| **Find References** | Find all template usages of an hx_request |
| **Hover Info** | View details about an hx_request on hover |
| **Autocomplete** | Get suggestions when typing `{% hx_get ` or `{% hx_post ` |
| **Diagnostics** | Warnings for undefined hx_request names |

## Supported Patterns

### Python (definitions)

```python
from hx_requests.hx_requests import BaseHxRequest, ModalHxRequest

class MyRequest(BaseHxRequest):
    name = "my_request"  # This name is indexed
    GET_template = "partials/my.html"
```

### Templates (usages)

```html
{% load hx_tags %}

<!-- hx_post with name as first argument -->
<button {% hx_post 'my_request' object=item %}>Click</button>

<!-- hx_get -->
<div {% hx_get 'another_request' %}>Load</div>

<!-- hx_vals with hx_request_name keyword -->
<div {% hx_vals hx_request_name='my_request' title='Modal' %}>Open</div>
```

## Requirements

- Python 3.11+

## Troubleshooting

### Server not found

1. Verify it's installed: `which hx-requests-lsp`
2. Make sure you're in the correct virtualenv

### No autocompletion or diagnostics

1. Ensure your template files are properly recognized by your editor
2. Restart your editor to reload the extension
3. Check that hx_request classes have a `name` attribute

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup instructions.
