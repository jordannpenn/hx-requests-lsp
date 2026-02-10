"""Test configuration for hx-requests-lsp tests."""

import sys
from pathlib import Path

# Add the package to the path for testing
package_path = Path(__file__).parent.parent / "hx_requests_lsp"
sys.path.insert(0, str(package_path.parent))
