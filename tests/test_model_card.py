"""
Unit tests for model_card.py
"""
# Standard Library Imports
from unittest.mock import (
    MagicMock,
    Mock,
    patch
)

# Third-party Imports
import IPython
import pandas as pd
import pytest

# Local Application Imports
from model_card_printer.model_card import ModelCard
from fixtures.model_card_data import (
    MockModelCard,
    test_ModelCard_internal_data
)

@pytest.mark.parametrize("test_model_card_dict", test_ModelCard_internal_data)
def test_ModelCard_internal(test_model_card_dict: dict) -> None:
    """
    Test Case 1: Successfully execute 'validate_visualization' method.
    """
    # Get test inputs
    test_plotly_visual, test_visual_name = test_model_card_dict["test_validate_visualization"]

    # Initalise an empty model card
    model_card = ModelCard()

    # Assert output is None
    assert model_card.validate_visualization(test_plotly_visual, test_visual_name) == None

    # Create Mock object to raise ValueError
    mock_object = Mock()

    # Assert ValueError occurred: visual object does not have 'to_html' method
    with pytest.raises(ValueError) as excinfo:

        model_card.validate_visualization(mock_object, test_visual_name)

    # Assert error message is correct
    assert f"Visualization object does not have 'to_html' attribute"

    # Store visual name inside model card to raise ValueError
    model_card._all_visual_names.append(test_visual_name)

    # Assert ValueError occurred: visual name already used
    with pytest.raises(ValueError) as excinfo:

        model_card.validate_visualization(test_plotly_visual, test_visual_name)

    # Assert error message is correct
    assert f"'{test_visual_name}' already in use" in str(excinfo)

    """
    Test Case 2: Successfully execute 'create_visualization' method.
    """
    # Get test inputs
    test_plotly_visual, test_visual_name = test_model_card_dict["test_create_visualization"]["test_input"]

    # Get expected output
    expected_output = test_model_card_dict["test_create_visualization"]["expected_output"]

    # Temporarily remove expected output's visualization HTML
    temp_html = str(expected_output.visualization_html)
    expected_output.visualization_html = None

    # Initalise an empty model card
    model_card = ModelCard()

    # Get actual output
    actual_output = model_card.create_visualization(test_plotly_visual, test_visual_name)

    # Assert expected and actual outputs are equal
    assert actual_output == expected_output

    # Restore HTML
    expected_output.visualization_html = temp_html

    """
    Test Case 3: Successfully execute 'create_dataset' method.
    """
    # Get test inputs
    mock_dataframe, mock_dataframe_name = test_model_card_dict["test_create_dataset"]["test_input"]

    # Get expected output
    expected_output = test_model_card_dict["test_create_dataset"]["expected_output"]

    # Initalise an empty model card
    model_card = ModelCard()

    # Get actual output
    actual_output = model_card.create_dataset(mock_dataframe, mock_dataframe_name)

    # Assert expected and actual outputs are equal
    assert actual_output == expected_output

    """
    Test Case 4: Successfully execute 'add_training_dataset' method.
    """
    # Get test inputs
    mock_dataframe, mock_dataframe2 = test_model_card_dict["test_add_training_dataset"]

    # Initalise an empty model card
    model_card = ModelCard()

    # Execute 'add_training_dataset'
    model_card.add_training_dataset(training_features = mock_dataframe,
                                    training_labels = mock_dataframe2)

    # Assert dataframes stored correctly
    lst_training_dataset = model_card.training_dataset_details.dataset_list
    for dataset in lst_training_dataset:
        if dataset.dataset_name == "Training Features":
            pd.testing.assert_frame_equal(dataset.dataset_object, mock_dataframe)
        elif dataset.dataset_name == "Training Labels":
            pd.testing.assert_frame_equal(dataset.dataset_object, mock_dataframe2)

    """
    Test Case 5: Successfully execute 'add_custom_documentation' method.
    """
    # Get test inputs
    test_documentation, test_document_name = test_model_card_dict["test_add_custom_documentation"]

    # Initalise an empty model card
    model_card = ModelCard()

    # Execute 'add_custom_documentation'
    model_card.add_custom_documentation(documentation = test_documentation,
                                        document_name = test_document_name)
    
    # Assert custom documentation stored correctly
    lst_custom_doc = model_card.custom_documentation
    for custom_doc in lst_custom_doc:
        assert custom_doc.document_name == test_document_name
        assert custom_doc.documentation == test_documentation

    """
    Test Case 6: Successfully execute 'add_individual_custom_visualization' method.
    """
    # Get test inputs
    test_plotly_visual, test_visual_name = test_model_card_dict["test_add_individual_custom_visualization"]

    # Initalise an empty model card
    model_card = ModelCard()

    # Execute 'add_individual_custom_visualization'
    model_card.add_individual_custom_visualization(visualization = test_plotly_visual,
                                                   visualization_name = test_visual_name)

    # Assert custom visualization stored correctly
    lst_indiv_custom_visuals = model_card.custom_visuals.individual_visualizations
    for custom_visual in lst_indiv_custom_visuals:
        assert custom_visual.visualization_object is test_plotly_visual
        assert custom_visual.visualization_name == test_visual_name

    """
    Test Case 7: Successfully execute 'add_custom_visualization_collection' method.
    """
    # Get test inputs
    test_visual_dict, test_collection_name, test_custom_documentation = test_model_card_dict["test_add_custom_visualization_collection"]["dict_test_custom_visuals"], test_model_card_dict["test_add_custom_visualization_collection"]["test_collection_name"], test_model_card_dict["test_add_custom_visualization_collection"]["test_custom_documentation"]

    # Initalise an empty model card
    model_card = ModelCard()

    # Execute 'add_custom_visualization_collection'
    model_card.add_custom_visualization_collection(dict_visualization_objects = test_visual_dict,
                                                   collection_name = test_collection_name,
                                                   documentation = test_custom_documentation)
    
    # Assert custom visualization collection stored correctly
    lst_visualization_collection = model_card.custom_visuals.visualization_collections
    for visualization_collection in lst_visualization_collection:

        # Assert collection name is correct
        assert visualization_collection.collection_name == test_collection_name

        # Assert documentation is correct
        assert visualization_collection.documentation == test_custom_documentation

        for visualization in visualization_collection.visualizations:
            
            # Assert visualization name stored correctly
            assert visualization.visualization_name in test_visual_dict.keys()

            # Assert visualization object stored correctly
            assert visualization.visualization_object == test_visual_dict[visualization.visualization_name]

    """
    Test Case 8: Successfully execute 'add_training_dataset_visualization' method.
    """
    # Get test inputs
    test_plotly_visual, test_visual_name = test_model_card_dict["test_add_training_dataset_visualization"]["test_input"]

    # Get expected output
    expected_output = test_model_card_dict["test_add_training_dataset_visualization"]["expected_output"]

    # Initalise an empty model card
    model_card = ModelCard()

    # Execute 'add_custom_visualization_collection'
    model_card.add_training_dataset_visualization(visualization = test_plotly_visual,
                                                  visualization_name = test_visual_name)

    # Assert visualization stored correctly
    lst_visuals = model_card.training_dataset_details.dataset_visualization_collection.visualizations
    for visual in lst_visuals:
        assert visual.visualization_name == test_visual_name
        assert visual.visualization_object is test_plotly_visual

    """
    Test Case 9: Successfully execute 'add_validation_dataset_visualization' method.
    """
    # Get test inputs
    test_plotly_visual, test_visual_name = test_model_card_dict["test_add_validation_dataset_visualization"]["test_input"]

    # Get expected output
    expected_output = test_model_card_dict["test_add_validation_dataset_visualization"]["expected_output"]

    # Initalise an empty model card
    model_card = ModelCard()

    # Execute 'add_custom_visualization_collection'
    model_card.add_validation_dataset_visualization(visualization = test_plotly_visual,
                                                    visualization_name = test_visual_name)

    # Assert visualization stored correctly
    lst_visuals = model_card.validation_dataset_details.dataset_visualization_collection.visualizations
    for visual in lst_visuals:
        assert visual.visualization_name == test_visual_name
        assert visual.visualization_object is test_plotly_visual

    """
    Test Case 10: Successfully execute 'show' method.
    """
    # Initalise an empty model card
    model_card = ModelCard()

    # Assert output type is correct
    assert isinstance(model_card.show(), IPython.core.display.HTML)

@patch("model_card_printer.model_card.open")
@patch("model_card_printer.model_card.add_custom_visualization_html")
@patch("model_card_printer.model_card.add_visualization_collection_html")
@patch("model_card_printer.model_card.add_textcontent_html")
@patch("model_card_printer.model_card.create_html_template")
def test_ModelCard_external(mock_create_html_template: MagicMock,
                            mock_add_textcontent_html: MagicMock,
                            mock_add_visualization_collection_html: MagicMock,
                            mock_add_custom_visualization_html: MagicMock,
                            mock_open: MagicMock) -> None:
    """
    Test Case 1: Successfully execute 'to_html' method (all content populated).
    """
    # Initalise mocked ModelCard object
    mock_model_card = MockModelCard()

    # Initialise empty model card and store attributes using attributes of mocked model card
    model_card = ModelCard(model_details = mock_model_card.model_details,
                           training_dataset_details = mock_model_card.training_dataset_details,
                           validation_dataset_details = mock_model_card.validation_dataset_details,
                           custom_visuals = mock_model_card.custom_visuals,
                           custom_documentation = mock_model_card.custom_documentation,
                           _all_visual_names = mock_model_card._all_visual_names)

    # Create 'prettify' class method for mock_custom_visualization_html object
    config = {"prettify.return_value": "test"}

    # Mock intermediate outputs
    mock_html_template_output = Mock()
    mock_textcontent_html_output = Mock()
    mock_visualization_collection_html_output = Mock()
    mock_custom_visualization_html_output = Mock(**config)
    mock_create_html_template.return_value = mock_html_template_output
    mock_add_textcontent_html.return_value = mock_textcontent_html_output
    mock_add_visualization_collection_html.return_value = mock_visualization_collection_html_output
    mock_add_custom_visualization_html.return_value = mock_custom_visualization_html_output

    # Get actual output
    is_dark_mode = True
    actual_output = model_card.to_html(is_dark_mode = is_dark_mode)

    # Assert output is string type
    assert isinstance(actual_output, str)

    # Assert mock objects called correctly (assert statements are called in sequence of 'to_html' execution)
    mock_create_html_template.assert_called_once_with(dark_mode = is_dark_mode)
    mock_add_textcontent_html.assert_any_call(SoupObject = mock_html_template_output,
                                              textcontent = model_card.model_details.documentation,
                                              div_id = f"{model_card.model_details.model_name} text")
    mock_add_visualization_collection_html.assert_any_call(SoupObject = mock_textcontent_html_output,
                                                           visualizationcollection = model_card.training_dataset_details.dataset_visualization_collection,
                                                           div_id = f"{model_card.training_dataset_details.dataset_visualization_collection.collection_name} visuals and text",
                                                           dark_mode = is_dark_mode)
    mock_add_visualization_collection_html.assert_any_call(SoupObject = mock_visualization_collection_html_output,
                                                           visualizationcollection = model_card.validation_dataset_details.dataset_visualization_collection,
                                                           div_id = f"{model_card.validation_dataset_details.dataset_visualization_collection.collection_name} visuals and text",
                                                           dark_mode = is_dark_mode)
    mock_add_textcontent_html.assert_any_call(SoupObject = mock_visualization_collection_html_output,
                                              textcontent = model_card.custom_documentation[0].documentation,
                                              div_id = f"{model_card.custom_documentation[0].document_name} text")
    mock_add_visualization_collection_html.assert_any_call(SoupObject = mock_textcontent_html_output,
                                                           visualizationcollection = model_card.custom_visuals.visualization_collections[0],
                                                           div_id = f"{model_card.custom_visuals.visualization_collections[0].collection_name} visuals and text",
                                                           dark_mode = is_dark_mode)
    mock_add_custom_visualization_html.assert_any_call(SoupObject = mock_visualization_collection_html_output,
                                                       visualization = model_card.custom_visuals.individual_visualizations[0],
                                                       div_id = f"{model_card.custom_visuals.individual_visualizations[0].visualization_name} visual",
                                                       dark_mode = is_dark_mode)
    mock_custom_visualization_html_output.prettify.assert_called_once()

    mock_add_textcontent_html.call_count == 2
    mock_add_visualization_collection_html.call_count == 3
    mock_add_custom_visualization_html.call_count == 1
    
    # Reset mock objects
    mock_create_html_template.reset_mock()
    mock_add_textcontent_html.reset_mock()
    mock_add_visualization_collection_html.reset_mock()
    mock_add_custom_visualization_html.reset_mock()
    mock_custom_visualization_html_output.reset_mock()

    """
    Test Case 2: Successfully execute 'to_html' method (visualcollection of training and validation datasets not available).
    """
    # Remove VisualizationCollection from training and validation dataset details
    model_card.training_dataset_details.dataset_visualization_collection.collection_name = None
    model_card.validation_dataset_details.dataset_visualization_collection.collection_name = None

    # Get actual output
    is_dark_mode = True
    actual_output = model_card.to_html(is_dark_mode = is_dark_mode)

    # Assert output is string type
    assert isinstance(actual_output, str)

    # Assert mock objects called correctly (assert statements are called in sequence of 'to_html' execution)
    mock_create_html_template.assert_called_once_with(dark_mode = is_dark_mode)
    mock_add_textcontent_html.assert_any_call(SoupObject = mock_html_template_output,
                                              textcontent = model_card.model_details.documentation,
                                              div_id = f"{model_card.model_details.model_name} text")
    mock_add_textcontent_html.assert_any_call(SoupObject = mock_textcontent_html_output,
                                              textcontent = model_card.training_dataset_details.documentation,
                                              div_id = f"training dataset text")
    mock_add_textcontent_html.assert_any_call(SoupObject = mock_textcontent_html_output,
                                              textcontent = model_card.validation_dataset_details.documentation,
                                              div_id = f"validation dataset text")
    mock_add_textcontent_html.assert_any_call(SoupObject = mock_textcontent_html_output,
                                              textcontent = model_card.custom_documentation[0].documentation,
                                              div_id = f"{model_card.custom_documentation[0].document_name} text")
    mock_add_visualization_collection_html.assert_any_call(SoupObject = mock_textcontent_html_output,
                                                           visualizationcollection = model_card.custom_visuals.visualization_collections[0],
                                                           div_id = f"{model_card.custom_visuals.visualization_collections[0].collection_name} visuals and text",
                                                           dark_mode = is_dark_mode)
    mock_add_custom_visualization_html.assert_any_call(SoupObject = mock_visualization_collection_html_output,
                                                       visualization = model_card.custom_visuals.individual_visualizations[0],
                                                       div_id = f"{model_card.custom_visuals.individual_visualizations[0].visualization_name} visual",
                                                       dark_mode = is_dark_mode)
    mock_custom_visualization_html_output.prettify.assert_called_once()

    mock_add_textcontent_html.call_count == 4
    mock_add_visualization_collection_html.call_count == 1
    mock_add_custom_visualization_html.call_count == 1

    """
    Test Case 3: Successfully execute 'write_html' method.
    """
    # Initialise empty model card and store attributes using attributes of mocked model card
    model_card = ModelCard()

    # Mock 'write' method of 'open'
    mock_write = Mock(**{"write.return_value": None})
    mock_open.return_value.__enter__.return_value = mock_write

    # Execute 'write_html' method
    test_path = "test_path"
    is_dark_mode = True
    model_card.write_html(file_path = test_path, is_dark_mode = is_dark_mode)

    # Assert mock objects called correctly
    mock_open.assert_called_once_with(test_path, "w")
    mock_write.write.assert_called_once_with(model_card.to_html(is_dark_mode = is_dark_mode))

    # Reset mock objects
    mock_open.reset_mock()
    mock_write.reset_mock()

    """
    Test Case 4: Successfully execute 'write_json' method.
    """
    # Initialise empty model card and store attributes using attributes of mocked model card
    model_card = ModelCard()

    # Execute 'write_json' method
    model_card.write_json(test_path)

    # Assert mock objects called correctly
    mock_open.assert_called_once_with(test_path, "w")
    mock_write.write.assert_called_once_with(model_card.to_json())
