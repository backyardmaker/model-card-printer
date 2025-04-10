# Model Card Printer
The Model Card Printer simplifies the generation of model cards for machine learning models. Model Card Printer offers a standardized and structured approach to documenting machine learning models, while still providing flexibility for users to customize the document without being overly restrictive.

- Works with popular data visualization libraries such as `Pandas` and `Plotly`.
- Supports all text-based documentation in Markdown format.
- Tailor your model card to fit your needs and preferences.
- Supports exporting model cards in JSON, Pickle, and HTML formats.

# Installation
Model Card Printer is available as a PyPI package. Install it using pip package manager:
```bash
pip install model-card-printer
```
# Quickstart
### 1. Create documentation and data visualizations
Note: All visualizations generated here are for demonstration purposes. You could use `Pandas` to create your visualizations as well.
```python
import plotly.express as px

# Create documentation (markdown format)
documentation_standalone = "# Model Card Demo\nHere is a paragraph related to the documentation.\n## Considerations\nThis demonstration is for anyone that wants to quickly start generating model cards with their trained ML models."

# Create data visualizations and related documentation
df = px.data.tips()
fig1 = px.box(df, y="total_bill")
fig2 = px.histogram(df, x="total_bill", color="sex", marginal="rug",
                         hover_data=df.columns)
fig3 = px.density_heatmap(df, x="total_bill", y="tip")

documentation_for_visuals = "# Quantitative Analysis\nThe visualizations presented are for demonstration purposes only."

# Create standalone data visualizations
df = px.data.iris()
fig_standalone = px.scatter_matrix(df,
    dimensions=["sepal_length", "sepal_width", "petal_length", "petal_width"],
    color="species", symbol="species",
    title="Scatter matrix of iris data set",
    labels={col:col.replace('_', ' ') for col in df.columns})
fig_standalone.update_traces(diagonal_visible=False)
```

### 2. Create model card
```python
from model_card_printer import ModelCardPrinter

# Generate an empty model card
model_card = ModelCardPrinter.generate_card()

# Store all the information
model_card.add_custom_documentation(documentation_standalone, document_name = 'demo')
model_card.add_custom_visualization_collection({"demo fig 1": fig1, "demo fig 2": fig2, "demo fig 3": fig3},
                                               documentation = documentation_for_visuals,
                                               collection_name = "Demo visuals and text")
model_card.add_individual_custom_visualization(fig_standalone, "demo standalone fig")

# Save model card as HTML (default dark mode, else add parameter "is_dark_mode = False")
model_card.write_html("demo_model_card.html")
```

# Model Card Export Formats
1. Output as JSON
```python
# Saving to JSON file
model_card.write_json("model_card.json")

# OPTIONAL: Intermediate output
model_card_json = model_card.to_json()
```

2. Output as HTML
```python
# Saving to HTML file
model_card.write_html("model_card.html")

# OPTIONAL: Intermediate output
model_card_html = model_card.to_html()
```

3. Output as Pickle object (not recommended unless there is a need to store the datasets inside the model card)
```python
import pickle

with open('model_card.pkl', 'wb') as file:
    pickle.dump(model_card, file)
```

# Model Card Import Formats
1. Load from JSON file
```python
model_card = ModelCardPrinter(file_path = "model_card.json").load_from_json()
```

2. Load from Python dictionary
```python
dict_model_card = previous_model_card.to_dict()
model_card = ModelCardPrinter(data_dict = dict_model_card).load_from_dict()
```

# Tutorials
For more in-depth demonstrations on `model-card-printer` package, refer to the provided [examples](https://github.com/backyardmaker/model-card-printer/tree/main/examples).

- [Creating a model card using the Breast Cancer dataset](https://github.com/backyardmaker/model-card-printer/blob/main/examples/breast_cancer_prediction.ipynb)
- [Create a custom model card](https://github.com/backyardmaker/model-card-printer/blob/main/examples/custom_model_card.ipynb)