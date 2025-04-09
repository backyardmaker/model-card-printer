"""
This file contains the main utilities to create model cards
using trained models and their datasets, including any
additional custom data visualisation.
"""
# Standard Library Imports
import json
from datetime import (
    datetime,
    timezone
)
from pathlib import (
    Path
)

# Local Application Imports
from model_card_printer.model_card import (
    ModelCard
)

class ModelCardPrinter():
    """
    This class provides the main utilities to create a model card.
    """
    
    def __init__(self, file_path: str = None, data_dict: dict = None):
        """
        Parameters:
        - self: Current instance of ModelCardPrinter class.
        - file_path (str): File path to load model card (.json or .html).
        - data_dict (dict): Dictionary containing model card data.
        """
        self.current_datetime = datetime.now(timezone.utc)
        self.file_path = file_path
        self.data_dict = data_dict

    @classmethod
    def generate_card(cls) -> ModelCard:
        """
        Creates ModelCard object.
        """
        # Initialise ModelCard object
        modelcard = ModelCard()

        # Store created date
        current_datetime = cls().current_datetime
        current_date_str = current_datetime.strftime("%d %B %Y")
        modelcard.created_date = current_date_str

        return modelcard

    def load_from_json(self) -> ModelCard:
        """
        Creates ModelCard from JSON file.

        Parameters:
        - self: Current instance of ModelCardPrinter class.

        Returns:
        - ModelCard: Created model card from JSON file.
        """
        if not self.file_path:
            raise ValueError("There is no JSON file provided. Re-initialise with the JSON file path using 'file_path' parameter.")

        if Path(self.file_path).is_file() and Path(self.file_path).suffix == ".json":

            # Load JSON file
            dict_json = json.load(open(self.file_path))

            # Create model card with JSON dictionary
            modelcard = ModelCard()._from_json(ModelCard(), dict_json)
        
        # Raise ValueError if invalid file path
        else:
            raise ValueError(f"Invalid JSON file path provided: {self.file_path}")

        return modelcard

    def load_from_dict(self) -> ModelCard:
        """
        Creates ModelCard from Python dictionary.

        Parameters:
        - self: Current instance of ModelCardPrinter class.

        Returns:
        - ModelCard: Created model card from dictionary.
        """
        if not self.data_dict:
            raise ValueError("There is no data dictionary provided. Re-initialise with the data dictionary using 'data_dict' parameter.")

        # Create model card with dictionary
        modelcard = ModelCard()._from_json(ModelCard(), self.data_dict)

        return modelcard

