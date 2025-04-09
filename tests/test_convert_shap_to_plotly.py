"""
Unit tests for convert_shap_to_plotly.py
"""
# Standard Library Imports
import os
import sys

# Third-party Imports
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pytest
import shap

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Local Application Imports
from fixtures.convert_shap_to_plotly_data import (
    test_generate_beeswarm_plotly_figure_data,
    test_get_shap_feature_importance_df_data,
    test_get_shap_values_df_data,
    test_label_percentile_range_data
)
from model_card_printer.utils.convert_shap_to_plotly import (
    generate_beeswarm_plotly_figure,
    get_shap_feature_importance_df,
    get_shap_values_df,
    label_percentile_range
)

@pytest.mark.parametrize("test_single_row_shap_values, test_explainer_data", test_get_shap_values_df_data)
def test_get_shap_values_df(test_single_row_shap_values, test_explainer_data):
    """
    Test Case 1: Successfully create SHAP values dataframe.
    """
    # Load test explainer dataset
    df_explainer_test = pd.DataFrame(test_explainer_data)

    # Get feature names
    lst_feature_names = list(df_explainer_test.columns)

    # Create list of SHAP values
    lst_shap_values = [test_single_row_shap_values]*len(df_explainer_test)

    # Create mock prediction results
    lst_prob = [[-0.5, 0.5]*len(df_explainer_test)]

    # Create test SHAP values Explanation object
    test_shap_values = shap.Explanation(values = np.array(lst_shap_values),
                                        base_values = lst_prob,
                                        data = np.array(df_explainer_test),
                                        feature_names = lst_feature_names)

    # Create expected shap values dataframe with feature names as columns
    expected_shap_values_df = pd.DataFrame(test_shap_values[..., 1].values, columns = lst_feature_names)

    # Get actual output
    actual_shap_values_df = get_shap_values_df(test_shap_values, df_explainer_test)

    # Assert dataframes are equal
    pd.testing.assert_frame_equal(expected_shap_values_df, actual_shap_values_df)

@pytest.mark.parametrize("test_inputs, test_output_data", test_get_shap_feature_importance_df_data)
def test_get_shap_feature_importance_df(test_inputs, test_output_data):
    """
    Test Case 1: Successfully create SHAP feature importance dataframe.
    """
    # Get test inputs
    test_single_row_shap_values, test_explainer_data = test_inputs[0]

    # Load test explainer dataset
    df_explainer_test = pd.DataFrame(test_explainer_data)

    # Get feature names
    lst_feature_names = list(df_explainer_test.columns)

    # Create list of SHAP values
    lst_shap_values = [test_single_row_shap_values]*len(df_explainer_test)

    # Mock predicted probabilities results
    lst_proba = [[-0.5, 0.5]*len(df_explainer_test)]

    # Create test SHAP values Explanation object
    test_shap_values = shap.Explanation(values = np.array(lst_shap_values),
                                        base_values = lst_proba,
                                        data = np.array(df_explainer_test),
                                        feature_names = lst_feature_names)

    # Create expected SHAP feature importance dataframe
    expected_shap_importance_df = pd.DataFrame(data = {"feature_name": test_output_data.keys(), "feature_importance_val": test_output_data.values()})

    # Get actual output
    actual_shap_importance_df = get_shap_feature_importance_df(test_shap_values, df_explainer_test)

    # Assert dataframes are equal
    pd.testing.assert_frame_equal(expected_shap_importance_df, actual_shap_importance_df)


@pytest.mark.parametrize("test_inputs, test_output_lst", test_label_percentile_range_data)
def test_label_percentile_range(test_inputs, test_output_lst):
    """
    Test Case 1: Successfully return percentile label.
    """
    # Get test input percentile dictionary
    test_percentile_dict = test_inputs["test_percentile_dict"]

    for index, test_data in enumerate(test_inputs["test_data"]):

        # Create test pd.Series object
        test_series = pd.Series(data = test_data, index = list(test_data.keys()))

        # Get actual output
        actual_output = label_percentile_range(test_series, test_percentile_dict)

        # Assert actual output is same as expected output
        assert actual_output == test_output_lst[index]

@pytest.mark.parametrize("test_inputs", test_generate_beeswarm_plotly_figure_data)
def test_generate_beeswarm_plotly_figure(test_inputs):
    """
    Test Case 1: Successfully generate beeswarm plot.
    """
    # Get test inputs
    test_single_row_shap_values, test_explainer_data = test_inputs

    # Load test explainer dataset
    df_explainer_test = pd.DataFrame(test_explainer_data)

    # Get feature names
    lst_feature_names = list(df_explainer_test.columns)

    # Create list of SHAP values
    lst_shap_values = [test_single_row_shap_values]*len(df_explainer_test)

    # Mock predicted probabilities results
    lst_proba = [[-0.5, 0.5]*len(df_explainer_test)]

    # Create test SHAP values Explanation object
    test_shap_values = shap.Explanation(values = np.array(lst_shap_values),
                                        base_values = lst_proba,
                                        data = np.array(df_explainer_test),
                                        feature_names = lst_feature_names)

    # Get actual output figure
    actual_fig = generate_beeswarm_plotly_figure(test_shap_values,
                                                 df_explainer_test,
                                                 show_num_features = len(df_explainer_test.columns),
                                                 dark_mode = True)

    # Assert output figure is a Plotly figure
    assert isinstance(actual_fig, go.Figure)

    # Assert figure layout is correct
    assert set(actual_fig.layout.yaxis.categoryarray) == set(df_explainer_test.columns)
    assert list(actual_fig.layout.xaxis.domain) == [0, 1]
    assert actual_fig.layout.boxmode == "overlay"
