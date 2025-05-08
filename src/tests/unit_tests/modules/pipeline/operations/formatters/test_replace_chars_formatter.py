import pytest
from packag.modules.pipeline.operations.formatters.replaceCharsFormatter import ReplaceCharsFormatter
from packag.modules.pipeline.utils.exceptions import ValidationError

def test_replace_chars_formatter_with_valid_input():
    """Test if characters are correctly replaced in the specified columns."""
    formatter = ReplaceCharsFormatter(
        columns=['state', 'city'],
        chars_to_replace={'RIO DE JANEIRO': 'RJ', 'SAO PAULO': 'SP'}
    )
    input_data = {
        'state': 'RIO DE JANEIRO',
        'city': 'SAO PAULO',
        'other': 'RIO DE JANEIRO'  # Should not be affected
    }
    expected = {
        'state': 'RJ',
        'city': 'SP',
        'other': 'RIO DE JANEIRO'
    }
    assert formatter.run(input_data) == expected

def test_replace_chars_formatter_with_multiple_replacements():
    """Test if multiple replacements work correctly in the same string."""
    formatter = ReplaceCharsFormatter(
        columns=['text'],
        chars_to_replace={'a': '1', 'b': '2', 'c': '3'}
    )
    input_data = {
        'text': 'abcabc',
        'other': 'abcabc'
    }
    expected = {
        'text': '123123',
        'other': 'abcabc'
    }
    assert formatter.run(input_data) == expected

def test_replace_chars_formatter_with_no_matches():
    """Test if strings without matches remain unchanged."""
    formatter = ReplaceCharsFormatter(
        columns=['text'],
        chars_to_replace={'x': 'y'}
    )
    input_data = {
        'text': 'hello',
        'other': 'hello'
    }
    expected = {
        'text': 'hello',
        'other': 'hello'
    }
    assert formatter.run(input_data) == expected

def test_replace_chars_formatter_with_empty_string():
    """Test if empty strings are handled correctly."""
    formatter = ReplaceCharsFormatter(
        columns=['text'],
        chars_to_replace={'a': 'b'}
    )
    input_data = {
        'text': '',
        'other': ''
    }
    expected = {
        'text': '',
        'other': ''
    }
    assert formatter.run(input_data) == expected

def test_replace_chars_formatter_with_invalid_chars_to_replace_type():
    """Test if ValidationError is raised for invalid chars_to_replace type."""
    with pytest.raises(ValidationError):
        ReplaceCharsFormatter(
            columns=['text'],
            chars_to_replace="not a dict"
        )

def test_replace_chars_formatter_with_invalid_chars_to_replace_keys():
    """Test if ValidationError is raised for invalid chars_to_replace keys."""
    with pytest.raises(ValidationError):
        ReplaceCharsFormatter(
            columns=['text'],
            chars_to_replace={1: 'a'}  # Invalid key type
        )

def test_replace_chars_formatter_with_invalid_chars_to_replace_values():
    """Test if ValidationError is raised for invalid chars_to_replace values."""
    with pytest.raises(ValidationError):
        ReplaceCharsFormatter(
            columns=['text'],
            chars_to_replace={'a': 1}  # Invalid value type
        ) 