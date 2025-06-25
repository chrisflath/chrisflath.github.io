import marimo

__generated_with = "0.13.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    from drawdata import ScatterWidget
    import pandas as pd
    import seaborn as sns
    return (
        KNeighborsClassifier,
        LogisticRegression,
        ScatterWidget,
        accuracy_score,
        mo,
        np,
        pd,
        plt,
        sns,
        precision_score,
        recall_score,
        f1_score,
    )


@app.cell
def _(mo):
    mo.vstack([
        mo.md("# Classification"),
        mo.md("## Data Generation")
    ])
    algorithm = mo.ui.radio(options=["Logistic Regression", "k-NN"], value="Logistic Regression", label="Algorithm")
    return (algorithm,)


@app.cell
def _(algorithm, mo):
    C = mo.ui.slider(0.01, 10.0, value=1.0, label="Regularization (C)", disabled=(algorithm.value!="Logistic Regression"))
    n_neighbors = mo.ui.slider(1, 20, value=5, label="Number of neighbors (k)", disabled=(algorithm.value!="k-NN"))
    return C, n_neighbors


@app.cell
def _(ScatterWidget, mo):
    # Create ScatterWidget with 4 colors
    run_button = mo.ui.run_button(label="Process data and create plot")
    scatter_widget = ScatterWidget(classes=4)
    mo.vstack([
        mo.md(r"""
        **Instructions:**  

        - colors 1&2 = Training data
        - colors 3&4 = Test data
        - colors 1&3 = Class A
        - colors 2&4 = Class B
        """),
        scatter_widget
    ])
    return run_button, scatter_widget


@app.cell
def _(C, algorithm, mo, n_neighbors, run_button):
    # Layout
    mo.vstack([
        mo.md("## Logistic Regression and k-Nearest Neighbors"),
        algorithm,
        C,
        n_neighbors,
        run_button
    ])
    return


@app.cell
def _(
    C,
    KNeighborsClassifier,
    LogisticRegression,
    accuracy_score,
    algorithm,
    mo,
    n_neighbors,
    pd,
    run_button,
    scatter_widget,
    precision_score,
    recall_score,
    f1_score,
):
    combined_df = {}
    mo.stop(not run_button.value)
    df = pd.DataFrame(scatter_widget.data_as_pandas)

    # Map colors to classes and data types
    # Colors a,c -> Class 0, Colors b,d -> Class 1
    # Colors a,b -> Training, Colors c,d -> Test
    color_to_class = {'a': 0, 'b': 1, 'c': 0, 'd': 1}  # Color a&c = Class A (0), Color b&d = Class B (1)
    color_to_data_type = {'a': 'train', 'b': 'train', 'c': 'test', 'd': 'test'}  # Colors a&b = train, Colors c&d = test

    # Convert color indices (which are 0-based) to class labels and data types
    df['class_label'] = df['label'].map(color_to_class)
    df['data_type'] = df['label'].map(color_to_data_type)

    # Check if we have both training and test data
    if 'train' not in df['data_type'].values:
        mo.stop("Please add training data using colors 1 and 2.")
    if 'test' not in df['data_type'].values:
        mo.stop("Please add test data using colors 3 and 4.")

    # Separate training and test data
    train_data = df[df['data_type'] == 'train']
    test_data = df[df['data_type'] == 'test']

    X_train = train_data[['x', 'y']].values
    y_train = train_data['class_label'].values
    X_test = test_data[['x', 'y']].values
    y_test = test_data['class_label'].values

    # Train the model
    if algorithm.value == "Logistic Regression":
        model = LogisticRegression(C=C.value, solver='liblinear', multi_class='ovr', random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    elif algorithm.value == "k-NN":
        model = KNeighborsClassifier(n_neighbors=n_neighbors.value)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

    # Create DataFrames for training and test data
    train_df = pd.DataFrame(X_train, columns=['x', 'y'])
    train_df['true_label'] = y_train
    train_df['predicted_label'] = model.predict(X_train)  # Predictions for training data
    train_df['data_type'] = 'train'
    train_df['original_color'] = train_data['color'].values

    test_df = pd.DataFrame(X_test, columns=['x', 'y'])
    test_df['true_label'] = y_test
    test_df['predicted_label'] = y_pred
    test_df['data_type'] = 'test'
    test_df['original_color'] = test_data['color'].values

    # Combine the DataFrames
    combined_df = pd.concat([train_df, test_df], ignore_index=True)

    # Calculate performance metrics on the test set
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Display metrics as cards
    mo.vstack([
        mo.md("### Performance Metrics (on Test Set)"),
        mo.hstack([
            mo.stat(label="Accuracy", value=f"{accuracy:.3f}", ),
            mo.stat(label="Precision (Class A)", value=f"{precision:.3f}"),
            mo.stat(label="Recall (Class A)", value=f"{recall:.3f}"),
            mo.stat(label="F1-Score (Class A)", value=f"{f1:.3f}")
        ], justify="space-around")
    ])
    return combined_df, model


@app.cell
def _(combined_df, model, np, plt, sns):
    plt.figure(figsize=(18, 5))

    # Plot 1: Original colors
    plt.subplot(1, 3, 1)
    sns.scatterplot(
        data=combined_df,
        x='x',
        y='y',
        hue='original_color',
        style='data_type',
        markers={'train': 'o', 'test': 'X'},
        s=100,
        alpha=0.7,
        palette=['blue', 'orange', 'green', 'red'],
        legend=False  # Remove legend for this specific plot
    )
    plt.title('Data by Original Colors')
    plt.xlabel('Feature 1 (x)')
    plt.ylabel('Feature 2 (y)')
    # plt.legend(title='Color/Type')
    plt.grid(True, alpha=0.3)

    # Plot 2: True classes
    plt.subplot(1, 3, 2)
    sns.scatterplot(
        data=combined_df,
        x='x',
        y='y',
        hue='true_label',
        style='data_type',
        markers={'train': 'o', 'test': 'X'},
        s=100,
        palette=['blue', 'red'],
        alpha=0.7
    )
    plt.title('True Classes')
    plt.xlabel('Feature 1 (x)')
    plt.ylabel('Feature 2 (y)')
    plt.legend(title='Class/Type')
    plt.grid(True, alpha=0.3)

    # Plot 3: Predictions vs Reality
    plt.subplot(1, 3, 3)

    # Create a column to identify correct/incorrect predictions
    combined_df['prediction_status'] = combined_df['true_label'] == combined_df['predicted_label']

    # Plot training data
    sns.scatterplot(
        data=combined_df[combined_df['data_type'] == 'train'],
        x='x',
        y='y',
        hue='true_label',
        palette=['blue', 'red'],
        marker='o',
        s=100,
        alpha=0.7,
    )

    # Plot correct test predictions
    sns.scatterplot(
        data=combined_df[(combined_df['data_type'] == 'test') & (combined_df['prediction_status'] == True)],
        x='x',
        y='y',
        hue='true_label',
        palette=['blue', 'red'],
        marker='X',
        s=100,
        alpha=0.7,
    )

    # Plot incorrect test predictions with different border color
    incorrect_test_data = combined_df[(combined_df['data_type'] == 'test') & (combined_df['prediction_status'] == False)]
    for i, row in incorrect_test_data.iterrows():
        color = 'blue' if row['true_label'] == 0 else 'red'
        edgecolor = 'red' if row['true_label'] == 0 else 'blue'  # Invert color for border
        plt.scatter(row['x'], row['y'], marker='X', s=100, alpha=0.7, c=color, edgecolors=edgecolor, linewidth=1.5, label='Incorrect Prediction')

    plt.title('Predicted Classification')
    plt.xlabel('Feature 1 (x)')
    plt.ylabel('Feature 2 (y)')
    plt.grid(True, alpha=0.3)

    # Add decision boundary
    x_min, x_max = combined_df['x'].min() - 0.1, combined_df['x'].max() + 0.1
    y_min, y_max = combined_df['y'].min() - 0.1, combined_df['y'].max() + 0.1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contour(xx, yy, Z, colors=['green'], linewidths=2, levels=[0.5])

    # Remove duplicate labels
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.tight_layout()
    plt.gca()
    return


if __name__ == "__main__":
    app.run()
