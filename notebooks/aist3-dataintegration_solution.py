import marimo

__generated_with = "0.13.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import seaborn as sns
    return mo, pd, sns


@app.cell
def _(pd):
    pokemon = pd.read_csv("https://gist.githubusercontent.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6/raw/92200bc0a673d5ce2110aaad4544ed6c4010f687/pokemon.csv")
    return (pokemon,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # Exploring and Aggregating Data

    The first step in any data project is to **understand the raw dataset** — view it, inspect data types, and check for missing or inconsistent values.

    The `mo.ui.dataframe()` widget helps by rendering a scrollable, filterable view of the full dataset. This is great for manual inspection and exploration.

    In practice, however, data rarely stays in its raw form. It often goes through **ETL (Extract, Transform, Load)** steps such as:

    - Filtering rows
    - Renaming or converting columns
    - Grouping and aggregating values
    - Sampling or reshaping tables

    These operations are all **available in Marimo’s UI**, as shown in tools like:

    - `Group By`
    - `Aggregate`
    - `Filter Rows`
    - `Column Conversion`

    While this interface is highly useful during exploration and prototyping, **production-grade pipelines** rely on **explicit code or SQL** — ensuring reproducibility, version control, and auditability.
    """
    )
    return


@app.cell
def _(mo, pokemon):
    mo.ui.dataframe(pokemon)
    return


@app.cell
def _(mo, pokemon):
    aggregatedTypeLegend = mo.sql(
        f"""
        SELECT "Type 1", AVG(HP) from pokemon
        GROUP BY "Type 1", Legendary
        """
    )
    return (aggregatedTypeLegend,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ## Your Turn!
    ### Task 1 — Count Pokémon per Type

    Write a SQL query that counts how many Pokémon belong to each `"Type 1"`. Your output should contain two columns:

    - `Type 1`: the primary type (e.g., Fire, Water, etc.)
    - `Count`: the number of Pokémon in that type

    Order the results by `Count` in descending order.
    """
    )
    return


@app.cell
def _(mo):
    task1 = mo.sql(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ### Task 2 — Highest Average Defense (Non-Legendary Only)

    Write a SQL query that computes the **average `"Defense"`** for each `"Type 1"` among **non-legendary Pokémon** only (`Legendary = FALSE`).

    Your output should contain:

    - `Type 1`
    - `Average_Defense`

    Then, sort the result in descending order and **limit it to the top 5 types** with the highest average defense.

    **Bonus**: Can you rewrite the query to return *only the single type with the highest average defense*?
    """
    )
    return


@app.cell
def _(mo):
    task2 = mo.sql(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ### Task 3 — Top Defense Pokémon by Type

    Write a SQL query that returns the **single Pokémon with the highest Defense** for each `"Type 1"`.

    Your result should include:

    - `"Type 1"`
    - `"Name"`
    - `"Defense"`

    If there are ties (multiple Pokémon with the same highest Defense in a type), any one of them can be returned.
    """
    )
    return


@app.cell
def _(mo):
    task3 = mo.sql(
        f"""
        -- Your query here
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # Aesthetic Mapping in Visualizations

    Aesthetic mapping is a core concept in data visualization. It refers to how variables in your dataset are visually encoded — deciding what appears on each axis, how categories are colored, and how data is broken down into groups.

    Common aesthetic dimensions include:

    - **x-axis**: A numeric or categorical variable shown horizontally
    - **y-axis**: A numeric or categorical variable shown vertically
    - **color (hue)**: Used to distinguish categories by color
    - **size**: Can be used to represent magnitude (e.g., HP or Speed)
    - **shape**: Useful for additional categorical distinctions
    - **facets or panels**: Enable side-by-side comparisons across subsets

    Whether working through a point-and-click interface or writing code, this mapping process is fundamental:

    - In interactive tools, you assign variables to visual dimensions using dropdowns or drag-and-drop.
    - In code (e.g., `sns.scatterplot(...)`), you explicitly define these mappings via parameters like `x`, `y`, `hue`, or `size`.

    Understanding aesthetic mapping helps you:

    - Design plots that answer specific questions
    - Make multidimensional patterns easier to recognize
    - Maintain visual clarity and analytical relevance

    It's not about making data look good — it's about making relationships and differences in the data **visible and meaningful**.
    """
    )
    return


@app.cell
def _(mo, pokemon):
    mo.ui.data_explorer(pokemon)
    return


@app.cell
def _(pokemon, sns):
    sns.scatterplot(pokemon, x="Attack", y="Defense", hue="Type 1")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # Scatter Plot

    ## Aesthetic Mapping
    - **x-axis**: Continuous variable
    - **y-axis**: Continuous variable
    - **hue**: Categorical variable (optional)
    - **size**: Continuous variable (optional)
    - **style**: Categorical variable (optional)

    ## Usage Scenario
    Scatter plots are used to visualize the relationship between two continuous variables. They are particularly useful for identifying correlations, clusters, and outliers. By adding a hue, size, or style, you can introduce additional dimensions to the plot, allowing for more complex data exploration. Scatter plots are commonly used in exploratory data analysis to understand the relationships and patterns in the data.
    """
    )
    return


@app.cell
def _(pokemon, sns):
    import matplotlib.pyplot as plt

    # Scatter plot of Attack vs Defense
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=pokemon, x="Attack", y="Defense", hue="Type 1", alpha=0.7)
    plt.title("Scatter Plot of Attack vs Defense")
    plt.xlabel("Attack")
    plt.ylabel("Defense")
    plt.gca()
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # Bar Plot

    ## Aesthetic Mapping
    - **x-axis**: Categorical variable
    - **y-axis**: Continuous variable (usually an aggregate like mean or sum)
    - **hue**: Categorical variable (optional)

    ## Usage Scenario
    Bar plots are ideal for comparing quantities across different categories. They are often used to display the distribution of categorical data or to compare the sizes of different groups. Bar plots can be used to show counts, sums, or averages, making them versatile for summarizing data. They are particularly useful in business and social sciences for comparing different groups or tracking changes over time.
    """
    )
    return


@app.cell
def _(aggregatedTypeLegend, plt, sns):
    # Bar plot of average HP by Type 1
    plt.figure(figsize=(10, 6))
    sns.barplot(data=aggregatedTypeLegend, x="Type 1", y="avg(HP)")
    plt.title("Average HP by Type 1")
    plt.xlabel("Type 1")
    plt.ylabel("Average HP")
    plt.xticks(rotation=45)
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # Box Plot

    ## Aesthetic Mapping
    - **x-axis**: Categorical variable
    - **y-axis**: Continuous variable
    - **hue**: Categorical variable (optional)

    ## Usage Scenario
    Box plots are used to display the distribution of data based on a five-number summary: minimum, first quartile, median, third quartile, and maximum. They are excellent for identifying outliers and understanding the spread and skewness of the data. Box plots are commonly used in statistical analysis to compare distributions across different groups or categories.
    """
    )
    return


@app.cell
def _(plt, pokemon, sns):
    # Box plot of Attack by Type 1
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=pokemon, x="Type 1", y="Attack")
    plt.title("Box Plot of Attack by Type 1")
    plt.xlabel("Type 1")
    plt.ylabel("Attack")
    plt.xticks(rotation=45)
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # Histogram

    ## Aesthetic Mapping
    - **x-axis**: Continuous variable
    - **y-axis**: Frequency or count

    ## Usage Scenario
    Histograms are used to visualize the distribution of a single continuous variable. They show the frequency of data points within specified ranges (bins). Histograms are useful for understanding the shape of the data distribution, such as whether it is normal, skewed, or has multiple modes. They are widely used in data analysis to assess the underlying distribution of data and to identify patterns or anomalies.
    """
    )
    return


@app.cell
def _(plt, pokemon, sns):
    # Histogram of Speed
    plt.figure(figsize=(8, 6))
    sns.histplot(pokemon["Speed"], bins=20, kde=True)
    plt.title("Histogram of Speed")
    plt.xlabel("Speed")
    plt.ylabel("Frequency")
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # Violin Plot

    ## Aesthetic Mapping
    - **x-axis**: Categorical variable
    - **y-axis**: Continuous variable
    - **hue**: Categorical variable (optional)

    ## Usage Scenario
    Violin plots combine the features of box plots and KDE (kernel density estimation) to show the distribution of a continuous variable across categories. They provide insight into the probability density of the data at different values, while still showing median and quartile information. Violin plots are particularly useful when comparing the distribution shape between several groups and when you want to visualize multimodality or skewness.
    """
    )
    return


@app.cell
def _(plt, pokemon, sns):
    # Violin plot of Speed by Type 1
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=pokemon, x="Type 1", y="Speed", inner="box")
    plt.title("Violin Plot of Speed by Type 1")
    plt.xlabel("Type 1")
    plt.ylabel("Speed")
    plt.xticks(rotation=45)
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # Swarm Plot

    ## Aesthetic Mapping
    - **x-axis**: Categorical variable
    - **y-axis**: Continuous variable
    - **hue**: Categorical variable (optional)

    ## Usage Scenario
    Swarm plots show all data points and are ideal for visualizing the distribution and density of a dataset within categories. Unlike box plots or violin plots, swarm plots avoid overlap by adjusting the position of points along the categorical axis. This makes them especially useful for small-to-moderate sized datasets where individual observations should be visible. They are commonly used to compare distributions across groups while preserving individual data visibility.
    """
    )
    return


@app.cell
def _(plt, pokemon, sns):
    # Swarm plot of Speed by Type 1
    plt.figure(figsize=(12, 6))
    sns.swarmplot(data=pokemon, x="Type 1", y="Speed", size=3)
    plt.title("Swarm Plot of Speed by Type 1")
    plt.xlabel("Type 1")
    plt.ylabel("Speed")
    plt.xticks(rotation=45)
    plt.gca()
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ### Exam Task – NBA Player Stats Visualization (2 points)

    In the lecture, we discussed how graphs and color palettes should reflect the underlying data types.

    Using the dataset below (NBA player positions and shooting stats), create a suitable plot to visually compare players.
    """
    )
    return


@app.cell(hide_code=True)
def _(pd):
    import numpy as np

    np.random.seed(42)

    positions = ['PG', 'SG', 'SF', 'PF', 'C']
    players = [f"Player {i+1}" for i in range(20)]

    mock_nba = pd.DataFrame({
        "Name": players,
        "Position": np.random.choice(positions, size=20),
        "Pts_per_Game": np.round(np.random.normal(loc=20, scale=5, size=20), 1),
        "Field_Goal_Pct": np.round(np.random.normal(loc=45, scale=5, size=20), 1),
        "Games_Played": np.random.randint(50, 82, size=20)
    })

    mock_nba["Pts_per_Game"] = mock_nba["Pts_per_Game"].clip(lower=5)
    mock_nba["Field_Goal_Pct"] = mock_nba["Field_Goal_Pct"].clip(lower=35, upper=60)

    mock_nba
    return mock_nba, np


@app.cell
def _(mock_nba, plt, sns):
    plt.figure()
    sns.scatterplot(
        data=mock_nba,
        x="Field_Goal_Pct",
        y="Pts_per_Game",
        size="Games_Played",
        hue="Position"
    )
    plt.xlabel("Field Goal Percentage")
    plt.ylabel("Points per Game")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ### Exam Task – Bundesliga Passing Distributions (1 point)

    The table below provides the number of **played passes per matchday** for all 18 Bundesliga teams over a single season (34 matchdays).

    Create a plot that shows the **distribution of passes per team** across the season.
    """
    )
    return


@app.cell(hide_code=True)
def _(np, pd):

    np.random.seed(123)

    teams = [
        "Bayern München", "Borussia Dortmund", "RB Leipzig", "Union Berlin", "SC Freiburg",
        "Eintracht Frankfurt", "VfL Wolfsburg", "Bayer Leverkusen", "Mainz 05", "Borussia M'gladbach",
        "FC Köln", "TSG Hoffenheim", "Werder Bremen", "FC Augsburg", "VfB Stuttgart",
        "Hertha BSC", "Schalke 04", "Bochum"
    ]
    matchdays = list(range(1, 35))

    data = []
    for team in teams:
        passes = np.random.normal(loc=600, scale=80, size=34).round().astype(int)
        for matchday, count in zip(matchdays, passes):
            data.append({
                "Team": team,
                "Matchday": matchday,
                "Passes": max(count, 300)  # prevent unrealistic low values
            })

    bundesliga_passes = pd.DataFrame(data)
    bundesliga_passes
    return


@app.cell
def _(mock_nba, plt, sns):
    plt.figure()
    sns.scatterplot(
        data=mock_nba,
        x="Field_Goal_Pct",
        y="Pts_per_Game",
        size="Games_Played",
        hue="Position"
    )
    plt.xlabel("Field Goal Percentage")
    plt.ylabel("Points per Game")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
