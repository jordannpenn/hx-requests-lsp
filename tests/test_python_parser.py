"""Tests for the Python parser module."""

import pytest

from hx_requests_lsp.python_parser import (
    HxRequestDefinition,
    parse_hx_requests_from_source,
)


class TestParseHxRequestsFromSource:
    """Tests for parse_hx_requests_from_source function."""

    def test_parses_basic_hx_request_class(self):
        """Should parse a basic HxRequest class with name attribute."""
        source = """
from hx_requests.hx_requests import BaseHxRequest

class NotesCount(BaseHxRequest):
    name = "notes_count"

    def get_response_html(self, **kwargs):
        return "42"
"""
        definitions = parse_hx_requests_from_source(source)

        assert len(definitions) == 1
        assert definitions[0].name == "notes_count"
        assert definitions[0].class_name == "NotesCount"
        assert "BaseHxRequest" in definitions[0].base_classes

    def test_parses_modal_hx_request(self):
        """Should parse a ModalHxRequest with template attributes."""
        source = """
from hx_requests.hx_requests import ModalHxRequest

class Notes(ModalHxRequest):
    name = "notes"
    GET_template = "includes/notes.html"
    modal_size_classes = "modal-lg"
"""
        definitions = parse_hx_requests_from_source(source)

        assert len(definitions) == 1
        assert definitions[0].name == "notes"
        assert definitions[0].get_template == "includes/notes.html"

    def test_parses_form_modal_hx_request(self):
        """Should parse a FormModalHxRequest."""
        source = """
from hx_requests.hx_requests import FormModalHxRequest

class EditNote(FormModalHxRequest):
    name = "edit_note"
    GET_template = "forms/edit_note.html"
    POST_template = "partials/note_row.html"
"""
        definitions = parse_hx_requests_from_source(source)

        assert len(definitions) == 1
        assert definitions[0].name == "edit_note"
        assert definitions[0].get_template == "forms/edit_note.html"
        assert definitions[0].post_template == "partials/note_row.html"

    def test_parses_multiple_classes(self):
        """Should parse multiple HxRequest classes from the same file."""
        source = """
from hx_requests.hx_requests import BaseHxRequest, ModalHxRequest

class FirstRequest(BaseHxRequest):
    name = "first_request"

class SecondRequest(ModalHxRequest):
    name = "second_request"

class NotAnHxRequest:
    name = "should_not_match"
"""
        definitions = parse_hx_requests_from_source(source)

        assert len(definitions) == 2
        names = {d.name for d in definitions}
        assert names == {"first_request", "second_request"}

    def test_ignores_classes_without_name_attribute(self):
        """Should ignore HxRequest classes that don't have a name attribute."""
        source = '''
from hx_requests.hx_requests import BaseHxRequest

class BaseMixin(BaseHxRequest):
    """A base mixin without a name."""
    pass
'''
        definitions = parse_hx_requests_from_source(source)

        assert len(definitions) == 0

    def test_parses_class_with_docstring(self):
        """Should extract docstring from HxRequest class."""
        source = '''
from hx_requests.hx_requests import BaseHxRequest

class DocumentedRequest(BaseHxRequest):
    """This is a documented request.

    It does something useful.
    """
    name = "documented_request"
'''
        definitions = parse_hx_requests_from_source(source)

        assert len(definitions) == 1
        assert definitions[0].docstring is not None
        assert "documented request" in definitions[0].docstring

    def test_tracks_line_numbers(self):
        """Should correctly track line numbers for definitions."""
        source = """
from hx_requests.hx_requests import BaseHxRequest

class FirstRequest(BaseHxRequest):
    name = "first"

class SecondRequest(BaseHxRequest):
    name = "second"
"""
        definitions = parse_hx_requests_from_source(source)

        first = next(d for d in definitions if d.name == "first")
        second = next(d for d in definitions if d.name == "second")

        assert first.line_number == 4
        assert second.line_number == 7

    def test_handles_inheritance_from_custom_base(self):
        """Should detect HxRequest classes that inherit from custom bases ending in HxRequest."""
        source = """
class CustomBaseHxRequest:
    pass

class MyRequest(CustomBaseHxRequest):
    name = "my_request"
"""
        definitions = parse_hx_requests_from_source(source)

        assert len(definitions) == 1
        assert definitions[0].name == "my_request"

    def test_handles_tabs_router(self):
        """Should detect BaseTabsRouter classes."""
        source = """
from hx_requests.hx_requests import BaseTabsRouter

class SidePanelTabs(BaseTabsRouter):
    name = "side_panel_tabs"
    tabs = []
"""
        definitions = parse_hx_requests_from_source(source)

        assert len(definitions) == 1
        assert definitions[0].name == "side_panel_tabs"

    def test_handles_syntax_error_gracefully(self):
        """Should return empty list for files with syntax errors."""
        source = """
class Broken(
    name = "broken"
"""
        definitions = parse_hx_requests_from_source(source)

        assert definitions == []

    def test_handles_mixin_inheritance(self):
        """Should detect classes that use HxRequest mixins."""
        source = """
from dynpy_gfl.hx_requests import TriggerRowRefreshMixin
from hx_requests.hx_requests import BaseHxRequest

class RefreshableRequest(TriggerRowRefreshMixin, BaseHxRequest):
    name = "refreshable"
"""
        definitions = parse_hx_requests_from_source(source)

        assert len(definitions) == 1
        assert definitions[0].name == "refreshable"
        assert "TriggerRowRefreshMixin" in definitions[0].base_classes
        assert "BaseHxRequest" in definitions[0].base_classes
