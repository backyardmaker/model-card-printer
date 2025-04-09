"""
Unit tests for core.py
"""
# Standard Library Imports
import os
import sys

# Third-party Imports
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Local Application Imports
from model_card_printer.core import (
    ModelCardPrinter
)
from fixtures.core_data import (
    test_ModelCardPrinter
)

@pytest.mark.parametrize("test_inputs", test_ModelCardPrinter)
def test_ModelCardPrinter(test_inputs: dict) -> None:
    """
    Test Case 1: Successfully execute 'generate_card' method.
    """
    # Get expected output
    expected_output = test_inputs["test_generate_card"]

    # Get actual output
    actual_output = ModelCardPrinter.generate_card()

    # Assert output type is correct
    assert isinstance(actual_output, type(expected_output))

    # Assert 'created_date' attribute is not None
    assert actual_output.created_date is not None

    """
    Test Case 2: Successfully raise ValueError when executing 'load_from_json' method (missing JSON file path).
    """
    # Assert ValueError occurred
    with pytest.raises(ValueError) as excinfo:
        _ = ModelCardPrinter().load_from_json()
    
    # Assert error message is correct
    assert "There is no JSON file provided. Re-initialise with the JSON file path using 'file_path' parameter." in str(excinfo)

    """
    Test Case 3: Successfully raise ValueError when executing 'load_from_json' method (invalid JSON file path).
    """
    # Initialise ModelCardPrinter object with test JSON file
    mcp = ModelCardPrinter(file_path = "test_invalid_path.txt")

    # Assert ValueError occurred
    with pytest.raises(ValueError) as excinfo:
        _ = mcp.load_from_json()
    
    # Assert error message is correct
    assert "Invalid JSON file path provided: test_invalid_path.txt" in str(excinfo)

    """
    Test Case 4: Successfully execute 'load_from_json' method.
    """
    # Initialise ModelCardPrinter object with test JSON file
    mcp = ModelCardPrinter(file_path = test_inputs["test_load_from_json"]["test_input"])

    # Get actual output
    actual_output = mcp.load_from_json()

    # Assert actual and expected outputs are equal
    assert actual_output == test_inputs["test_load_from_json"]["expected_output"]

    """
    Test Case 5: Successfully raise ValueError when executing 'load_from_dict' method (missing dictionary).
    """
    # Assert ValueError occurred
    with pytest.raises(ValueError) as excinfo:
        _ = ModelCardPrinter().load_from_dict()
    
    # Assert error message is correct
    assert "There is no data dictionary provided. Re-initialise with the data dictionary using 'data_dict' parameter." in str(excinfo)

    """
    Test Case 6: Successfully execute 'load_from_dict' method.
    """
    # Initialise ModelCardPrinter object with test dictionary
    mcp = ModelCardPrinter(data_dict = test_inputs["test_load_from_dict"])

    # Get actual output
    actual_output = mcp.load_from_dict()

    # Assert actual and expected outputs are equal
    assert actual_output == test_inputs["test_load_from_json"]["expected_output"]



