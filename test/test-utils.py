import pandas as pd
import numpy as np
import pytest
import sys
import os

# Import the encode function from the src folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.utils import encode

# Test data
test_data = pd.DataFrame({'month': [1, 4, 7, 10]})

# Test for correct input data types
def test_encode_input_data_types():
    with pytest.raises(TypeError):
        encode("not_a_dataframe", 'month', 12) # first input is not a pandas data frame
    with pytest.raises(KeyError):
        encode(test_data, 123, 12) # column input is not a string
    with pytest.raises(TypeError):
        encode(test_data, 'month', "not_a_number") # max_val is not a number

# Test for error handling with invalid column name
def test_encode_invalid_column_name():
    with pytest.raises(KeyError):
        encode(test_data, 'invalid_column', 12)
        
# Test for handling of negative max_val
def test_encode_negative_max_val():
    with pytest.raises(ValueError):
        encode(test_data, 'month', -12)
    with pytest.raises(ValueError):
        encode(test_data, 'month', -12.0)

# Test for correct return type
def test_encode_returns_dataframe():
    result = encode(test_data, 'month', 12)
    assert isinstance(result, pd.DataFrame), "encode should return a pandas DataFrame"

# Test for creation of corresponding columns
def test_encode_creates_columns():
    result = encode(test_data, 'month', 12)
    assert 'month_sin' in result.columns and 'month_cos' in result.columns, "encode should create '_sin' and '_cos' columns"

# Test for correct values in new columns
def test_encode_correct_values():
    result = encode(test_data, 'month', 12)
    expected_sin = np.sin(2 * np.pi * test_data['month'] / 12)
    expected_cos = np.cos(2 * np.pi * test_data['month'] / 12)
    pd.testing.assert_series_equal(result['month_sin'], expected_sin, check_dtype=False, check_names=False)
    pd.testing.assert_series_equal(result['month_cos'], expected_cos, check_dtype=False, check_names=False)


