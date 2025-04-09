"""
Fixtures used to unit test model_card.py
"""
# Standard Library Imports
import dataclasses

# Third-party Imports
import plotly.graph_objects as go
from sklearn.ensemble import GradientBoostingClassifier

# Local Library Imports
from fixtures.model_card_components_data import (
    mock_dataframe,
    mock_Dataset
)
from model_card_printer.model_card_components import (
    DatasetMetadata,
    CustomDetails,
    CustomVisuals,
    ModelDetails,
    Visualization,
    VisualizationCollection,
)
from model_card_printer.model_card import ModelCard

# Create mock model details
mock_model_details = ModelDetails(model_name = "test model",
                                  model_path = "test_model_path",
                                  model_object = GradientBoostingClassifier(),
                                  documentation = "test model documentation")

# Create mock custom details
mock_custom_details = CustomDetails(document_name = "test custom document",
                                    documentation = "test custom documentation")

# Create mock visualization object
mock_plotly_visual1 = go.Figure()
mock_plotly_visual2 = go.Figure()
mock_plotly_visual3 = go.Figure()
mock_plotly_visual4 = go.Figure()
mock_plotly_custom_visual1 = go.Figure()
mock_plotly_custom_visual2 = go.Figure()
mock_plotly_visual1_html = mock_plotly_visual1.to_html(config={'staticPlot': True},
                                                     include_plotlyjs = True,
                                                     include_mathjax = False,
                                                     full_html = False,
                                                     div_id = "test visual1")
mock_plotly_visual2_html = mock_plotly_visual2.to_html(config={'staticPlot': True},
                                                       include_plotlyjs = True,
                                                       include_mathjax = False,
                                                       full_html = False,
                                                       div_id = "test visual2")
mock_plotly_visual3_html = mock_plotly_visual3.to_html(config={'staticPlot': True},
                                                     include_plotlyjs = True,
                                                     include_mathjax = False,
                                                     full_html = False,
                                                     div_id = "test visual1")
mock_plotly_visual4_html = mock_plotly_visual4.to_html(config={'staticPlot': True},
                                                       include_plotlyjs = True,
                                                       include_mathjax = False,
                                                       full_html = False,
                                                       div_id = "test visual2")
mock_plotly_custom_visual1_html = mock_plotly_custom_visual1.to_html(config={'staticPlot': True},
                                                                     include_plotlyjs = True,
                                                                     include_mathjax = False,
                                                                     full_html = False,
                                                                     div_id = "test custom visual1")
mock_plotly_custom_visual2_html = mock_plotly_custom_visual2.to_html(config={'staticPlot': True},
                                                                     include_plotlyjs = True,
                                                                     include_mathjax = False,
                                                                     full_html = False,
                                                                     div_id = "test custom visual2")

# Create mock Visualization objects
mock_visualization1 = Visualization(visualization_name = "test visual1",
                                    visualization_type = type(go.Figure()),
                                    visualization_object = mock_plotly_visual1,
                                    visualization_html = mock_plotly_visual1_html)

mock_visualization2 = Visualization(visualization_name = "test visual2",
                                    visualization_type = type(go.Figure()),
                                    visualization_object = mock_plotly_visual2,
                                    visualization_html = mock_plotly_visual2_html)

mock_visualization3 = Visualization(visualization_name = "test visual3",
                                    visualization_type = type(go.Figure()),
                                    visualization_object = mock_plotly_visual1,
                                    visualization_html = mock_plotly_visual1_html)

mock_visualization4 = Visualization(visualization_name = "test visual4",
                                    visualization_type = type(go.Figure()),
                                    visualization_object = mock_plotly_visual2,
                                    visualization_html = mock_plotly_visual2_html)

mock_custom_visualization1 = Visualization(visualization_name = "test custom visual1",
                                           visualization_type = type(go.Figure()),
                                           visualization_object = mock_plotly_custom_visual1,
                                           visualization_html = mock_plotly_custom_visual1_html)

mock_custom_visualization2 = Visualization(visualization_name = "test custom visual2",
                                           visualization_type = type(go.Figure()),
                                           visualization_object = mock_plotly_custom_visual2,
                                           visualization_html = mock_plotly_custom_visual2_html)

# Create mock VisualizationCollection objects
mock_visualization_collection = VisualizationCollection(collection_name = "test visual collection",
                                                        visualizations = [mock_visualization1, mock_visualization2],
                                                        documentation = "test visual collection documentation")

mock_custom_visualization_collection = VisualizationCollection(collection_name = "test custom visual collection",
                                                               visualizations = [mock_custom_visualization2],
                                                               documentation = "test custom visual collection documentation")

# Create mock training dataset details
mock_training_dataset_details = DatasetMetadata(dataset_list = [mock_Dataset, mock_Dataset],
                                                documentation = "test training dataset details",
                                                dataset_visualization_collection = mock_visualization_collection)

# Create mock validation dataset details
mock_validation_dataset_details = DatasetMetadata(dataset_list = [mock_Dataset, mock_Dataset],
                                                  documentation = "test validation dataset details",
                                                  dataset_visualization_collection = mock_visualization_collection)

# Create mock CustomVisuals object
mock_custom_visuals = CustomVisuals(individual_visualizations = [mock_custom_visualization1],
                                    visualization_collections = [mock_custom_visualization_collection])

# Create mock ModelCard class
@dataclasses.dataclass
class MockModelCard(ModelCard):

    def __init__(self):
        """
        Initialise mock model card with the mocked attributes.
        """
        self.model_details = mock_model_details
        self.training_dataset_details = mock_training_dataset_details
        self.validation_dataset_details = mock_validation_dataset_details
        self.custom_visuals = mock_custom_visuals
        self.custom_documentation = [mock_custom_details, mock_custom_details]
        self.created_date = None
        self._all_visual_names = ["test visual1", "test visual2", "test visual3", "test visual4", "test custom visual1", "test custom visual2"]

test_ModelCard_internal_data = [(
    {
        "test_validate_visualization": [mock_plotly_visual1, "test visual1"],
        "test_create_visualization": {
            "test_input": [mock_plotly_visual1, "test visual1"],
            "expected_output": mock_visualization1
            },
        "test_create_dataset": {
            "test_input": [mock_dataframe, mock_Dataset.dataset_name],
            "expected_output": mock_Dataset
            },
        "test_add_training_dataset": [mock_dataframe, mock_dataframe],
        "test_add_custom_documentation": ["test custom documentation", "test custom document name"],
        "test_add_individual_custom_visualization": [mock_plotly_visual1, "test visual1"],
        "test_add_custom_visualization_collection": {
            "dict_test_custom_visuals": {
                "test custom visual1": mock_plotly_custom_visual1,
                "test custom visual2": mock_plotly_custom_visual2
                },
            "test_collection_name": "test custom collection",
            "test_custom_documentation": "test custom documentation"
            },
        "test_add_training_dataset_visualization": {
            "test_input": [mock_plotly_visual1, "test visual1"],
            "expected_output": [mock_visualization1]
            },
        "test_add_validation_dataset_visualization": {
            "test_input": [mock_plotly_visual1, "test visual1"],
            "expected_output": [mock_visualization1]
            }
    }
)]