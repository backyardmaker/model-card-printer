"""
This file contains the ModelCard data class that is use to construct the model card.

It can be represented in the following formats:
    1) HTML
    2) JSON
    3) Python dictionary
"""
# Standard Library Imports
import dataclasses
from typing import (
    Any,
    Dict,
    List,
    Optional
)

# Third-party Imports
import IPython

# Local Application Imports
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
from model_card_printer.utils.html_utils import (
    add_custom_visualization_html,
    add_textcontent_html,
    add_visualization_collection_html,
    create_html_template
)

@dataclasses.dataclass
class ModelCard(ModelCardBaseField):
    """
    This class constructs the model card.

    This class is used to encapsulate individual pieces of content that will be part
    of the final model card.

    Attributes:
    - model_details: Descriptive metadata for the model.
    - training_dataset_details: Descriptive and quantitative metadata for the dataset used to train model.
    - validation_dataset_details: Descriptive and quantitative metadata for the dataset used to validate model.
    - custom_visuals: Additional custom visuals to populate the model card.
    - custom_documentation: Additional documentation to be added to model card.
    - created_date: Model card's creation date.
    - _all_visual_names: List of all visualization names stored in model card (for deconflicting names when creating HTML)
    """
    model_details: ModelDetails = dataclasses.field(default_factory = ModelDetails)
    training_dataset_details: DatasetMetadata = dataclasses.field(default_factory = DatasetMetadata)
    validation_dataset_details: DatasetMetadata = dataclasses.field(default_factory = DatasetMetadata)
    custom_visuals: CustomVisuals = dataclasses.field(default_factory = CustomVisuals)
    custom_documentation: List[CustomDetails] = dataclasses.field(default_factory = list)
    created_date: Optional[str] = None
    _all_visual_names: Optional[list] = dataclasses.field(default_factory = list)

    def validate_visualization(self, visualization_object: Any, visualization_name: str) -> None:
        """
        Validates visualization object and its name for HTML compatibility.
        
        Parameters:
        - visualization (Any): Any Python visualization object that supports HTML.
        - visualization_name (str): Name of visualization.

        Returns:
        - None
        """
        if visualization_name in self._all_visual_names:
            raise ValueError(f"'{visualization_name}' already in use. Please use a different name.")

        if "to_html" not in dir(visualization_object):
            raise ValueError(f"Visualization object does not have 'to_html' attribute. Please use a different Python object class.")

    def create_visualization(self, visualization_object: Any, visualization_name: str) -> Visualization:
        """
        Creates Visualization object.

        Parameters:
        - visualization (Any): Any Python visualization object that supports HTML.
        - visualization_name (str): Name of visualization.

        Returns:
        - Visualization: Initialised Visualization class with specified visualization.
        """
        created_visualization = Visualization()
        created_visualization.visualization_name = visualization_name
        created_visualization.visualization_object = visualization_object
        created_visualization.visualization_type = self._get_type(visualization_object)

        return created_visualization
    
    def create_dataset(self, dataset_object: Any, dataset_name: str) -> Dataset:
        """
        Creates Dataset object

        Parameters:
        - dataset_object (Any): Any dataset object.
        - dataset_name (str): Name of dataset.

        Returns:
        - Dataset: Initialised Dataset class with specified dataset.
        """
        created_dataset = Dataset()
        created_dataset.dataset_name = dataset_name
        created_dataset.dataset_object = dataset_object

        return created_dataset

    def add_training_dataset(self, training_features: Any, training_labels: Any) -> None:
        """
        Stores training dataset objects into training_dataset_details attribute.

        Parameters:
        - training_features (Any): Dataset (features) of any type used for training model.
        - training_labels (Any): Dataset (labels) of any type used for training model.

        Return:
        - None
        """
        # Create Dataset object for training features
        training_features = self.create_dataset(training_features, "Training Features")

        # Create Dataset object for training labels
        training_labels = self.create_dataset(training_labels, "Training Labels")

        # Store training dataset objects inside class
        self.training_dataset_details.dataset_list = [training_features, training_labels]

    def add_custom_documentation(self, documentation: str, document_name: str) -> None:
        """
        Adds custom documentation to model card.
        
        Parameters:
        - documentation (str): Text in markdown format.
        - document_name (str): Name of documentation.

        Returns:
        - None
        """
        # Store documentation in CustomDetails object
        custom_doc = CustomDetails()
        custom_doc.documentation = documentation
        custom_doc.document_name = document_name

        # Store documentation in model card
        self.custom_documentation.append(custom_doc)

    def add_individual_custom_visualization(self, visualization: Any, visualization_name: str) -> None:
        """
        Adds individual custom visualization to model card.
        
        Parameters:
        - visualization (Any): Any Python visualization class that supports HTML.
        - visualization_name (str): Name of visualization.

        Returns:
        - None
        """
        # Validate visualization
        self.validate_visualization(visualization, visualization_name)

        # Store visualization_name in model card
        self._all_visual_names.append(visualization_name)

        # Create Visualization class object
        custom_visualization = self.create_visualization(visualization, visualization_name)

        # Store Visualization class object inside model card
        self.custom_visuals.individual_visualizations.append(custom_visualization)

    def add_custom_visualization_collection(self, dict_visualization_objects: Dict[str, Any], collection_name: str, documentation: str = None) -> None:
        """
        Adds collection of custom visualizations to model card.

        Usage Example:
            model_card = ConstructModelCard().create()
            df_train_y = pd.DataFrame({data = {"target": [1,0,0,1,0,1,1]}})
            df_eval_y = pd.DataFrame({data = {"target": [1,0,0,1,0,1,1]}})
            dict_visualization_objects = {"training_labels": df_train_y.plot(kind="hist"), "eval_labels": df_eval_y.plot(kind="hist")}

            documentation_markdown = '''
            # Here are all the custom visualizations in a collection

            They have a dedicated section.
            '''

            model_card.add_custom_visualization_collection(dict_visualization_objects, "training and evaluation labels", documentation_markdown)

        Parameters:
        - dict_visualization_objects (Dict[str, Any]): Dictionary containing name of visualizations and their visualization objects.
        - collection_name (str): Name of collection.
        - documentation (str): Any documentation related to the visualization collection (default = None)

        Returns:
        - None
        """
        # Create Visualization class objects and store in list
        lst_visuals = []
        lst_visual_names = []
        for visual_name, visual_object in dict_visualization_objects.items():
            
            # Validate visualization
            self.validate_visualization(visual_object, visual_name)

            lst_visual_names.append(visual_name)

            # Store Visualization object
            custom_visualization = self.create_visualization(visual_object, visual_name)
            lst_visuals.append(custom_visualization)

        # Store all visualization names
        self._all_visual_names.extend(lst_visual_names)

        # Create VisualizationCollection
        visualization_collection = VisualizationCollection()
        visualization_collection.collection_name = collection_name
        visualization_collection.visualizations = lst_visuals
        visualization_collection.documentation = documentation

        # Store collection in model card
        self.custom_visuals.visualization_collections.append(visualization_collection)

    def add_training_dataset_visualization(self, visualization: Any, visualization_name: str) -> None:
        """
        Adds training dataset-related visual to model card.

        Parameters:
        - visualization (Any): Any Python visualization object that supports HTML.
        - visualization_name (str): Name of visualization.

        Returns:
        - None
        """
        # Validate visualization
        self.validate_visualization(visualization, visualization_name)

        # Store visualization name
        self._all_visual_names.append(visualization_name)

        # Initialise VisualizationCollection to enable storing of visuals
        if not self.training_dataset_details.dataset_visualization_collection.collection_name:
            created_visualization_collection = VisualizationCollection()
            created_visualization_collection.collection_name = "Training Dataset"
            self.training_dataset_details.dataset_visualization_collection = created_visualization_collection

        # Create Visualization object with visual
        visualization = self.create_visualization(visualization, visualization_name)

        # Store Visualization object inside VisualCollection
        self.training_dataset_details.dataset_visualization_collection.visualizations.append(visualization)

    def add_validation_dataset_visualization(self, visualization: Any, visualization_name: str) -> None:
        """
        Adds validation dataset-related visual to model card.

        Parameters:
        - visualization (Any): Any Python visualization object that supports HTML.
        - visualization_name (str): Name of visualization.

        Returns:
        - None
        """
        # Validate visualization
        self.validate_visualization(visualization, visualization_name)

        # Store visualization name
        self._all_visual_names.append(visualization_name)

        # Initialise VisualizationCollection to enable storing of visuals
        if not self.validation_dataset_details.dataset_visualization_collection.collection_name:
            created_visualization_collection = VisualizationCollection()
            created_visualization_collection.collection_name = "Validation Dataset"
            self.training_dataset_details.dataset_visualization_collection = created_visualization_collection

        # Create Visualization object with visual
        visualization = self.create_visualization(visualization, visualization_name)

        # Store Visualization object inside VisualCollection
        self.validation_dataset_details.dataset_visualization_collection.visualizations.append(visualization)

    def show(self, is_dark_mode: bool = True) -> IPython.core.display.HTML:
        """
        Displays model card's HTML in Jupyter Notebook interface.

        Parameters:
        - self: Current instance of ModelCard class.
        - is_dark_mode (bool): Boolean flag to enable dark mode for HTML (default = True).

        Returns:
        - IPython.core.display.HTML: Displayed HTML content of model card.
        """
        # Create HTML for model card
        model_card_html = self.to_html(is_dark_mode = is_dark_mode)

        # Display HTML
        return IPython.display.HTML(model_card_html)

    def to_html(self, is_dark_mode: bool = True) -> str:
        """
        Converts model card into HTML.

        Parameters:
        - is_dark_mode (bool): Boolean flag to enable dark mode for HTML (default = True).

        Returns:
        - str: Prettified HTML string.
        """
        # Create HTML template
        model_card_soup = create_html_template(dark_mode = is_dark_mode)
        
        # Add model's documentation to HTML body
        model_card_soup = add_textcontent_html(SoupObject = model_card_soup,
                                               textcontent = self.model_details.documentation,
                                               div_id = f"{self.model_details.model_name} text")

        # Add training dataset documentation and visuals together if visuals exist
        if self.training_dataset_details.dataset_visualization_collection.collection_name:

            # Add documentation to VisualCollection
            self.training_dataset_details.dataset_visualization_collection.documentation = self.training_dataset_details.documentation

            # Add documentation and visuals HTML together
            model_card_soup = add_visualization_collection_html(SoupObject = model_card_soup,
                                                                visualizationcollection = self.training_dataset_details.dataset_visualization_collection,
                                                                div_id = f"{self.training_dataset_details.dataset_visualization_collection.collection_name} visuals and text",
                                                                dark_mode = is_dark_mode)

        # Only add training dataset documentation if no visuals
        else:
            model_card_soup = add_textcontent_html(SoupObject = model_card_soup,
                                                   textcontent = self.training_dataset_details.documentation,
                                                   div_id = "training dataset text")

        # Add validation dataset documentation and visuals together if visuals exist
        if self.validation_dataset_details.dataset_visualization_collection.collection_name:

            # Add documentation to VisualCollection
            self.validation_dataset_details.dataset_visualization_collection.documentation = self.validation_dataset_details.documentation

            # Add documentation and visuals HTML together
            model_card_soup = add_visualization_collection_html(SoupObject = model_card_soup,
                                                                visualizationcollection = self.validation_dataset_details.dataset_visualization_collection,
                                                                div_id = f"{self.validation_dataset_details.dataset_visualization_collection.collection_name} visuals and text",
                                                                dark_mode = is_dark_mode)

        # Only add training dataset documentation if no visuals
        else:
            model_card_soup = add_textcontent_html(SoupObject = model_card_soup,
                                                   textcontent = self.validation_dataset_details.documentation,
                                                   div_id = "validation dataset text")
        
        # Add all custom documentation to HTML body
        for custom_doc in self.custom_documentation:
            model_card_soup = add_textcontent_html(SoupObject = model_card_soup,
                                                   textcontent = custom_doc.documentation,
                                                   div_id = f"{custom_doc.document_name} text")

        # Add custom visualization collections to HTML body
        for visualization_collection in self.custom_visuals.visualization_collections:
            model_card_soup = add_visualization_collection_html(SoupObject = model_card_soup,
                                                                visualizationcollection = visualization_collection,
                                                                div_id = f"{visualization_collection.collection_name} visuals and text",
                                                                dark_mode = is_dark_mode)

        # Add individual custom visualizations to HTML body
        for custom_visualization in self.custom_visuals.individual_visualizations:
            model_card_soup = add_custom_visualization_html(SoupObject = model_card_soup,
                                                            visualization = custom_visualization,
                                                            div_id = f"{custom_visualization.visualization_name} visual",
                                                            dark_mode = is_dark_mode)

        # Pretty-print HTML document
        model_card_html = model_card_soup.prettify()
        
        return model_card_html

    def write_html(self, file_path: str, is_dark_mode: bool = True) -> None:
        """
        Writes model card to HTML file representation.

        Parameters:
        - file_path (str): A string representing a local file path.
        - is_dark_mode (bool): Boolean flag to enable dark mode for HTML (default = True).

        Returns:
        - None
        """
        # Create HTML for model card
        model_card_html = self.to_html(is_dark_mode = is_dark_mode)

        with open(file_path, "w") as file:
            file.write(model_card_html)

    def write_json(self, file_path: str) -> None:
        """
        Writes model card to JSON file representation.

        Parameters:
        - file_path (str): A string representing a local file path.

        Returns:
        - None
        """
        # Create JSON for model card
        model_card_json = self.to_json()

        with open(file_path, "w") as file:
            file.write(model_card_json)
