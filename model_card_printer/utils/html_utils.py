"""
Utilities to create HTML for model cards.
"""
# Standard Library Imports
import os
import re

# Third-party Imports
import markdown
import pandas as pd
import plotly.graph_objects as go
from bs4 import BeautifulSoup

# Local Application Imports
from model_card_printer.model_card_components import Visualization, VisualizationCollection

# Activate "plotly" backend for pandas dataframe plotting
pd.options.plotting.backend = "plotly"

def load_css_as_text(path: str) -> str:
    """
    Loads CSS file as text.
    """
    with open(path, "r") as file:
        css_content = file.read()
    
    return css_content

# Initialise model card's CSS styles
MODEL_CARD_CSS_STYLES_TEXT = load_css_as_text(os.path.join("model_card_printer", "utils", "model_card_style.css"))

def css_selector(element_selector: str, css_text: str) -> str:
    """
    Returns specified CSS declaration block.

    Parameters:
    - element_selector (str): CSS selector to retrieve its declaration block.
    - css_text (str): CSS file in text format.

    Returns:
    - str: Specified CSS declaration block.
    """
    # Create regex pattern
    pattern = element_selector + r'\s*\{([^}]*)\}'

    # Retrieve CSS declaration block
    css_declaration_block = re.search(pattern, css_text).group()

    return css_declaration_block

def add_css_style(SoupObject: BeautifulSoup, css_styles: str) -> BeautifulSoup:
    """
    Adds all CSS styles to HTML document, inside <head> section where
    different <div> classes can be referenced.

    Parameters:
    - SoupObject (BeautifulSoup): HTML document BeautifulSoup object.
    - css_styles (str): All CSS styles loaded as a string.

    Returns:
    - BeautifulSoup: Parsed HTML document.
    """
    # Add CSS styles if "head" section of HTML does not exists
    if not SoupObject.html.head:
        head_tag = SoupObject.new_tag("head")
        style_tag = SoupObject.new_tag("style")
        style_tag.string = css_styles
        head_tag.append(style_tag)
        SoupObject.html.append(head_tag)

        return SoupObject
    
    # Add 'style' tag if it does not exist in 'head' section
    html_head_style_tag = SoupObject.head.find("style")
    if not html_head_style_tag:
        style_tag = SoupObject.new_tag("style")
        SoupObject.head.append(style_tag)

        # Update variable
        html_head_style_tag = SoupObject.head.find("style")

    # Replace CSS styles if "head" and its "style" section already exists
    if html_head_style_tag:
        html_head_style_tag.string = css_styles

        return SoupObject

def create_html_template(dark_mode: bool = True) -> BeautifulSoup:
    """
    Creates HTML template to populate content.

    Parameters:
    - dark_mode (bool): True if HTML generated to be dark, else False.

    Returns:
    - BeautifulSoup: BeautifulSoup object with 'body' element added.
    """
    # Initialise HTML document
    SoupObject = BeautifulSoup()

    # Add 'html' tag
    SoupObject.append(SoupObject.new_tag("html"))

    # Add CSS styles
    SoupObject = add_css_style(SoupObject, MODEL_CARD_CSS_STYLES_TEXT)

    # Create 'body' tag
    body_tag = SoupObject.new_tag("body")

    # Change body element to be dark (if applicable)
    if dark_mode:
        body_tag["class"] = "body-dark-mode"
    
    else:
        body_tag["class"] = "body-light-mode"

    # Add 'body' tag
    SoupObject.html.append(body_tag)

    return SoupObject

def add_textcontent_html(SoupObject: BeautifulSoup, textcontent: str, div_id: str) -> BeautifulSoup:
    """
    Adds text content in markdown format into HTML document.

    Parameters:
    - SoupObject (BeautifulSoup): HTML document BeautifulSoup object.
    - textcontent (str): Text to add into HTML document in sequence.
    - div_id (str): Unique ID of HTML element.

    Returns:
    - BeautifulSoup: Parsed HTML document.
    """
    # Check if HTML document has 'body' tag
    if not SoupObject.body:
        raise ValueError("HTML document missing 'body' element.")

    # Return Soup object if there is no text
    if not textcontent:
        return SoupObject

    # Create content HTML as unicode string
    content_html = markdown.markdown(textcontent)

    # Add "div" tag to content HTML for CSS style application
    content_html = f"<div>\n{content_html}\n</div>"

    # Add CSS style
    content_soup = BeautifulSoup(content_html, "html.parser")
    content_div = content_soup.find("div")
    content_div["class"] = "div-textcontent"
    content_div["id"] = div_id

    # Store content to body of HTML document
    SoupObject.body.extend(content_soup.contents)

    return SoupObject

def create_visualization_html(visualization: Visualization, dark_mode: bool = True) -> str:
    """
    Converts visualization object into HTML and stores it as an attribute.

    Parameters:
    - visualization (Visualization): Visualization class object that contains visualization object.
    - dark_mode (bool): Boolean flag to determine whether visualizations should be dark or light (default=True).

    Returns:
    - str: Visualization object's HTML.
    """
    # Return visualization HTML if attribute already exists
    if visualization.visualization_html and visualization.is_dark_mode == str(dark_mode):
        return visualization.visualization_html

    # Get visualization object from Visualization class object
    visualization_object = visualization.visualization_object

    # Update Plotly figure if missing title and/or to change visualization to dark mode
    if visualization.visualization_type == go.Figure:
        visualization_object = go.Figure(visualization_object)
        if not visualization_object.layout.title.text:
            visualization_object.update_layout(title = visualization.visualization_name,
                                               template = "plotly_dark" if dark_mode else "plotly")
        elif dark_mode:
            visualization_object.update_layout(template = "plotly_dark")

        object_header = ""

    # Create header for custom visualization if it has no title
    else:
        object_header = markdown.markdown(f"## {visualization.visualization_name}")

    # Convert object to html
    try:
        if visualization.visualization_type == go.Figure:
            object_html = visualization_object.to_html(config={'staticPlot': True},
                                                       include_plotlyjs = True,
                                                       include_mathjax = False,
                                                       full_html = False,
                                                       div_id = visualization.visualization_name)
        else:
            # Assumption: visualization object has "to_html" attribute
            object_html = visualization_object.to_html()

    except AttributeError:
        raise AttributeError(f"Object is not HTML-compatible: {visualization.visualization_name}")

    # Add header to object (if applicable)
    object_html = f"{object_header}\n{object_html}" if object_header else object_html

    # Store HTML inside Visualization object
    visualization.visualization_html = object_html

    # Set 'is_dark_mode' attribute inside Visualization object
    visualization.is_dark_mode = str(dark_mode)

    return object_html

def add_visualization_collection_html(SoupObject: BeautifulSoup, visualizationcollection: VisualizationCollection, div_id: str, dark_mode: bool = True) -> BeautifulSoup:
    """
    Adds visualization collection in a single section into HTML document.

    Parameters:
    - SoupObject (BeautifulSoup): HTML document BeautifulSoup object.
    - visualizationcollection (VisualizationCollection): VisualizationCollection class object that contains list of visualization objects.
    - div_id (str): Unique ID of HTML element.
    - dark_mode (bool): Boolean flag to determine whether visualizations should be dark or light (default=True).

    Returns:
    - BeautifulSoup: Parsed HTML document.
    """
    # Check if HTML document has 'body' tag
    if not SoupObject.body:
        raise ValueError("HTML document missing 'body' element.")

    # Return Soup object if no visuals available
    if not visualizationcollection.visualizations:
        return SoupObject

    # Create div section for collection of visuals
    collection_soup = BeautifulSoup(f"<div></div>", "html.parser")
    collection_div = collection_soup.find("div")
    collection_div["class"] = "div-container-visualcollection"
    collection_div["id"] = div_id

    # Create header/documentation for collection of visuals
    collection_header_html = markdown.markdown(f"{visualizationcollection.documentation}"
                                               if visualizationcollection.documentation
                                               else f"# {visualizationcollection.collection_name} Visualizations")
    collection_header_html = f"<div>{collection_header_html}</div>"
    header_soup = BeautifulSoup(collection_header_html, "html.parser")
    header_div = header_soup.find("div")
    header_div["class"] = "div-text-visualcollection"
    header_div["id"] = f"{visualizationcollection.collection_name} text"
    collection_div.extend(header_soup.contents)

    # Create HTML for each visual
    for visual in visualizationcollection.visualizations:
        
        # Create visual HTML
        visual_html = create_visualization_html(visual, dark_mode=dark_mode)

        # Add 'div' element (if applicable)
        visual_html = f"<div>{visual_html}</div>" if "div" not in visual_html else visual_html

        # Add class attribute to div
        visual_soup = BeautifulSoup(visual_html, "html.parser")
        visual_div = visual_soup.find("div", id = visual.visualization_name) if visual.visualization_type == go.Figure else visual_soup.find("div")
        visual_div["class"] = "div-visual-in-container"

        # Remove style that came with visual's HTML
        if "style" in visual_div.attrs.keys():
            del visual_div["style"]

        # Store visual into div section of collection of visuals
        collection_div.extend(visual_soup.contents)

    # Store visualcollection inside main HTML body
    SoupObject.body.extend(collection_soup.contents)

    return SoupObject

def add_custom_visualization_html(SoupObject: BeautifulSoup, visualization: Visualization, div_id: str, dark_mode: bool = True) -> BeautifulSoup:
    """
    Adds custom visualization (HTML-compatible) into HTML document.

    Parameters:
    - SoupObject (BeautifulSoup): HTML document BeautifulSoup object.
    - visualization (Visualization): Visualization class object that contains visualization object.
    - div_id (str): Unique ID of HTML element.
    - dark_mode (bool): Boolean flag to determine whether visualizations should be dark or light (default=True).

    Returns:
    - BeautifulSoup: Parsed HTML document.
    """
    # Check if HTML document has 'body' tag
    if not SoupObject.body:
        raise ValueError("HTML document missing 'body' element.")

    # Create HTML for visualization object
    object_html = create_visualization_html(visualization, dark_mode=dark_mode)

    # Add 'div' tag to object HTML (if applicable)
    object_html = f'<div class="none" id="{div_id}">{object_html}</div>' if "div" not in object_html else object_html

    # Add CSS style
    object_soup = BeautifulSoup(object_html, "html.parser")
    object_div = object_soup.find("div", id = visualization.visualization_name) if visualization.visualization_type == go.Figure else object_soup.find("div", id = div_id)
    object_div["class"] = "div-custom-visual"

    # Remove style that came with visual's HTML
    if "style" in object_div.attrs.keys():
        del object_div["style"]

    # Store object HTML to body of HTML document
    SoupObject.body.extend(object_soup.contents)

    return SoupObject
