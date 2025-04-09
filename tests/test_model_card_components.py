"""
Unit tests for model_card_components.py
"""
# Standard Library Imports
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Third-party Imports
import pandas as pd
import pytest

# Local Application Imports
from fixtures.model_card_components_data import (
    test_CustomDetails_data,
    test_CustomVisuals_data,
    test_Dataset_data,
    test_DatasetMetadata_data,
    test_ModelCardBaseField_data,
    test_ModelDetails_data,
    test_Visualization_data,
    test_VisualizationCollection_data,
)
from model_card_printer.model_card_components import (
    CustomDetails,
    CustomVisuals,
    Dataset,
    DatasetMetadata,
    ModelCardBaseField,
    ModelDetails,
    Visualization,
    VisualizationCollection
)

@pytest.mark.parametrize("mock_base_field, mock_base_field_dict, expected_output_dict", test_ModelCardBaseField_data)
def test_ModelCardBaseField(mock_base_field: ModelCardBaseField, mock_base_field_dict: dict, expected_output_dict: dict) -> None:
    """
    Test Case 1: Successfully return all methods' outputs.
    """
    # Get expected outputs for each method
    expected_output_to_dict = expected_output_dict["expected_output_to_dict"]
    expected_output_to_json = expected_output_dict["expected_output_to_json"]
    expected_output_from_json = expected_output_dict["expected_output_from_json"]
    expected_output_get_type = expected_output_dict["expected_output_get_type"]

    # Get actual output for 'to_dict' method
    actual_output_to_dict = ModelCardBaseField.to_dict(mock_base_field)

    # Get actual output for 'to_json' method
    actual_output_to_json = ModelCardBaseField.to_json(mock_base_field)

    # Get actual output for '_from_json' method
    actual_output_from_json = mock_base_field._from_json(mock_base_field, mock_base_field_dict)

    # Get actual output for '_get_type' method
    actual_output_get_type = ModelCardBaseField()._get_type("test")

    # Assert actual and expected outputs are equal
    assert actual_output_to_dict == expected_output_to_dict
    assert actual_output_to_json == expected_output_to_json
    assert actual_output_from_json == expected_output_from_json
    assert actual_output_get_type == expected_output_get_type

    """
    Test Case 2: Successfully raise ValueError due to no subfield name.
    """
    # Create invalid basefield dictionary
    invalid_base_field_dict = {"invalid_attribute": "test"}

    # Assert ValueError occurred
    with pytest.raises(ValueError) as excinfo:
        _ = mock_base_field._from_json(mock_base_field, invalid_base_field_dict)
    
    # Assert error message is correct
    assert f"{mock_base_field} does not have 'invalid_attribute' field"

@pytest.mark.parametrize("expected_default_dict, expected_values_dict", test_Visualization_data)
def test_Visualization(expected_default_dict: dict, expected_values_dict: dict) -> None:
    """
    Test Case 1: Successfully return all attributes' default values.
    """
    # Get expected default values
    expected_default_name = expected_default_dict["test_default_visualization_name"]
    expected_default_type = expected_default_dict["test_default_visualization_type"]
    expected_default_object = expected_default_dict["test_default_visualization_object"]
    expected_default_html = expected_default_dict["test_default_visualization_html"]
    expected_default_is_dark_mode = expected_default_dict["test_default_visualization_is_dark_mode"]

    # Get actual default values
    actual_visualization = Visualization()
    actual_default_name = actual_visualization.visualization_name
    actual_default_type = actual_visualization.visualization_type
    actual_default_object = actual_visualization.visualization_object
    actual_default_html = actual_visualization.visualization_html
    actual_default_is_dark_mode = actual_visualization.is_dark_mode

    # Assert actual and expected default values are equal
    assert expected_default_name == actual_default_name
    assert expected_default_type == actual_default_type
    assert expected_default_object == actual_default_object
    assert expected_default_html == actual_default_html
    assert expected_default_is_dark_mode == actual_default_is_dark_mode

    """
    Test Case 2: Successfully return all attributes' expected values.
    """
    # Get expected values
    expected_name = expected_values_dict["expected_visualization_name"]
    expected_type = expected_values_dict["expected_visualization_type"]
    expected_object = expected_values_dict["expected_visualization_object"]
    expected_html = expected_values_dict["expected_visualization_html"]
    expected_is_dark_mode = expected_values_dict["expected_visualization_is_dark_mode"]

    # Initialise Visualization object
    actual_visualization = Visualization()

    # Store expected values
    actual_visualization.visualization_name = expected_name
    actual_visualization.visualization_type = expected_type
    actual_visualization.visualization_object = expected_object
    actual_visualization.visualization_html = expected_html
    actual_visualization.is_dark_mode = expected_is_dark_mode

    # Assert actual and expected values are equal
    assert actual_visualization.visualization_name == expected_name
    assert actual_visualization.visualization_type == expected_type
    assert actual_visualization.visualization_object == expected_object
    assert actual_visualization.visualization_html == expected_html
    assert actual_visualization.is_dark_mode == expected_is_dark_mode

@pytest.mark.parametrize("expected_default_dict, expected_values_dict", test_VisualizationCollection_data)
def test_VisualizationCollection(expected_default_dict: dict, expected_values_dict: dict) -> None:
    """
    Test Case 1: Successfully return all attributes' default values.
    """
    # Get expected default values
    expected_default_collection_name = expected_default_dict["test_default_collection_name"]
    expected_default_visualizations = expected_default_dict["test_default_visualizations"]
    expected_default_documentation = expected_default_dict["test_default_documentation"]

    # Get actual default values
    actual_visualization_collection = VisualizationCollection()
    actual_default_collection_name = actual_visualization_collection.collection_name
    actual_default_visualizations = actual_visualization_collection.visualizations
    actual_default_documentation = actual_visualization_collection.documentation

    # Assert actual and expected default values are equal
    assert expected_default_collection_name == actual_default_collection_name
    assert expected_default_visualizations == actual_default_visualizations
    assert expected_default_documentation == actual_default_documentation

    """
    Test Case 2: Successfully return all attributes' expected values.
    """
    # Get expected values
    expected_collection_name = expected_values_dict["expected_collection_name"]
    expected_visualizations = expected_values_dict["expected_visualizations"]
    expected_documentation = expected_values_dict["expected_documentation"]

    # Initialise VisualizationCollection object
    actual_visualization_collection = VisualizationCollection()

    # Store expected values
    actual_visualization_collection.collection_name = expected_collection_name
    actual_visualization_collection.visualizations = expected_visualizations
    actual_visualization_collection.documentation = expected_documentation

    # Assert actual and expected values are equal
    assert actual_visualization_collection.collection_name == expected_collection_name
    assert actual_visualization_collection.visualizations == expected_visualizations
    assert actual_visualization_collection.documentation == expected_documentation

@pytest.mark.parametrize("expected_default_dict, expected_values_dict", test_Dataset_data)
def test_Dataset(expected_default_dict: dict, expected_values_dict: dict) -> None:
    """
    Test Case 1: Successfully return all attributes' default values.
    """
    # Get expected default values
    expected_default_dataset_name = expected_default_dict["test_default_dataset_name"]
    expected_default_dataset_path = expected_default_dict["test_default_dataset_path"]
    expected_default_dataset_object = expected_default_dict["test_default_dataset_object"]

    # Get actual default values
    actual_dataset = Dataset()
    actual_default_dataset_name = actual_dataset.dataset_name
    actual_default_dataset_path = actual_dataset.dataset_path
    actual_default_dataset_object = actual_dataset.dataset_object

    # Assert actual and expected default values are equal
    assert expected_default_dataset_name == actual_default_dataset_name
    assert expected_default_dataset_path == actual_default_dataset_path
    assert actual_default_dataset_object == expected_default_dataset_object

    """
    Test Case 2: Successfully return all attributes' expected values.
    """
    # Get expected values
    expected_dataset_name = expected_values_dict["expected_dataset_name"]
    expected_dataset_path = expected_values_dict["expected_dataset_path"]
    expected_dataset_object = expected_values_dict["expected_dataset_object"]

    # Initialise Dataset object
    actual_dataset = Dataset()

    # Store expected values
    actual_dataset.dataset_name = expected_dataset_name
    actual_dataset.dataset_path = expected_dataset_path
    actual_dataset.dataset_object= expected_dataset_object

    # Assert actual and expected values are equal
    assert actual_dataset.dataset_name == expected_dataset_name
    assert actual_dataset.dataset_path == expected_dataset_path
    pd.testing.assert_frame_equal(actual_dataset.dataset_object, expected_dataset_object)

@pytest.mark.parametrize("expected_default_dict, expected_values_dict", test_DatasetMetadata_data)
def test_DatasetMetadata(expected_default_dict: dict, expected_values_dict: dict) -> None:
    """
    Test Case 1: Successfully return all attributes' default values.
    """
    # Get expected default values
    expected_default_dataset_list = expected_default_dict["test_default_dataset_list"]
    expected_default_documentation = expected_default_dict["test_default_documentation"]
    expected_default_dataset_visualization_collection = expected_default_dict["test_default_dataset_visualization_collection"]

    # Get actual default values
    actual_dataset_metadata = DatasetMetadata()
    actual_default_dataset_list = actual_dataset_metadata.dataset_list
    actual_default_documentation = actual_dataset_metadata.documentation
    actual_default_dataset_visualization_collection = actual_dataset_metadata.dataset_visualization_collection

    # Assert actual and expected default values are equal
    assert actual_default_dataset_list == expected_default_dataset_list
    assert actual_default_documentation == expected_default_documentation
    assert actual_default_dataset_visualization_collection == expected_default_dataset_visualization_collection

    """
    Test Case 2: Successfully return all attributes' expected values.
    """
    # Get expected values
    expected_dataset_list = expected_values_dict["expected_dataset_list"]
    expected_documentation = expected_values_dict["expected_documentation"]
    expected_dataset_visualization_collection = expected_values_dict["expected_dataset_visualization_collection"]

    # Initialise DatasetMetadata object
    actual_dataset = DatasetMetadata()

    # Store expected values
    actual_dataset.dataset_name = expected_dataset_list
    actual_dataset.dataset_path = expected_documentation
    actual_dataset.dataset_object= expected_dataset_visualization_collection

    # Assert actual and expected values are equal
    assert actual_dataset.dataset_name == expected_dataset_list
    assert actual_dataset.dataset_path == expected_documentation
    assert actual_dataset.dataset_object == expected_dataset_visualization_collection

@pytest.mark.parametrize("expected_default_dict, expected_values_dict", test_ModelDetails_data)
def test_ModelDetails(expected_default_dict: dict, expected_values_dict: dict) -> None:
    """
    Test Case 1: Successfully return all attributes' default values.
    """
    # Get expected default values
    expected_default_model_name = expected_default_dict["test_default_model_name"]
    expected_default_model_path = expected_default_dict["test_default_model_path"]
    expected_default_model_object = expected_default_dict["test_default_model_object"]
    expected_default_documentation = expected_default_dict["test_default_documentation"]

    # Get actual default values
    actual_model_details = ModelDetails()
    actual_default_model_name = actual_model_details.model_name
    actual_default_model_path = actual_model_details.model_path
    actual_default_model_object = actual_model_details.model_object
    actual_default_documentation = actual_model_details.documentation

    # Assert actual and expected default values are equal
    assert actual_default_model_name == expected_default_model_name
    assert actual_default_model_path == expected_default_model_path
    assert actual_default_model_object == expected_default_model_object
    assert actual_default_documentation == expected_default_documentation

    """
    Test Case 2: Successfully return all attributes' expected values.
    """
    # Get expected values
    expected_model_name = expected_values_dict["expected_model_name"]
    expected_model_path = expected_values_dict["expected_model_path"]
    expected_model_object = expected_values_dict["expected_model_object"]
    expected_documentation = expected_values_dict["expected_documentation"]

    # Initialise ModelDetails object
    actual_model_details = ModelDetails()

    # Store expected values
    actual_model_details.model_name = expected_model_name
    actual_model_details.model_path = expected_model_path
    actual_model_details.model_object = expected_model_object
    actual_model_details.documentation = expected_documentation

    # Assert actual and expected values are equal
    assert actual_model_details.model_name == expected_model_name
    assert actual_model_details.model_path == expected_model_path
    assert actual_model_details.model_object == expected_model_object
    assert actual_model_details.documentation == expected_documentation

@pytest.mark.parametrize("expected_default_dict, expected_values_dict", test_CustomDetails_data)
def test_CustomDetails(expected_default_dict: dict, expected_values_dict: dict) -> None:
    """
    Test Case 1: Successfully return all attributes' default values.
    """
    # Get expected default values
    expected_default_document_name = expected_default_dict["test_default_document_name"]
    expected_default_documentation = expected_default_dict["test_default_documentation"]

    # Get actual default values
    actual_custom_details = CustomDetails()
    actual_default_document_name = actual_custom_details.document_name
    actual_default_documentation = actual_custom_details.documentation

    # Assert actual and expected default values are equal
    assert actual_default_document_name == expected_default_document_name
    assert actual_default_documentation == expected_default_documentation

    """
    Test Case 2: Successfully return all attributes' expected values.
    """
    # Get expected values
    expected_document_name = expected_values_dict["expected_document_name"]
    expected_documentation = expected_values_dict["expected_documentation"]

    # Initialise ModelDetails object
    actual_custom_details = CustomDetails()

    # Store expected values
    actual_custom_details.document_name = expected_document_name
    actual_custom_details.documentation = expected_documentation

    # Assert actual and expected values are equal
    assert actual_custom_details.document_name == expected_document_name
    assert actual_custom_details.documentation == expected_documentation

@pytest.mark.parametrize("expected_default_dict, expected_values_dict", test_CustomVisuals_data)
def test_CustomVisuals(expected_default_dict: dict, expected_values_dict: dict) -> None:
    """
    Test Case 1: Successfully return all attributes' default values.
    """
    # Get expected default values
    expected_default_individual_visualizations = expected_default_dict["test_default_individual_visualizations"]
    expected_default_visualization_collections = expected_default_dict["test_default_visualization_collections"]

    # Get actual default values
    actual_custom_visuals = CustomVisuals()
    actual_default_individual_visualizations = actual_custom_visuals.individual_visualizations
    actual_default_visualization_collections = actual_custom_visuals.visualization_collections

    # Assert actual and expected default values are equal
    assert actual_default_individual_visualizations == expected_default_individual_visualizations
    assert actual_default_visualization_collections == expected_default_visualization_collections

    """
    Test Case 2: Successfully return all attributes' expected values.
    """
    # Get expected values
    expected_individual_visualizations = expected_values_dict["expected_individual_visualizations"]
    expected_visualization_collections = expected_values_dict["expected_visualization_collections"]

    # Initialise ModelDetails object
    actual_custom_visuals = CustomVisuals()

    # Store expected values
    actual_custom_visuals.individual_visualizations = expected_individual_visualizations
    actual_custom_visuals.visualization_collections = expected_visualization_collections

    # Assert actual and expected values are equal
    assert actual_custom_visuals.individual_visualizations == expected_individual_visualizations
    assert actual_custom_visuals.visualization_collections == expected_visualization_collections
