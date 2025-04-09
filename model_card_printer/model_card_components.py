"""
This file contains data classes used to create model cards
for trained models, datasets and data visualisations.
"""
# Standard Library Imports
import abc
import dataclasses
import json
from typing import (
    Any,
    Dict,
    List,
    TypeVar,
    Optional
)

# Define subclass type of ModelCardBaseField
T = TypeVar("T", bound = "ModelCardBaseField")

class ModelCardBaseField(abc.ABC):
    """
    Model card base field where all the model card fields inherit.
    """
    def _get_type(self, obj: Any) -> type:
        """
        Gets the type of specified object.
        """
        return type(obj)
    
    def to_dict(self) -> dict:
        """
        Converts class object to dictionary object.
        """
        # Create function to exclude model/visualization/dataframe objects and None properties
        exclude_object = lambda attributes: {key: val for key, val in attributes if "_object" not in key and "_type" not in key and val}

        return dataclasses.asdict(self, dict_factory = exclude_object)

    def to_json(self) -> str:
        """
        Converts class object to JSON.
        """
        return json.dumps(self.to_dict(), indent = 4)

    def _from_json(self, modelcardfield: T, dict_json: Dict[str, Any]) -> T:
        """
        Parses a JSON dictionary into specified model card field object.

        Parameters:
        - self
        - modelcardfield (T): Model card field object.
        - dict_json (Dict[str, Any]): Dictionary containing subfield names and their values.

        Returns:
        - T: Model card field object with populated.
        """
        for json_subfield_name, json_subfield_value in dict_json.items():
            
            # Check if attribute exists modelcardfield object
            if not hasattr(modelcardfield, json_subfield_name):
                raise ValueError(f"{modelcardfield} does not have '{json_subfield_name}' field.")
            
            # check if subfield value is a dictionary (i.e nested subfield)
            if isinstance(json_subfield_value, dict):
                subfield_value = self._from_json(getattr(modelcardfield, json_subfield_name), json_subfield_value)

            # Check if list items are dictionary objects (i.e each element is a subfield)
            elif isinstance(json_subfield_value, list):
                
                subfield_value = []
                for val in json_subfield_value:
                    if isinstance(val, dict):
                        # Create instance of subfield
                        _subfield = modelcardfield.__annotations__[json_subfield_name].__args__[0]()
                        subfield_value.append(self._from_json(_subfield, val))
                    else:
                        subfield_value.append(val)
            else:
                subfield_value = json_subfield_value

            # Store subfield value into modelcardfield object
            setattr(modelcardfield, json_subfield_name, subfield_value)

        return modelcardfield

@dataclasses.dataclass
class Visualization(ModelCardBaseField):
    """
    This class provides information on a visualization relevant to the model.

    Attributes:
    - visualization_name: Name of the visualization.
    - visualization_type: Type of visualization (common types include Pandas and Plotly plots).
    - visualization_object: Visualization object.
    """
    visualization_name: Optional[str] = None
    visualization_type: Optional[type] = None
    visualization_object: Optional[Any] = None
    visualization_html: Optional[str] = None
    is_dark_mode: Optional[str] = None

@dataclasses.dataclass
class VisualizationCollection(ModelCardBaseField):
    """
    This class contains a collection of visualizations for the model card.

    Attributes:
    - collection_name: Name of collection to which the visualizations belong to.
    - visualizations: List of Visualization objects.
    """
    collection_name: Optional[str] = None
    visualizations: List[Visualization] = dataclasses.field(default_factory = list)
    documentation: Optional[str] = None

@dataclasses.dataclass
class Dataset(ModelCardBaseField):
    """
    This class provides documentation and metadata on a dataset.

    Attributes:
    - dataset_name: Name of dataset.
    - dataset_path: Path where training dataset is stored.
    - dataset_object: Dataset object.
    """
    dataset_name: Optional[str] = None
    dataset_path: Optional[str] = None
    dataset_object: Optional[Any] = None

@dataclasses.dataclass
class DatasetMetadata(ModelCardBaseField):
    """
    This class provides documentation and metadata on the training dataset.

    Attributes:
    - dataset_list: List of Dataset objects.
    - documentation: All content related to the dataset - this is a free text field in markdown format.
    - dataset_visualization_collection: VisualizationCollection containing visuals related to dataset.
    """
    dataset_list: List[Dataset] = dataclasses.field(default_factory = list)
    documentation: Optional[str] = None
    dataset_visualization_collection: VisualizationCollection = dataclasses.field(default_factory = VisualizationCollection)

@dataclasses.dataclass
class ModelDetails(ModelCardBaseField):
    """
    This class provides documentation on the model.

    Attributes:
    - model_name: Name of the model.
    - model_path: Path where model is stored.
    - documentation: All content related to the model - this is a free text field in markdown format.
    - model_object: Trained model object.
    """
    model_name: Optional[str] = None
    model_path: Optional[str] = None
    model_object: Optional[Any] = None
    documentation: Optional[str] = None

@dataclasses.dataclass
class CustomDetails(ModelCardBaseField):
    """
    This class contains custom documentation.

    Attributes:
    - documentation: Any documentation - this is a free text field in markdown format.
    """
    document_name: Optional[str] = None
    documentation: Optional[str] = None

@dataclasses.dataclass
class CustomVisuals(ModelCardBaseField):
    """
    This class contains custom visualizations and custom visualization collections.

    Visualization collections will be displayed together, assuming they are related to one another.

    Attributes:
    - individual_visualizations: List of individual visualizations.
    - visualization_collections: List of visualization collections.
    """
    individual_visualizations: List[Visualization] = dataclasses.field(default_factory = list)
    visualization_collections: List[VisualizationCollection] = dataclasses.field(default_factory = list)
