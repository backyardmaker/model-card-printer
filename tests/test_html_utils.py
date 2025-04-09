"""
Unit tests for html_utils.py
"""
# Standard Library Imports
from unittest.mock import (
    MagicMock,
    Mock,
    patch
)
# Third-party Imports
import plotly.graph_objects as go
import pytest
from bs4 import (
    BeautifulSoup
)

# Local Application Imports
import model_card_printer.utils.html_utils as html_utils
from fixtures.html_utils_data import (
    test_add_css_style_data,
    test_add_textcontent_html_data,
    test_add_visualization_collection_html_data,
    test_add_custom_visualization_html_data,
    test_create_html_template_data,
    test_create_visualization_html_data,
    test_css_selector_data,
    TEST_MODEL_CARD_CSS
)
from model_card_printer.model_card_components import (
    Visualization,
    VisualizationCollection
)
from model_card_printer.utils.html_utils import (
    add_css_style,
    add_custom_visualization_html,
    add_textcontent_html,
    add_visualization_collection_html,
    create_html_template,
    create_visualization_html,
    css_selector,
    load_css_as_text
)

@patch("model_card_printer.utils.html_utils.open")
def test_load_css_as_text(mock_open: MagicMock) -> None:
    """
    Test Case 1: Successfully load file with correct syntax.
    """
    # Mock 'read' method of 'open'
    mock_read = Mock(**{"read.return_value": "test"})
    mock_open.return_value.__enter__.return_value = mock_read

    # Get actual output
    test_path = "test_path"
    actual_output = load_css_as_text(test_path)

    # Assert actual and expected outputs are equal
    assert actual_output == "test"

    # Assert mock objects called correctly
    mock_open.assert_called_once_with(test_path, "r")
    mock_read.read.assert_called_once()

@pytest.mark.parametrize("test_input_element, test_input_css, expected_output", test_css_selector_data)
def test_css_selector(test_input_element: str, test_input_css: str, expected_output: str) -> None:
    """
    Test Case 1: Successfully return CSS declaration block.
    """
    # Get actual output
    actual_output = css_selector(test_input_element, test_input_css)

    # Assert actual and expected outputs are equal
    assert actual_output == expected_output

@pytest.mark.parametrize("test_input_no_head_tag, test_input_with_head_tag_no_style_tag, test_input_with_head_tag, expected_output", test_add_css_style_data)
def test_add_css_style(test_input_no_head_tag: str, test_input_with_head_tag_no_style_tag: str, test_input_with_head_tag: str, expected_output: str) -> None:
    """
    Test Case 1: Successfully return HTML string (no head tag input).
    """
    # Convert input into BeautifulSoup object
    test_soup = BeautifulSoup(test_input_no_head_tag, "html.parser")

    # Get actual output
    actual_output = add_css_style(test_soup, TEST_MODEL_CARD_CSS)

    # Assert actual and expected outputs are equal
    assert isinstance(actual_output, BeautifulSoup)
    assert actual_output.prettify() == expected_output

    """
    Test Case 2: Successfully return HTML string (head tag but no style tag input).
    """
    # Convert input into BeautifulSoup object
    test_soup = BeautifulSoup(test_input_with_head_tag_no_style_tag, "html.parser")

    # Get actual output
    actual_output = add_css_style(test_soup, TEST_MODEL_CARD_CSS)

    # Assert actual and expected outputs are equal
    assert isinstance(actual_output, BeautifulSoup)
    assert actual_output.prettify() == expected_output

    """
    Test Case 3: Successfully return HTML string (head tag and style tag input).
    """
    # Convert input into BeautifulSoup object
    test_soup = BeautifulSoup(test_input_with_head_tag, "html.parser")

    # Get actual output
    actual_output = add_css_style(test_soup, TEST_MODEL_CARD_CSS)

    # Assert actual and expected outputs are equal
    assert isinstance(actual_output, BeautifulSoup)
    assert actual_output.prettify() == expected_output

@pytest.mark.parametrize("expected_output_dark_mode, expected_output_light_mode", test_create_html_template_data)
def test_create_html_template(expected_output_dark_mode: str, expected_output_light_mode: str) -> None:
    """
    Test Case 1: Successfully return HTML string (dark mode enabled)
    """
    # Overwrite model card CSS with test CSS
    html_utils.MODEL_CARD_CSS_STYLES_TEXT = TEST_MODEL_CARD_CSS
    
    # Get actual output
    actual_output = create_html_template(dark_mode = True)

    # Assert actual and expected outputs are equal
    assert isinstance(actual_output, BeautifulSoup)
    assert actual_output.prettify() == expected_output_dark_mode

    """
    Test Case 2: Successfully return HTML string (dark mode disabled)
    """
    # Get actual output
    actual_output = create_html_template(dark_mode = False)

    # Assert actual and expected outputs are equal
    assert isinstance(actual_output, BeautifulSoup)
    assert actual_output.prettify() == expected_output_light_mode

@pytest.mark.parametrize("test_input_no_body, test_input_with_body", test_add_textcontent_html_data)
def test_add_textcontent_html(test_input_no_body: str, test_input_with_body: str) -> None:
    """
    Test Case 1: Successfully raise ValueError due to missing 'body' element.
    """
    # Create test content
    test_textcontent = "# Test"

    # Create BeautifulSoup object with test input
    test_soup = BeautifulSoup(test_input_no_body, "html.parser")

    # Assert ValueError occurred
    with pytest.raises(ValueError) as excinfo:
        _ = add_textcontent_html(test_soup, test_textcontent, "test id")
    
    # Assert error message is correct
    assert "HTML document missing 'body' element." in str(excinfo)

    """
    Test Case 2: Successfully return HTML with added text content.
    """
    # Create BeautifulSoup object with test input
    test_soup = BeautifulSoup(test_input_with_body, "html.parser")

    # Get actual output
    actual_soup = add_textcontent_html(test_soup, test_textcontent, "test id")

    # Assert actual BeautifulSoup object has the correct elements
    assert actual_soup.find("div", class_ = "div-textcontent") is not None
    assert actual_soup.find("div", class_ = "div-textcontent")["id"] == "test id"
    assert actual_soup.find("h1") is not None

    """
    Test Case 3: Successfully return HTML with no text content.
    """
    # Get actual output
    actual_soup = add_textcontent_html(test_soup, "", "test id")

    # Assert original soup object is returned
    assert actual_soup is test_soup

@pytest.mark.parametrize("test_visual_pandas, test_visual_plotly", test_create_visualization_html_data)
def test_create_visualization_html(test_visual_pandas: Visualization, test_visual_plotly: Visualization) -> None:
    """
    Test Case 1: Successfully create visualization HTML (pandas plot figure).
    """
    # Get actual output
    is_dark_mode = True
    actual_html = create_visualization_html(test_visual_pandas, is_dark_mode)

    # Create BeautifulSoup object with actual output
    actual_soup = BeautifulSoup(actual_html, "html.parser")

    # Assert visualization HTML has 'h2' element (created header)
    assert actual_soup.find("h2") is not None

    # Assert visualization HTML has 'div' element (created visualization HTML)
    assert actual_soup.find("div") is not None
    assert actual_soup.find("div", class_ = "plotly-graph-div") is not None

    # Assert Visualization class object updated
    assert test_visual_pandas.visualization_html is not None
    assert test_visual_pandas.is_dark_mode == str(is_dark_mode)

    """
    Test Case 2: Successfully create visualization HTML (plotly figure with no title).
    """
    # Get actual output
    is_dark_mode = True
    actual_html = create_visualization_html(test_visual_plotly, is_dark_mode)

    # Create BeautifulSoup object with actual output
    actual_soup = BeautifulSoup(actual_html, "html.parser")

    # Assert visualization HTML has no 'h2' element (title is updated into the plot)
    assert actual_soup.find("h2") is None

    # Assert visualization HTML has 'div' element (created visualization HTML)
    assert actual_soup.find("div") is not None
    assert actual_soup.find("div", class_ = "plotly-graph-div") is not None

    # Assert Visualization class object updated
    assert test_visual_plotly.visualization_html is not None
    assert test_visual_plotly.is_dark_mode == str(is_dark_mode)

    """
    Test Case 3: Successfully create visualization HTML (plotly figure with title).
    """
    # Add title to test Plotly figure
    plotly_fig_with_title = go.Figure(test_visual_plotly.visualization_object)
    plotly_fig_with_title.update_layout(title = "test plotly figure")
    test_visual_plotly.visualization_object = plotly_fig_with_title
    test_visual_plotly.visualization_html = None

    # Get actual output
    actual_html = create_visualization_html(test_visual_plotly, is_dark_mode)

    # Create BeautifulSoup object with actual output
    actual_soup = BeautifulSoup(actual_html, "html.parser")

    # Assert visualization HTML has no 'h2' element (title is updated into the plot)
    assert actual_soup.find("h2") is None

    # Assert visualization HTML has 'div' element (created visualization HTML)
    assert actual_soup.find("div") is not None
    assert actual_soup.find("div", class_ = "plotly-graph-div") is not None

    # Assert Visualization class object updated
    assert test_visual_plotly.visualization_html is not None
    assert test_visual_plotly.is_dark_mode == str(is_dark_mode)

    """
    Test Case 4: Successfully raise AttributeError due to no 'to_html' attribute.
    """
    # Create mock object
    mock_visual_no_html = Mock(**{"to_html.side_effect": AttributeError})

    # Create Visualization object
    mock_visual_no_html = Visualization(visualization_name = "mock visual", visualization_object = mock_visual_no_html, visualization_type = type(mock_visual_no_html))

    # Assert AttributeError occurred
    with pytest.raises(AttributeError) as excinfo:
        _ = create_visualization_html(mock_visual_no_html, is_dark_mode)
    
    # Assert error message is correct
    assert "Object is not HTML-compatible: mock visual" in str(excinfo)

    """
    Test Case 5: Successfully return visualization HTML from Visualization object.
    """
    # Create Visualization object add store mock HTML
    test_html = "test"
    mock_visual_with_html = Visualization(visualization_html = test_html, is_dark_mode = str(is_dark_mode))

    # Get actual output
    actual_output = create_visualization_html(mock_visual_with_html, is_dark_mode)

    # Assert actual and expected outputs are equal
    assert actual_output is test_html

@patch("model_card_printer.utils.html_utils.create_visualization_html")
@pytest.mark.parametrize("test_input_html, test_input_visualization_collection, test_input_visualization_collection_no_documentation", test_add_visualization_collection_html_data)
def test_add_visualization_collection_html(mock_create_visualization_html: MagicMock,
                                           test_input_html: str,
                                           test_input_visualization_collection: VisualizationCollection,
                                           test_input_visualization_collection_no_documentation: VisualizationCollection) -> None:
    """
    Test Case 1: Succesfully update BeautifulSoup object with HTML of visualization collection (with documentation).
    """
    # Create BeautifulSoup object with input HTML
    test_input_soup = BeautifulSoup(test_input_html, "html.parser")

    # Create intermediate output for mock object
    mock_create_visualization_html.side_effect = [f'<div class="none" id="{visual.visualization_name}" style="height:100%; width:100%;">TEST_VISUAL_HTML</div>' for visual in test_input_visualization_collection.visualizations]

    # Get actual output
    is_dark_mode = True
    actual_soup = add_visualization_collection_html(test_input_soup, test_input_visualization_collection, "test collection id", is_dark_mode)

    # Assert expected HTML elements are present
    assert actual_soup.find("div", id = "test collection id") is not None
    assert actual_soup.find("p") is not None
    assert test_input_visualization_collection.documentation in actual_soup.find("p")
    assert actual_soup.find("div", class_ = "div-visual-in-container") is not None

    # Assert mock object called correctly
    for visual in test_input_visualization_collection.visualizations:
        mock_create_visualization_html.assert_any_call(visual, dark_mode=is_dark_mode)

    """
    Test Case 2: Succesfully update BeautifulSoup object with HTML of visualization collection (no documentation).
    """
    # Create BeautifulSoup object with input HTML
    test_input_soup = BeautifulSoup(test_input_html, "html.parser")

    # Create intermediate output for mock object
    mock_create_visualization_html.side_effect = [f'<div class="none" id="{visual.visualization_name}" style="height:100%; width:100%;">TEST_VISUAL_HTML</div>' for visual in test_input_visualization_collection_no_documentation.visualizations]

    # Get actual output
    is_dark_mode = True
    actual_soup = add_visualization_collection_html(test_input_soup, test_input_visualization_collection_no_documentation, "test collection id", is_dark_mode)

    # Assert expected HTML elements are present
    assert actual_soup.find("div", id = "test collection id") is not None
    assert actual_soup.find("h1") is not None
    assert f"{test_input_visualization_collection.collection_name} Visualizations" in actual_soup.find("h1")
    assert actual_soup.find("div", class_ = "div-visual-in-container") is not None

    # Assert mock object called correctly
    for visual in test_input_visualization_collection.visualizations:
        mock_create_visualization_html.assert_any_call(visual, dark_mode=is_dark_mode)

    """
    Test Case 3: Successfully raise ValueError due to no 'body' element.
    """
    # Create test BeautifulSoup object
    test_input_soup = BeautifulSoup("<html></html>", "html.parser")

    # Assert ValueError occurred
    with pytest.raises(ValueError) as excinfo:
        _ = add_visualization_collection_html(test_input_soup, test_input_visualization_collection, "test collection id", is_dark_mode)

    # Assert error message is correct
    assert "HTML document missing 'body' element" in str(excinfo)

    """
    Test Case 4: Successfully return input BeautifulSoup object.
    """
    # Create test BeautifulSoup object
    test_input_soup = BeautifulSoup(test_input_html, "html.parser")

    # Get actual output
    actual_soup = add_visualization_collection_html(test_input_soup, VisualizationCollection(), "test collection id", is_dark_mode)

    # Assert actual and expected outputs are equal
    assert actual_soup is test_input_soup

@patch("model_card_printer.utils.html_utils.create_visualization_html")
@pytest.mark.parametrize("test_input_html, test_input_visualization", test_add_custom_visualization_html_data)
def test_add_custom_visualization_html(mock_create_visualization_html: MagicMock, test_input_html: str, test_input_visualization: Visualization) -> None:
    """
    Test Case 1: Successfully update BeautifulSoup object with HTML of visualization.
    """
    # Create BeautifulSoup object with input HTML
    test_input_soup = BeautifulSoup(test_input_html, "html.parser")

    # Create intermediate output for mock object
    mock_create_visualization_html.return_value = f'<div class="none" id="{test_input_visualization.visualization_name}" style="height:100%; width:100%;">TEST_VISUAL_HTML</div>'

    # Get actual output
    is_dark_mode = True
    actual_soup = add_custom_visualization_html(test_input_soup, test_input_visualization, "test custom visual", dark_mode = is_dark_mode)

    # Assert expected HTML elements are present
    assert actual_soup.find("div", id = test_input_visualization.visualization_name) is not None
    assert actual_soup.find("div", class_ = "div-custom-visual") is not None

    # Assert mock object called correctly
    mock_create_visualization_html.assert_called_once_with(test_input_visualization, dark_mode=is_dark_mode)

    # Reset mock object
    mock_create_visualization_html.reset_mock(return_value = True)

    """
    Test Case 2: Successfully update BeautifulSoup object with HTML of visualization (object HTML has no 'div' and 'id' tags).
    """
    # Create BeautifulSoup object with input HTML
    test_input_soup = BeautifulSoup(test_input_html, "html.parser")

    # Create intermediate output for mock object
    mock_create_visualization_html.return_value = "TEST_VISUAL_HTML"

    # Create test Visualization object
    test_visual = Visualization()

    # Get actual output
    is_dark_mode = True
    actual_soup = add_custom_visualization_html(test_input_soup, test_visual, "test custom visual", dark_mode = is_dark_mode)

    # Assert expected HTML elements are present
    assert actual_soup.find("div", id = "test custom visual") is not None
    assert actual_soup.find("div", class_ = "div-custom-visual") is not None

    # Assert mock object called correctly
    mock_create_visualization_html.assert_called_once_with(test_visual, dark_mode=is_dark_mode)

    """
    Test Case 3: Successfully raise ValueError due to no 'body' element.
    """
    # Create test BeautifulSoup object
    test_input_soup = BeautifulSoup("<html></html>", "html.parser")

    # Assert ValueError occurred
    with pytest.raises(ValueError) as excinfo:
        _ = add_custom_visualization_html(test_input_soup, test_visual, "test custom visual", dark_mode = is_dark_mode)

    # Assert error message is correct
    assert "HTML document missing 'body' element" in str(excinfo)
