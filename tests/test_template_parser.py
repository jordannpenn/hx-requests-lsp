"""Tests for the template parser module."""

import pytest

from hx_requests_lsp.template_parser import (
    HxRequestUsage,
    get_hx_request_name_at_position,
    parse_template_for_hx_requests,
)


class TestParseTemplateForHxRequests:
    """Tests for parse_template_for_hx_requests function."""

    def test_parses_hx_post_single_quotes(self):
        """Should parse hx_post tag with single-quoted name."""
        content = "{% hx_post 'update_status' object=item %}"
        usages = parse_template_for_hx_requests(content)

        assert len(usages) == 1
        assert usages[0].name == "update_status"
        assert usages[0].tag_type == "hx_post"

    def test_parses_hx_post_double_quotes(self):
        """Should parse hx_post tag with double-quoted name."""
        content = '{% hx_post "update_status" object=item %}'
        usages = parse_template_for_hx_requests(content)

        assert len(usages) == 1
        assert usages[0].name == "update_status"

    def test_parses_hx_get_tag(self):
        """Should parse hx_get tag."""
        content = "{% hx_get 'fetch_data' %}"
        usages = parse_template_for_hx_requests(content)

        assert len(usages) == 1
        assert usages[0].name == "fetch_data"
        assert usages[0].tag_type == "hx_get"

    def test_parses_hx_request_tag(self):
        """Should parse hx_request tag."""
        content = "{% hx_request 'my_request' %}"
        usages = parse_template_for_hx_requests(content)

        assert len(usages) == 1
        assert usages[0].name == "my_request"
        assert usages[0].tag_type == "hx_request"

    def test_parses_hx_vals_with_hx_request_name(self):
        """Should parse hx_vals tag with hx_request_name keyword argument."""
        content = "{% hx_vals hx_request_name='modal_form' title='Edit' %}"
        usages = parse_template_for_hx_requests(content)

        assert len(usages) == 1
        assert usages[0].name == "modal_form"
        assert usages[0].tag_type == "hx_vals"

    def test_parses_multiple_usages_same_line(self):
        """Should parse multiple usages on the same line."""
        content = "{% hx_post 'first' %} {% hx_post 'second' %}"
        usages = parse_template_for_hx_requests(content)

        assert len(usages) == 2
        names = {u.name for u in usages}
        assert names == {"first", "second"}

    def test_parses_multiple_lines(self):
        """Should parse usages across multiple lines."""
        content = """
<button {% hx_post 'action_one' %}>One</button>
<button {% hx_post 'action_two' %}>Two</button>
<button {% hx_get 'fetch_three' %}>Three</button>
"""
        usages = parse_template_for_hx_requests(content)

        assert len(usages) == 3
        names = {u.name for u in usages}
        assert names == {"action_one", "action_two", "fetch_three"}

    def test_tracks_line_numbers(self):
        """Should correctly track line numbers."""
        content = """line 1
{% hx_post 'first' %}
line 3
{% hx_post 'second' %}
"""
        usages = parse_template_for_hx_requests(content)

        first = next(u for u in usages if u.name == "first")
        second = next(u for u in usages if u.name == "second")

        assert first.line_number == 2
        assert second.line_number == 4

    def test_tracks_column_positions(self):
        """Should correctly track column positions."""
        content = "  {% hx_post 'my_action' %}"
        usages = parse_template_for_hx_requests(content)

        assert len(usages) == 1
        # Column should point to start of 'my_action' (after the quote)
        assert usages[0].column == 14  # Position of 'm' in 'my_action'

    def test_ignores_variable_references(self):
        """Should ignore variable references with dots."""
        content = "{% hx_post some_var.hx_name %}"
        usages = parse_template_for_hx_requests(content)

        # Variable references should be skipped
        assert len(usages) == 0

    def test_marks_quoted_names_as_not_variable(self):
        """Quoted names should have is_variable=False."""
        content = "{% hx_post 'my_request' %}"
        usages = parse_template_for_hx_requests(content)

        assert len(usages) == 1
        assert usages[0].is_variable is False

    def test_marks_unquoted_names_as_variable(self):
        """Unquoted names (template variables) should have is_variable=True."""
        content = "{% hx_post task_hx_name object=item %}"
        usages = parse_template_for_hx_requests(content)

        assert len(usages) == 1
        assert usages[0].name == "task_hx_name"
        assert usages[0].is_variable is True

    def test_hx_vals_quoted_is_not_variable(self):
        """hx_vals with quoted name should have is_variable=False."""
        content = "{% hx_vals hx_request_name='my_modal' %}"
        usages = parse_template_for_hx_requests(content)

        assert len(usages) == 1
        assert usages[0].is_variable is False

    def test_hx_vals_unquoted_is_variable(self):
        """hx_vals with unquoted name should have is_variable=True."""
        content = "{% hx_vals hx_request_name=dynamic_name %}"
        usages = parse_template_for_hx_requests(content)

        assert len(usages) == 1
        assert usages[0].is_variable is True

    def test_complex_template(self):
        """Should parse a complex template with various tag types."""
        content = """
{% load hx_tags %}

<div class="container">
    <button hx-target="#modal"
            {% hx_vals hx_request_name='edit_modal'
                       object=item
                       title='Edit Item' %}>
        Edit
    </button>

    <button {% hx_post 'delete_item' object=item row_object=item %}>
        Delete
    </button>

    <div hx-get="{% hx_get 'refresh_list' %}">
        Refresh
    </div>
</div>
"""
        usages = parse_template_for_hx_requests(content)

        names = {u.name for u in usages}
        assert "edit_modal" in names
        assert "delete_item" in names
        assert "refresh_list" in names


class TestGetHxRequestNameAtPosition:
    """Tests for get_hx_request_name_at_position function."""

    def test_returns_name_when_cursor_on_name(self):
        """Should return name when cursor is positioned on the name."""
        content = "{% hx_post 'my_action' %}"
        # Cursor on 'a' in 'my_action'
        result = get_hx_request_name_at_position(content, 1, 14)

        assert result is not None
        name, start, end = result
        assert name == "my_action"

    def test_returns_none_when_cursor_outside_name(self):
        """Should return None when cursor is not on a name."""
        content = "{% hx_post 'my_action' %}"
        # Cursor at the beginning
        result = get_hx_request_name_at_position(content, 1, 0)

        assert result is None

    def test_handles_multiline_content(self):
        """Should handle multiline content correctly."""
        content = """line 1
{% hx_post 'target' %}
line 3"""
        result = get_hx_request_name_at_position(content, 2, 13)

        assert result is not None
        name, _, _ = result
        assert name == "target"

    def test_returns_none_for_invalid_line(self):
        """Should return None for out-of-bounds line number."""
        content = "{% hx_post 'action' %}"
        result = get_hx_request_name_at_position(content, 999, 0)

        assert result is None
