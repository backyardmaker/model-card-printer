"""
Fixtures used to unit test model_card_components.py
"""
# Standard Library Imports
import dataclasses
from typing import (
    List
)

# Third-party Imports
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import GradientBoostingClassifier

# Local Library Imports
from model_card_printer.model_card_components import (
    Dataset,
    ModelCardBaseField,
    Visualization,
    VisualizationCollection,
)

# Create mock dataframe
mock_dataframe = pd.DataFrame(data = {"test": [1,2,3]})

# Create mock DataBaseField class
@dataclasses.dataclass
class MockDataBaseField(ModelCardBaseField):
    data_name: str = dataclasses.field(default = "test data basefield")

# Create mock ModelCardBaseField class
@dataclasses.dataclass
class MockModelCardBaseField(ModelCardBaseField):
    mock_attribute_1: str = dataclasses.field(default = "test1")
    mock_attribute_2: str = dataclasses.field(default = "test2")
    mock_attribute_3: List[str] = dataclasses.field(default_factory = list)
    mock_attribute_4: MockDataBaseField = dataclasses.field(default_factory = MockDataBaseField)
    mock_attribute_5: List[MockDataBaseField] = dataclasses.field(default_factory = list)

# Create mock Visualization object
mock_Visualization = Visualization(visualization_name = "test visual",
                                   visualization_type = type(go.Figure()),
                                   visualization_object = go.Figure(),
                                   visualization_html = "test")

# Create mock VisualizationCollection object
mock_VisualizationCollection = VisualizationCollection(collection_name = "test collection",
                                                       visualizations = [mock_Visualization],
                                                       documentation = "test collection documentation")

# Create mock Dataset object
mock_Dataset = Dataset(dataset_name = "test dataset",
                       dataset_path = None,
                       dataset_object = mock_dataframe)

test_ModelCardBaseField_data = [(
    MockModelCardBaseField(mock_attribute_3 = ["test3", "test4"], mock_attribute_5=[MockDataBaseField()]),
    {'mock_attribute_1': 'test1', 'mock_attribute_2': 'test2', 'mock_attribute_3': ["test3", "test4"], 'mock_attribute_4': {"data_name": "test data basefield"}, 'mock_attribute_5': [{'data_name': 'test data basefield'}]},
    {
        "expected_output_to_dict": {
            'mock_attribute_1': 'test1',
            'mock_attribute_2': 'test2',
            'mock_attribute_3': ['test3', 'test4'],
            'mock_attribute_4': {"data_name": "test data basefield"},
            'mock_attribute_5': [{'data_name': 'test data basefield'}]
            },
        "expected_output_to_json": '{\n    "mock_attribute_1": "test1",\n    "mock_attribute_2": "test2",\n    "mock_attribute_3": [\n        "test3",\n        "test4"\n    ],\n    "mock_attribute_4": {\n        "data_name": "test data basefield"\n    },\n    "mock_attribute_5": [\n        {\n            "data_name": "test data basefield"\n        }\n    ]\n}',
        "expected_output_from_json": MockModelCardBaseField(mock_attribute_3 = ["test3", "test4"], mock_attribute_5=[MockDataBaseField()]),
        "expected_output_get_type": type("test")
    }
)]

test_Visualization_data = [(
    {
        "test_default_visualization_name": None,
        "test_default_visualization_type": None,
        "test_default_visualization_object": None,
        "test_default_visualization_html": None,
        "test_default_visualization_is_dark_mode": None
    },
    {
        "expected_visualization_name": "test",
        "expected_visualization_type": type(go.Figure()),
        "expected_visualization_object": go.Figure(),
        "expected_visualization_html": "test",
        "expected_visualization_is_dark_mode": "True"
    }
)]

test_VisualizationCollection_data = [(
    {
        "test_default_collection_name": None,
        "test_default_visualizations": [],
        "test_default_documentation": None
    },
    {
        "expected_collection_name": "test",
        "expected_visualizations": [mock_Visualization],
        "expected_documentation": "test"
    }
)]

test_Dataset_data = [(
    {
        "test_default_dataset_name": None,
        "test_default_dataset_path": None,
        "test_default_dataset_object": None
    },
    {
        "expected_dataset_name": "test",
        "expected_dataset_path": "test_default_path",
        "expected_dataset_object": mock_dataframe
    }
)]

test_DatasetMetadata_data = [(
    {
        "test_default_dataset_list": [],
        "test_default_documentation": None,
        "test_default_dataset_visualization_collection": VisualizationCollection()
    },
    {
        "expected_dataset_list": [mock_Dataset],
        "expected_documentation": "test dataset documentation",
        "expected_dataset_visualization_collection": mock_VisualizationCollection
    }
)]

test_ModelDetails_data = [(
    {
        "test_default_model_name": None,
        "test_default_model_path": None,
        "test_default_model_object": None,
        "test_default_documentation": None
    },
    {
        "expected_model_name": "test model name",
        "expected_model_path": "test_model_path",
        "expected_model_object": GradientBoostingClassifier(),
        "expected_documentation": "test model details documentation"
    }
)]

test_CustomDetails_data = [(
    {
        "test_default_document_name": None,
        "test_default_documentation": None
    },
    {
        "expected_document_name": "test custom document name",
        "expected_documentation": "test custom documentation"
    }
)]

test_CustomVisuals_data = [(
    {
        "test_default_individual_visualizations": [],
        "test_default_visualization_collections": []
    },
    {
        "expected_individual_visualizations": [mock_Visualization],
        "expected_visualization_collections": [mock_VisualizationCollection]
    }
)]