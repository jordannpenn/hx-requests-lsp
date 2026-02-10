# hx-requests-lsp

Language Server Protocol implementation for the [hx-requests](https://github.com/yaakovLowworworthy/hx-requests) Django library.

## Features

- **Autocomplete**: Get suggestions for hx_request names in Django templates
- **Go-to-Definition**: Jump from template usage to the Python class definition
- **Find References**: Find all template usages of an hx_request
- **Diagnostics**: Warnings for undefined hx_request names
- **Hover Information**: View details about an hx_request on hover

## Installation

Install via pip:

```bash
pip install hx-requests-lsp
```

Verify installation:

```bash
hx-requests-lsp --help
```

## Quick Start

### VS Code Setup

1. Install the [hx-requests-lsp VS Code extension](https://github.com/jordannpenn/hx-requests-lsp-vscode)
2. The extension will automatically find the Python server once installed
3. Open a Django template file to start using LSP features

### Configuration

If the extension can't find the server automatically, add to your VS Code `.vscode/settings.json`:

```json
{
  "hxRequestsLsp.serverPath": "/path/to/venv/bin/hx-requests-lsp"
}
```

## Usage

Once installed, the LSP provides these features in your editor:

| Feature | How to Use |
|---------|------------|
| **Go to Definition** | `F12` or `Ctrl+Click` on an hx_request name in a template |
| **Find References** | `Shift+F12` or right-click → "Find All References" |
| **Hover Info** | Hover over an hx_request name |
| **Autocomplete** | Type `{% hx_get '` or `{% hx_post '` in a template |
| **Diagnostics** | Undefined hx_request names show warnings |

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
- `pygls` >= 1.3.0 (Python Language Server library)
- `lsprotocol` >= 2023.0.0

## Development

### Running Tests

```bash
pip install pytest pytest-asyncio
pytest
```

### Testing the Server Manually

```bash
# Test that the server responds to LSP initialize
msg='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"processId":null,"rootUri":"file:///app","capabilities":{}}}'
printf "Content-Length: ${#msg}\r\n\r\n${msg}" | hx-requests-lsp --stdio
```

## Troubleshooting

### Server not found

1. Verify it's installed: `which hx-requests-lsp`
2. Check the path matches your editor's `serverPath` setting
3. Make sure you're in the correct virtualenv

### Extension shows "Activating" forever

1. Check Developer Tools console: `Ctrl+Shift+P` → "Developer: Toggle Developer Tools" → Console tab
2. Look for errors mentioning "hx-requests"

### No autocompletion or diagnostics

1. Ensure your template files are properly recognized by your editor
2. Restart your editor to reload the extension
3. Check that hx_request classes have a `name` attribute

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
