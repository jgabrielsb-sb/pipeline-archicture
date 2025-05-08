import pytest
from packag.modules.pipeline.operations.formatters.removeZerosFromBeginningFormatter import RemoveZerosFromBeginningFormatter

def test_remove_zeros_from_beginning_formatter_with_leading_zeros():
    """Test if leading zeros are removed from the specified columns."""
    formatter = RemoveZerosFromBeginningFormatter(columns=['number', 'code'])
    input_data = {
        'number': '00000120',
        'code': '00123',
        'other': '000456'  # Should not be affected
    }
    expected = {
        'number': '120',
        'code': '123',
        'other': '000456'
    }
    assert formatter.run(input_data) == expected

def test_remove_zeros_from_beginning_formatter_with_no_leading_zeros():
    """Test if strings without leading zeros remain unchanged."""
    formatter = RemoveZerosFromBeginningFormatter(columns=['number', 'code'])
    input_data = {
        'number': '120',
        'code': '123',
        'other': '456'
    }
    expected = {
        'number': '120',
        'code': '123',
        'other': '456'
    }
    assert formatter.run(input_data) == expected

def test_remove_zeros_from_beginning_formatter_with_all_zeros():
    """Test if a string of all zeros returns a single zero."""
    formatter = RemoveZerosFromBeginningFormatter(columns=['number'])
    input_data = {
        'number': '0000',
        'other': '0000'
    }
    expected = {
        'number': '0',
        'other': '0000'
    }
    assert formatter.run(input_data) == expected

def test_remove_zeros_from_beginning_formatter_with_empty_string():
    """Test if an empty string returns an empty string."""
    formatter = RemoveZerosFromBeginningFormatter(columns=['number'])
    input_data = {
        'number': '',
        'other': ''
    }
    expected = {
        'number': '',
        'other': ''
    }
    assert formatter.run(input_data) == expected

def test_remove_zeros_from_beginning_formatter_with_non_string_input():
    """Test if TypeError is raised for non-string input."""
    formatter = RemoveZerosFromBeginningFormatter(columns=['number'])
    input_data = {
        'number': 12345,
        'other': '12345'
    }
    with pytest.raises(TypeError):
        formatter.run(input_data) 