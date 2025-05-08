import pytest
from packag.modules.pipeline.operations.formatters.toOnlyNumbersFormatter import ToOnlyNumbersFormatter

def test_to_only_numbers_formatter_with_leading_zeros():
    """Test if leading zeros are maintained in the specified columns."""
    formatter = ToOnlyNumbersFormatter(columns=['number', 'code'])
    input_data = {
        'number': '00000120',
        'code': '00123',
        'other': '000456'  # Should not be affected
    }
    expected = {
        'number': '00000120',
        'code': '00123',
        'other': '000456'
    }
    assert formatter.run(input_data) == expected

def test_to_only_numbers_formatter_with_special_characters():
    """Test if special characters are removed while keeping numbers."""
    formatter = ToOnlyNumbersFormatter(columns=['cpf', 'phone'])
    input_data = {
        'cpf': '083.254.754-98',
        'phone': '(11) 99999-9999',
        'other': '083.254.754-98'
    }
    expected = {
        'cpf': '08325475498',
        'phone': '11999999999',
        'other': '083.254.754-98'
    }
    assert formatter.run(input_data) == expected

def test_to_only_numbers_formatter_with_currency():
    """Test if currency symbols and commas are removed while keeping numbers."""
    formatter = ToOnlyNumbersFormatter(columns=['price'])
    input_data = {
        'price': 'R$120,00',
        'other': 'R$120,00'
    }
    expected = {
        'price': '12000',
        'other': 'R$120,00'
    }
    assert formatter.run(input_data) == expected

def test_to_only_numbers_formatter_with_text():
    """Test if text is removed while keeping numbers."""
    formatter = ToOnlyNumbersFormatter(columns=['text'])
    input_data = {
        'text': 'HEY JUDE LOOK AT ME: 120',
        'other': 'HEY JUDE LOOK AT ME: 120'
    }
    expected = {
        'text': '120',
        'other': 'HEY JUDE LOOK AT ME: 120'
    }
    assert formatter.run(input_data) == expected

def test_to_only_numbers_formatter_with_empty_string():
    """Test if empty strings are handled correctly."""
    formatter = ToOnlyNumbersFormatter(columns=['text'])
    input_data = {
        'text': '',
        'other': ''
    }
    expected = {
        'text': '',
        'other': ''
    }
    assert formatter.run(input_data) == expected

def test_to_only_numbers_formatter_with_no_numbers():
    """Test if strings with no numbers return empty strings."""
    formatter = ToOnlyNumbersFormatter(columns=['text'])
    input_data = {
        'text': 'No numbers here!',
        'other': 'No numbers here!'
    }
    expected = {
        'text': '',
        'other': 'No numbers here!'
    }
    assert formatter.run(input_data) == expected

def test_to_only_numbers_formatter_with_non_string_input():
    """Test if TypeError is raised for non-string input."""
    formatter = ToOnlyNumbersFormatter(columns=['number'])
    input_data = {
        'number': 12345,
        'other': '12345'
    }
    with pytest.raises(TypeError):
        formatter.run(input_data) 