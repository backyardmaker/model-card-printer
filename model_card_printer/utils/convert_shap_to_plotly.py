"""
Utilities to convert SHAP plots into Plotly plots to enable additional functions such as image conversion to HTML.
"""
# Third-party Imports
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import shap

def get_shap_values_df(shap_values: shap._explanation.Explanation, explainer_df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates SHAP values dataframe with their feature names from generated SHAP values.

    Parameters:
    - shap_values (shap._explanation.Explanation): SHAP values from specified SHAP explainer.
    - explainer_df (pd.DataFrame): Pandas dataframe containing dataset used to fit SHAP explainer.

    Returns:
    - pd.DataFrame: Pandas dataframe containing feature names and their SHAP values.
    """
    # Get feature names
    feature_names = explainer_df.columns

    # Create shap values dataframe with feature names as columns
    shap_values_df = pd.DataFrame(shap_values[..., 1].values, columns = feature_names)

    return shap_values_df

def get_shap_feature_importance_df(shap_values: shap._explanation.Explanation, explainer_df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates SHAP feature importance dataframe (in descending order) given SHAP values and the dataset the SHAP explainer was fitted on.

    Parameters:
    - shap_values (shap._explanation.Explanation): SHAP values from specified SHAP explainer.
    - explainer_df (pd.DataFrame): Pandas dataframe containing dataset used to fit SHAP explainer.

    Returns:
    - pd.DataFrame: Pandas dataframe containing mean absolute SHAP values of each feature in dataset.
    """
    # Get feature names
    feature_names = explainer_df.columns

    # Create shap values dataframe with feature names as columns
    shap_values_df = get_shap_values_df(shap_values, explainer_df)

    # Get mean absolute value of the SHAP values for each feature
    abs_shap_vals = np.abs(shap_values_df.values).mean(0)

    # Create shap importance dataframe
    shap_importance_df = pd.DataFrame(list(zip(feature_names, abs_shap_vals)),
                                    columns=['feature_name','feature_importance_val'])

    # Sort shap importance dataframe in descending order
    shap_importance_df = shap_importance_df.sort_values(by=['feature_importance_val'],
                                                        ascending=False,
                                                        inplace=False)

    # Reset index
    shap_importance_df = shap_importance_df.reset_index(drop = True, inplace = False)

    return shap_importance_df

def label_percentile_range(df_row: pd.Series, df_percentile_dict: dict) -> str:
    """
    Create percentile range label for each feature value. 
    
    Parameters:
    - df_row (pd.Series): Pandas Dataframe row that contains the feature value.
    - df_percentile_dict (dict): Dictionary containing percentile values of each feature in the dataframe.

    Returns:
    - str: Percentile range label.
    """
    # Get feature name
    col_name = df_row["feature"]

    # Get feature value
    row_val = df_row["feature_value"]

    # Get dictionary containing percentile values of specified feature
    percentile_dict = df_percentile_dict[col_name]

    # Get percentile values
    percentile_25, percentile_50, percentile_75 = percentile_dict["25%"], percentile_dict["50%"], percentile_dict["75%"]

    # Check which percentile ranges do the feature value fall in
    if row_val < percentile_25:
        return "<25%"
    elif percentile_25<row_val< percentile_50:
        return "25-50%"
    elif percentile_50<row_val< percentile_75:
        return "50-75%"
    else:
        return ">75%"

def generate_beeswarm_plotly_figure(shap_values: shap._explanation.Explanation,
                                    explainer_df: pd.DataFrame,
                                    show_num_features: int,
                                    dark_mode: bool = True) -> go.Figure:
    """
    Generates SHAP beeswarm plot as a Plotly figure.

    Parameters:
    - shap_values (shap._explanation.Explanation): SHAP values from specified SHAP explainer.
    - explainer_df (pd.DataFrame): Pandas dataframe used to fit SHAP explainer.
    - show_num_features (int): Number of features to show on beeswarm plot.
    - dark_mode (bool): Boolean value (True or False) to display HTML in dark mode, default value is True.

    Returns:
    - go.Figure: Plotly figure for SHAP beeswarm plot.
    """
    # Get SHAP feature importance dataframe
    feature_importance_df = get_shap_feature_importance_df(shap_values, explainer_df)

    # Get list of features in descending order of importance from feature importance dataframe
    lst_features = feature_importance_df["feature_name"]

    # Get SHAP values dataframe
    shap_values_df = get_shap_values_df(shap_values, explainer_df)

    # Convert dataframe from wide to long format where feature columns are measured variables
    melted_explainer_df = explainer_df.melt(value_vars = [col for col in explainer_df.columns],
                                              var_name = "feature",
                                              value_name = "feature_value")

    # Store feature values' percentile inside melted explainer dataframe
    melted_explainer_df["percentile_range_label"] = melted_explainer_df.apply(lambda row: label_percentile_range(row, explainer_df.describe().to_dict()), axis = 1)

    # Convert "percentile_range_label" column into categorical column
    melted_explainer_df["percentile_range_label"] = pd.Categorical(melted_explainer_df["percentile_range_label"], categories = ["<25%", "25-50%", "50-75%", ">75%"])

    # Get list of unqiue percentile range labels (possibility of at least one of the labels not existing)
    lst_percentile_range_labels = melted_explainer_df["percentile_range_label"].sort_values().unique()

    # Store percentile range labels into SHAP values dataframe
    shap_values_df["percentile_range_label"] = melted_explainer_df["percentile_range_label"]

    # Convert dataframe from wide to long format where feature columns are measured variables and "percentile_range_label" column is identifier variable
    melted_shap_values_df = shap_values_df.melt(value_vars = [col for col in shap_values_df.columns],
                                                id_vars = ["percentile_range_label"],
                                                var_name = "feature",
                                                value_name = "SHAP value")

    # Filter dataframe to specified number of features
    melted_shap_values_df = melted_shap_values_df[melted_shap_values_df["feature"].isin(lst_features[:show_num_features])]

    # Create ordered dictionary to sort beeswarm plot by descending feature importance
    ordered_features_dict = {"feature": lst_features[:show_num_features]}

    # Generate Plotly figure for beeswarm plot
    beeswarm_fig = px.strip(melted_shap_values_df,
                            x = "SHAP value",
                            y = "feature",
                            category_orders = ordered_features_dict,
                            color = "percentile_range_label",
                            color_discrete_map = dict(zip(lst_percentile_range_labels, ["yellow", "orange", "orangered", "darkred"])),
                            orientation = "h",
                            stripmode = "overlay",
                            height = 1050,
                            title = f"Bee Swarm Plot of SHAP Values by Feature ({len(lst_features[:show_num_features])} features shown)")
    
    # Add titles for X- and Y-axes of figure
    beeswarm_fig.update_layout(legend_title_text = "Feature value's<br>percentile range",
                               xaxis_title = 'SHAP Value (Impact on Model Output)',
                               yaxis_title = 'Feature',
                               yaxis = {"showgrid": True},
                               template = "plotly_dark" if dark_mode else "plotly_white"
                               )

    return beeswarm_fig
