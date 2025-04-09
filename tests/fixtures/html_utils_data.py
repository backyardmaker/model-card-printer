"""
Fixtures for unit testing html_utils.py.
"""
# Third-party Imports
import pandas as pd
import plotly.graph_objects as go

# Local Application Imports
from fixtures.model_card_data import (
    mock_visualization1,
    mock_visualization2,
    mock_visualization_collection
)
from model_card_printer.model_card_components import (
    Visualization,
    VisualizationCollection
)

# Initalise model card CSS fixture
TEST_MODEL_CARD_CSS = """
.body-dark-mode {
    background-color: #252525;  /* Dark grey background */
    color: #d9d9d9;  /* Light grey text */
    font-family: Arial, sans-serif; /* Font type */
}

.body-light-mode {
    background-color: #ffffff; /* Light background */
    color: #333333; /* Dark text for good contrast */
    font-family: 'Arial', sans-serif;
}

/* Container class for visuals in a collection */
.div-container-visualcollection {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border-radius: 10px;
    border: 0.5px solid lightgrey;
    gap: 5px;
    margin: 20px;
    padding: 15px;
    position: relative;
}

/* div class for visual of visualcollection */
.div-visual-in-container {
    display: flex;
    box-sizing: border-box;
    justify-content: center;
    align-items: center;
    height: auto;
    max-height: 300px;
    min-width: 100px;
    max-width: 300px;
}

/* div class for headers of visualcollection */
.div-text-visualcollection {
    grid-column: 1 / 4;
}

/* div class for text content */
.div-textcontent {
    border-radius: 10px;
    border: 0.5px solid lightgrey;
    margin: 20px;
    padding: 15px;
}

/* div class for custom visual */
.div-custom-visual {
    height: auto;
    max-height: 500px;
    min-width: 100px;
    margin: 20px;
    padding: 15px;
    border-radius: 10px;
    border: 0.5px solid lightgrey;
}
"""
# Create test Visualization object with plotly figure
TEST_VISUALIZATION_PLOTLY = Visualization(visualization_object = go.Figure(),
                                          visualization_name = "test plotly figure",
                                          visualization_type = type(go.Figure()))

# Create test Visualization object with pandas plot figure
mock_dataframe_plot = pd.DataFrame(data = {"test_col": [1,2,3,4,5]}).plot(kind = "hist")
TEST_VISUALIZATION_PANDAS = Visualization(visualization_object = mock_dataframe_plot,
                                          visualization_name = "test pandas figure",
                                          visualization_type = type(pd.DataFrame))

TEST_VISUALIZATION_COLLECTION_NO_DOCUMENTATION = VisualizationCollection(collection_name = "test visual collection",
                                                                         visualizations = [mock_visualization1, mock_visualization2])

test_css_selector_data = [(
    "body-dark-mode",
    TEST_MODEL_CARD_CSS,
"""body-dark-mode {
    background-color: #252525;  /* Dark grey background */
    color: #d9d9d9;  /* Light grey text */
    font-family: Arial, sans-serif; /* Font type */
}"""
)]

test_add_css_style_data = [(
    "<html></html>",
    "<html><head></head></html>",
    "<html><head><style></style></head></html>",
    "<html>\n <head>\n  <style>\n   .body-dark-mode {\n    background-color: #252525;  /* Dark grey background */\n    color: #d9d9d9;  /* Light grey text */\n    font-family: Arial, sans-serif; /* Font type */\n}\n\n.body-light-mode {\n    background-color: #ffffff; /* Light background */\n    color: #333333; /* Dark text for good contrast */\n    font-family: 'Arial', sans-serif;\n}\n\n/* Container class for visuals in a collection */\n.div-container-visualcollection {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);\n    border-radius: 10px;\n    border: 0.5px solid lightgrey;\n    gap: 5px;\n    margin: 20px;\n    padding: 15px;\n    position: relative;\n}\n\n/* div class for visual of visualcollection */\n.div-visual-in-container {\n    display: flex;\n    box-sizing: border-box;\n    justify-content: center;\n    align-items: center;\n    height: auto;\n    max-height: 300px;\n    min-width: 100px;\n    max-width: 300px;\n}\n\n/* div class for headers of visualcollection */\n.div-text-visualcollection {\n    grid-column: 1 / 4;\n}\n\n/* div class for text content */\n.div-textcontent {\n    border-radius: 10px;\n    border: 0.5px solid lightgrey;\n    margin: 20px;\n    padding: 15px;\n}\n\n/* div class for custom visual */\n.div-custom-visual {\n    height: auto;\n    max-height: 500px;\n    min-width: 100px;\n    margin: 20px;\n    padding: 15px;\n    border-radius: 10px;\n    border: 0.5px solid lightgrey;\n}\n  </style>\n </head>\n</html>\n"
)]

test_create_html_template_data = [(
    '<html>\n <head>\n  <style>\n   .body-dark-mode {\n    background-color: #252525;  /* Dark grey background */\n    color: #d9d9d9;  /* Light grey text */\n    font-family: Arial, sans-serif; /* Font type */\n}\n\n.body-light-mode {\n    background-color: #ffffff; /* Light background */\n    color: #333333; /* Dark text for good contrast */\n    font-family: \'Arial\', sans-serif;\n}\n\n/* Container class for visuals in a collection */\n.div-container-visualcollection {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);\n    border-radius: 10px;\n    border: 0.5px solid lightgrey;\n    gap: 5px;\n    margin: 20px;\n    padding: 15px;\n    position: relative;\n}\n\n/* div class for visual of visualcollection */\n.div-visual-in-container {\n    display: flex;\n    box-sizing: border-box;\n    justify-content: center;\n    align-items: center;\n    height: auto;\n    max-height: 300px;\n    min-width: 100px;\n    max-width: 300px;\n}\n\n/* div class for headers of visualcollection */\n.div-text-visualcollection {\n    grid-column: 1 / 4;\n}\n\n/* div class for text content */\n.div-textcontent {\n    border-radius: 10px;\n    border: 0.5px solid lightgrey;\n    margin: 20px;\n    padding: 15px;\n}\n\n/* div class for custom visual */\n.div-custom-visual {\n    height: auto;\n    max-height: 500px;\n    min-width: 100px;\n    margin: 20px;\n    padding: 15px;\n    border-radius: 10px;\n    border: 0.5px solid lightgrey;\n}\n  </style>\n </head>\n <body class="body-dark-mode">\n </body>\n</html>\n',
    '<html>\n <head>\n  <style>\n   .body-dark-mode {\n    background-color: #252525;  /* Dark grey background */\n    color: #d9d9d9;  /* Light grey text */\n    font-family: Arial, sans-serif; /* Font type */\n}\n\n.body-light-mode {\n    background-color: #ffffff; /* Light background */\n    color: #333333; /* Dark text for good contrast */\n    font-family: \'Arial\', sans-serif;\n}\n\n/* Container class for visuals in a collection */\n.div-container-visualcollection {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);\n    border-radius: 10px;\n    border: 0.5px solid lightgrey;\n    gap: 5px;\n    margin: 20px;\n    padding: 15px;\n    position: relative;\n}\n\n/* div class for visual of visualcollection */\n.div-visual-in-container {\n    display: flex;\n    box-sizing: border-box;\n    justify-content: center;\n    align-items: center;\n    height: auto;\n    max-height: 300px;\n    min-width: 100px;\n    max-width: 300px;\n}\n\n/* div class for headers of visualcollection */\n.div-text-visualcollection {\n    grid-column: 1 / 4;\n}\n\n/* div class for text content */\n.div-textcontent {\n    border-radius: 10px;\n    border: 0.5px solid lightgrey;\n    margin: 20px;\n    padding: 15px;\n}\n\n/* div class for custom visual */\n.div-custom-visual {\n    height: auto;\n    max-height: 500px;\n    min-width: 100px;\n    margin: 20px;\n    padding: 15px;\n    border-radius: 10px;\n    border: 0.5px solid lightgrey;\n}\n  </style>\n </head>\n <body class="body-light-mode">\n </body>\n</html>\n'
)]

test_add_textcontent_html_data = [(
    "<html><head><style></style></head></html>",
    "<html><head><style></style></head><body></body></html>"
)]

test_create_visualization_html_data = [(
    TEST_VISUALIZATION_PANDAS,
    TEST_VISUALIZATION_PLOTLY
)]

test_add_visualization_collection_html_data = [(
    "<html><body></body></html>",
    mock_visualization_collection,
    TEST_VISUALIZATION_COLLECTION_NO_DOCUMENTATION
)]

test_add_custom_visualization_html_data = [(
    "<html><body></body></html>",
    TEST_VISUALIZATION_PLOTLY
)]