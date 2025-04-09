"""
Fixtures used to unit test core.py
"""
# Standard Library Imports
import os
from pathlib import Path

# Local Library Imports
from model_card_printer.model_card import ModelCard

PATH_TO_TEST_JSON = Path(os.path.join("tests", "fixtures", "test_model_card.json")).resolve()

# Create expected model card output when loading "test_model_card.json"
expected_mc = ModelCard()
expected_mc.model_details.model_name = "test model"
expected_mc.model_details.documentation = "# Test Model Documentation"
expected_mc.created_date = "05 April 2025"

test_ModelCardPrinter = [(
    {
        "test_generate_card": ModelCard(),
        "test_load_from_json": {
            "test_input": PATH_TO_TEST_JSON,
            "expected_output": expected_mc
            },
        "test_load_from_dict": {"model_details": {"model_name": "test model", "documentation": "# Test Model Documentation"},"created_date": "05 April 2025"}
    }
)]
