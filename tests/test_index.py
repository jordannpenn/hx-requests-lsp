"""Tests for the index module."""

import tempfile
from pathlib import Path

import pytest

from hx_requests_lsp.index import HxRequestIndex


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace with sample files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)

        # Create Python file with hx_requests
        hx_requests_dir = root / "app" / "hx_requests"
        hx_requests_dir.mkdir(parents=True)

        (hx_requests_dir / "views.py").write_text("""
from hx_requests.hx_requests import BaseHxRequest, ModalHxRequest

class NotesCount(BaseHxRequest):
    name = "notes_count"

class EditModal(ModalHxRequest):
    name = "edit_modal"
    GET_template = "forms/edit.html"
""")

        # Create template files
        templates_dir = root / "app" / "templates" / "app"
        templates_dir.mkdir(parents=True)

        (templates_dir / "list.html").write_text("""
{% load hx_tags %}
<div>
    <span>{{ count }}</span>
    <button {% hx_post 'notes_count' %}>Refresh</button>
    <button {% hx_vals hx_request_name='edit_modal' object=item %}>Edit</button>
    <button {% hx_post 'undefined_action' %}>Broken</button>
</div>
""")

        (templates_dir / "detail.html").write_text("""
<div>
    <button {% hx_post 'edit_modal' object=item %}>Edit</button>
</div>
""")

        yield root


class TestHxRequestIndex:
    """Tests for HxRequestIndex class."""

    def test_builds_full_index(self, temp_workspace):
        """Should build index from workspace root."""
        index = HxRequestIndex(temp_workspace)
        index.build_full_index()

        # Check definitions were indexed
        assert index.get_definition("notes_count") is not None
        assert index.get_definition("edit_modal") is not None
        assert index.get_definition("nonexistent") is None

    def test_get_all_definition_names(self, temp_workspace):
        """Should return all definition names."""
        index = HxRequestIndex(temp_workspace)
        index.build_full_index()

        names = index.get_all_definition_names()

        assert "notes_count" in names
        assert "edit_modal" in names

    def test_get_usages(self, temp_workspace):
        """Should return all usages of a definition."""
        index = HxRequestIndex(temp_workspace)
        index.build_full_index()

        usages = index.get_usages("edit_modal")

        # edit_modal is used in both list.html and detail.html
        assert len(usages) == 2

    def test_get_usages_empty_for_unknown(self, temp_workspace):
        """Should return empty list for unknown names."""
        index = HxRequestIndex(temp_workspace)
        index.build_full_index()

        usages = index.get_usages("nonexistent")

        assert usages == []

    def test_find_undefined_usages(self, temp_workspace):
        """Should find usages that reference undefined hx_requests."""
        index = HxRequestIndex(temp_workspace)
        index.build_full_index()

        undefined = index.find_undefined_usages()

        # undefined_action is used but not defined
        names = {u.name for u in undefined}
        assert "undefined_action" in names

    def test_find_unused_definitions(self, temp_workspace):
        """Should find definitions that are never used."""
        index = HxRequestIndex(temp_workspace)
        index.build_full_index()

        # All our definitions should be used
        unused = index.find_unused_definitions()
        unused_names = {d.name for d in unused}

        # notes_count is only used in list.html
        assert "notes_count" not in unused_names

    def test_update_file_python(self, temp_workspace):
        """Should update index when Python file changes."""
        index = HxRequestIndex(temp_workspace)
        index.build_full_index()

        # Update with new content
        new_content = """
from hx_requests.hx_requests import BaseHxRequest

class NewRequest(BaseHxRequest):
    name = "new_request"
"""
        hx_file = temp_workspace / "app" / "hx_requests" / "views.py"
        index.update_file(hx_file, new_content)

        # Old definitions should be gone, new one should exist
        assert index.get_definition("notes_count") is None
        assert index.get_definition("new_request") is not None

    def test_update_file_template(self, temp_workspace):
        """Should update index when template file changes."""
        index = HxRequestIndex(temp_workspace)
        index.build_full_index()

        initial_usages = len(index.get_usages("edit_modal"))

        # Update template with additional usage
        new_content = """
<div>
    <button {% hx_post 'edit_modal' %}>Edit 1</button>
    <button {% hx_post 'edit_modal' %}>Edit 2</button>
    <button {% hx_post 'edit_modal' %}>Edit 3</button>
</div>
"""
        template_file = temp_workspace / "app" / "templates" / "app" / "list.html"
        index.update_file(template_file, new_content)

        # Should have more usages now (3 in list.html + 1 in detail.html)
        assert len(index.get_usages("edit_modal")) == 4

    def test_remove_file(self, temp_workspace):
        """Should remove file from index."""
        index = HxRequestIndex(temp_workspace)
        index.build_full_index()

        # Remove the Python file
        hx_file = temp_workspace / "app" / "hx_requests" / "views.py"
        index.remove_file(hx_file)

        # Definitions should be gone
        assert index.get_definition("notes_count") is None
        assert index.get_definition("edit_modal") is None

    def test_get_definitions_in_file(self, temp_workspace):
        """Should return definitions from a specific file."""
        index = HxRequestIndex(temp_workspace)
        index.build_full_index()

        hx_file = temp_workspace / "app" / "hx_requests" / "views.py"
        definitions = index.get_definitions_in_file(hx_file)

        names = {d.name for d in definitions}
        assert names == {"notes_count", "edit_modal"}

    def test_get_usages_in_file(self, temp_workspace):
        """Should return usages from a specific file."""
        index = HxRequestIndex(temp_workspace)
        index.build_full_index()

        template_file = temp_workspace / "app" / "templates" / "app" / "list.html"
        usages = index.get_usages_in_file(template_file)

        names = {u.name for u in usages}
        assert "notes_count" in names
        assert "edit_modal" in names
        assert "undefined_action" in names

    def test_thread_safety(self, temp_workspace):
        """Index operations should be thread-safe."""
        import threading

        index = HxRequestIndex(temp_workspace)
        index.build_full_index()

        errors = []

        def reader():
            try:
                for _ in range(100):
                    index.get_all_definition_names()
                    index.get_usages("edit_modal")
            except Exception as e:
                errors.append(e)

        def writer():
            try:
                for _ in range(100):
                    index.update_file(
                        temp_workspace / "app" / "hx_requests" / "views.py",
                        'class X(BaseHxRequest):\n    name = "x"',
                    )
            except Exception as e:
                errors.append(e)

        threads = [
            threading.Thread(target=reader),
            threading.Thread(target=reader),
            threading.Thread(target=writer),
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread safety errors: {errors}"
