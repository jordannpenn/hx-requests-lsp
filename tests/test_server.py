from lsprotocol import types as lsp

from hx_requests_lsp.server import initialize, server


class TestInitialize:
    def test_inter_file_dependencies_disabled(self):
        # DYN-8593: inter_file_dependencies=True causes VS Code to pull diagnostics
        # twice per visible file, resulting in duplicate warnings
        params = lsp.InitializeParams(
            capabilities=lsp.ClientCapabilities(),
            root_uri="file:///tmp/test-workspace",
        )

        result = initialize(server, params)

        diagnostic_options = result.capabilities.diagnostic_provider
        assert isinstance(diagnostic_options, lsp.DiagnosticOptions)
        assert diagnostic_options.inter_file_dependencies is False

    def test_workspace_diagnostics_disabled(self):
        params = lsp.InitializeParams(
            capabilities=lsp.ClientCapabilities(),
            root_uri="file:///tmp/test-workspace",
        )

        result = initialize(server, params)

        diagnostic_options = result.capabilities.diagnostic_provider
        assert isinstance(diagnostic_options, lsp.DiagnosticOptions)
        assert diagnostic_options.workspace_diagnostics is False
