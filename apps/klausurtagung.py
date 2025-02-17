import marimo

__generated_with = "0.11.5"
app = marimo.App(
    width="full",
    app_title="Intro to Marimo Notebooks",
    layout_file="layouts/klausurtagung.slides.json",
)


@app.cell
def _():
    import marimo as mo
    import datetime as dt
    import pandas as pd
    import polars as pl
    import time
    import pyarrow
    import duckdb
    import sqlglot
    #from lets_plot import ggplot, geom_line, geom_bar, aes, scale_color_manual, theme, element_text, element_blank, element_line, element_rect, element_blank, as_discrete, coord_flip, theme, geom_text, layer_tooltips
    import numpy as np
    from scipy.optimize import milp, LinearConstraint
    import altair as alt
    return (
        LinearConstraint,
        alt,
        dt,
        duckdb,
        milp,
        mo,
        np,
        pd,
        pl,
        pyarrow,
        sqlglot,
        time,
    )


@app.cell
def _():
    import requests

    # URL of the dataset (must allow direct downloads)
    url = "https://raw.githubusercontent.com/WIBA-DMA/exam-2024-pprm/refs/heads/main/train.csv"

    # Download and save the file
    filename = "train.csv"

    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download, status: {response.status_code}")
    return file, filename, requests, response, url


@app.cell
def _(mo):
    class SlideCreator:
        def __init__(self, chair_title="Default Chair Title", lecture_name="Default Lecture Name"):
            self.chair_title = chair_title
            self.lecture_name = lecture_name
            self.vertical_spacer_height = 800
            self.horizontal_spacer_width = 1280
            self.logo = mo.image("https://raw.githubusercontent.com/d3group/.github/refs/heads/main/assets/D3_2c.png", width=200)

        def get_spacer_horizontal(self, size=1200):
            return mo.md(r"""&nbsp;""").style({"width": f"{size}px"})

        def get_spacer_vertical(self, size=600):
            return mo.md(r"""&nbsp;""").style({"height": f"{size}px"})

        def get_horizontal_rule(self):
            return mo.md(f"<div style='width: {self.horizontal_spacer_width}px; height: 1px; background-color: darkgray;'></div>")

        def get_footer(self):
            return mo.vstack([
                self.get_horizontal_rule(),
                mo.hstack([
                    mo.vstack([
                        mo.md(f"_{self.chair_title}_"),
                        mo.md(f"_{self.lecture_name}_")
                    ], gap=0, justify="start"),
                    self.logo
                ])
            ])

        def create_slide(self, slide_data, layout_type="2-column", left_width=750, right_width=450):   
            if layout_type == "title-slide":
                if slide_data.get("content2") is None:
                    slide_data["content2"] = mo.md("")
                slide = mo.vstack([
                    self.get_spacer_horizontal(),
                    self.get_horizontal_rule(),
                    self.get_spacer_vertical(100),
                    mo.hstack([
                        mo.md("""<div style='width: 4px; height: 300px; background-color: darkgray;'></div>"""),
                        mo.vstack([mo.md(f"# {slide_data['title']}").style({"text-align": "left"}),
                        mo.hstack([
                        mo.vstack([
                            mo.md(f"### {slide_data['presenter']}").style({"text-align": "left"}),
                            mo.md(f"_{self.chair_title}_").style({"text-align": "left"})
                        ], align="center"),
                        mo.image("https://raw.githubusercontent.com/d3group/.github/refs/heads/main/assets/D3_2c.png", width=300),
                        slide_data.get("content2")],align="center", gap=1, justify="space-around")], align="center")
                    ], justify="start", align="center", gap=5),
                    self.get_spacer_vertical(100),
                    self.get_horizontal_rule()
                    #self.get_footer()
                ], gap=0, justify="center")
            elif layout_type == "1-column":
                slide = mo.vstack([
                    self.get_spacer_horizontal(),
                    slide_data['title'],
                    self.get_horizontal_rule(),
                    mo.hstack([
                        self.get_spacer_vertical(),
                        slide_data.get("content1").style({"width": "1200px"})
                    ],
                    gap=0,
                    justify="center",
                    align="center"),
                    self.get_footer()
                ], gap=0)
            elif layout_type == "side-by-side":
                slide = mo.vstack([
                    slide_data['title'],
                    self.get_horizontal_rule(),
                    mo.hstack([
                        self.get_spacer_vertical(),
                        slide_data.get("content1").style({"width": "600px", "margin-left": "auto", "margin-right": "auto"}),
                        slide_data.get("content2").style({"width": "600px", "margin-left": "auto", "margin-right": "auto"}),
                    ],
                    gap=0,
                    justify="center",
                    align="center"),
                    self.get_footer()
                ], gap=0, justify="center")
            elif layout_type == "flexible-2-column":
                slide = mo.vstack([
                    slide_data['title'],
                    self.get_horizontal_rule(),
                    mo.hstack([
                        self.get_spacer_vertical(),
                        slide_data.get("content1").style({"width": f"{left_width}px", "margin-left": "auto", "margin-right": "auto"}),
                        slide_data.get("content2").style({"width": f"{right_width}px", "margin-left": "auto", "margin-right": "auto"}),
                    ],
                    gap=0,
                    justify="center",
                    align="center"),
                    self.get_footer()
                ], gap=0, justify="center")
            else:
                slide = mo.vstack([
                    slide_data['title'],
                    self.get_horizontal_rule(),
                    mo.hstack([
                        self.get_spacer_vertical(),
                        slide_data.get("content1").style({"width": "750px", "margin-left": "auto", "margin-right": "auto"}),
                        slide_data.get("content2").style({"width": "450px", "margin-left": "auto", "margin-right": "auto"}),
                    ],
                    gap=0,
                    justify="center",
                    align="center"),
                    self.get_footer()
                ], gap=0, justify="center")

            return slide
    return (SlideCreator,)


@app.cell
def _(mo):
    textInputFootnote = mo.ui.text("Lehrstuhl für Wirtschaftsinformatik & Business Analytics")
    return (textInputFootnote,)


@app.cell
def _(SlideCreator, textInputFootnote):
    slides = {}

    lehrstuhl = textInputFootnote.value
    vorlesung = "An Intro To Marimo Notebooks"

    sc = SlideCreator(lehrstuhl, vorlesung)
    return lehrstuhl, sc, slides, vorlesung


@app.cell
def _(mo, sc, slides):
    slides["title"] = {}
    slides["title"]["presenter"] = "Christoph M. Flath"
    slides["title"]["title"] = mo.md(
        r"""
        # An Intro To Marimo Notebooks
        """
    )
    slides["title"]["content2"] = mo.image("https://docs.marimo.io/_static/marimo-logotype-horizontal.png", width=300)
    sc.create_slide(slides["title"], layout_type="title-slide")
    return


@app.cell
def _(mo, sc, slides):
    slides["intro"] = {}
    slides["intro"]["title"] = mo.md(
        r"""
        # ❤️ Why We Love Jupyter Notebooks
        """
    )

    slides["intro"]["content1"] = mo.md("""
    - **Easy to use**: Write code and see results instantly  
    - **Great for data science**: Pandas, NumPy, and visualization work well  
    - **Flexible**: Supports Python, R, Julia, and more  
    - **Widely adopted**: Used in research, teaching, and industry
    - **Free**: No cost to use or install
      """)

    slides["intro"]["content2"] = mo.image("https://mljar.com/glossary/jupyter-notebook/mljar_everyone_loves_your_work.jpeg")

    sc.create_slide(slides["intro"], layout_type="side-by-side")
    return


@app.cell
def _(mo, sc, slides):
    slides["issues"] = {}

    slides["issues"]["title"] = mo.md(
        r"""
        # 😬 But… Not Everything is Perfect
        """)

    slides["issues"]["content1"] = mo.md(
        r"""

    ### Common Frustrations with Jupyter:

    ❌ **Hidden state issues**: Running cells out of order breaks things  
    ❌ **Manual updates**: Change a variable → Manually re-run all dependent cells  
    ❌ **Interactivity is clunky**: Requires external libraries (ipywidgets, Voila)  
    ❌ **Difficult deployment**: Sharing notebooks often leads to dependency nightmares  

    🤔 What if there was a **better way**?

        """
    )

    slides["issues"]["content2"] = mo.image("https://user-images.githubusercontent.com/9068012/103839742-f26a8f00-5044-11eb-8f5c-b845efb2959b.png")

    sc.create_slide(slides["issues"], layout_type="side-by-side")
    return


@app.cell
def _(mo, sc, slides):
    slides["marimo"] = {}
    slides["marimo"]["title"] =  mo.md(r"""
        # 🔍 Introducing Marimo

    """)
    slides["marimo"]["content1"] = mo.md(r"""

    - **A reactive programming environment for Python**  
    - Combines the best of **Jupyter + ObservableHQ**  
    - **Automatic updates** when variables change  
    - **Built-in UI components** for interactivity  
    - **Lightweight and shareable**
    """)

    slides["marimo"]["content2"] = mo.image("https://docs.marimo.io/_static/marimo-logotype-thick.svg")


    sc.create_slide(slides["marimo"], layout_type="side-by-side")
    return


@app.cell
def _(mo, sc, slides):
    slides["features"] = {}
    slides["features"]["title"] =  mo.md(r"""
        # 🏗️ Core Features of Marimo
    """)
    slides["features"]["content1"] = mo.md(r"""



    ✅ **Reactive Execution** – Cells update automatically  
    ✅ **Live UI Components** – Sliders, buttons, forms, and more  
    ✅ **State Consistency** – No hidden execution order issues  
    ✅ **Fast & Lightweight** – No need for extra libraries  

    """)

    slides["features"]["content2"] = mo.vstack([mo.image("https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/outputs.gif"),
                                                mo.image("https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/readme-ui.gif")])


    sc.create_slide(slides["features"], layout_type="side-by-side")
    return


@app.cell
def _(mo):
    x = mo.ui.slider(1, 10, value=5, label="$X_t$", step=1, show_value=True)
    xhat = mo.ui.slider(1, 10, value=1, label="$X_{t-1}$", step=1, show_value=True)
    y = mo.ui.radio(['neutral', 'warn', 'success', 'info', 'danger'], label="Type", value="info", inline=True)
    return x, xhat, y


@app.cell
def _(mo, sc, slides, x, xhat, y):
    Delta = (x.value - xhat.value) / x.value

    slides["Reactive"] = {}
    slides["Reactive"]["title"] = mo.md(
        r"""
        # 🔄 Reactive Execution in Action
        """
    )

    slides["Reactive"]["content1"] = mo.md(r"""

    - **Jupyter:** Run a cell → Change a variable → Manually re-run dependent cells  
    - **Marimo:** Change a variable → **Everything updates instantly**  

    """
    )

    display1 = mo.callout(f"Current value: {x.value}", kind=str(y.value))
    display2 = mo.stat(
        label="Value",
        bordered=True,
        value=f"{x.value}",
        caption=f"{Delta:.0%}",
        direction="increase" if Delta > 0 else "decrease",
    )

    slides["Reactive"]["content2"] = mo.vstack([mo.hstack([x,xhat]), y, display1, display2])

    sc.create_slide(slides["Reactive"])
    return Delta, display1, display2


@app.cell
def _(mo, sc, slides):
    slides["UICode"] = {}
    slides["UICode"]["title"] = mo.md(
        r"""
        # 🎨 Code for Example
        """
    )

    slides["UICode"]["content1"] = mo.md("""
    ```python
    import marimo as mo

    # backend code (eleement definition)
    x = mo.ui.slider(1, 10, value=5, label="$X_t$", step=1, show_value=True)
    xhat = mo.ui.slider(1, 10, value=1, label="$X_{t-1}$", step=1, show_value=True)
    y = mo.ui.radio(['neutral', 'warn', 'success', 'info', 'danger'],
    label="Type", value="info", inline=True)
    display1 = mo.callout(f"Current value: {x.value}", kind=str(y.value))
    display2 = mo.stat(
        label="Value",
        bordered=True,
        value=f"{x.value}",
        caption=f"{Delta:.0%}",
        direction="increase" if Delta > 0 else "decrease",
    )]

    # frontend code (rendering)
    mo.vstack([mo.hstack([x,xhat]), y, display1, display2])
    ```
    """)
    slides["UICode"]["content2"] = mo.image("https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/outputs.gif")

    sc.create_slide(slides["UICode"], layout_type="1-column")
    return


@app.cell
def _(mo):
    toggle = mo.ui.switch(value=False, label="Toggle Visibility")
    return (toggle,)


@app.cell
def _(toggle):
    toggleLable = ""
    if toggle.value:
        toggleLable = "Toggled!"
    else:
        toggleLable = ""
    return (toggleLable,)


@app.cell
def _(mo, sc, slides, toggle, toggleLable):
    slides["UI"] = {}
    slides["UI"]["title"] = mo.md(
        r"""
        # 🎨 UI Components Made Easy
        """
    )

    slides["UI"]["content1"] = mo.md(
        r"""
    No need for **ipywidgets**, just use Marimo’s built-in elements:

    - ✅ Sliders
    - ✅ Buttons
    - ✅ Text Inputs
    - ✅ Tabs
    - ✅ File Uploads
    - ✅ And more!

        """
    )
    slides["UI"]["content2"] = mo.vstack([mo.ui.slider(1, 10, value=5, label="$X_t$", step=1, show_value=True),
                                          mo.md("---"),
                                          toggle,
                                          mo.md(f"{toggleLable}"),
                                          mo.md("---"),
                                          mo.ui.text("Type something..."),
                                          mo.md("---"),
                                          mo.ui.tabs({"Tab 1": "My cool content from tab 1", "Tab 2": "My even cooler content from tab 2"}),
                                          mo.md("---"),
                                          mo.ui.file()])

    sc.create_slide(slides["UI"])
    return


@app.cell
def _(mo, sc, slides, textInputFootnote):
    slides["state"] = {}

    slides["state"]["title"] = mo.md(
        r"""
        # 🚀 State Management: No More Hidden State
        """
    )

    slides["state"]["content1"] = mo.md(
        r"""
    * Jupyter: The execution order matters!
    * Marimo: Every variable is automatically tracked

    ```python
    a = mo.ui.textbox("Enter text")
    mo.md(f"You typed: {a.value}")
    ```

        """
    )

    slides["state"]["content2"] = textInputFootnote


    sc.create_slide(slides["state"])
    return


@app.cell
def _(mo):
    diagram2 = '''graph TD;
        A[Start] --> B{Decision?};
        B -->|Yes| C[Do Task];
        B -->|No| D[End];
        C --> D;'''
    diagramEditor = mo.ui.text_area(diagram2, label="Mermaid Diagram", full_width=True, rows=10)
    return diagram2, diagramEditor


@app.cell
def _(diagramEditor, mo, sc, slides):
    slides["mermaid"] = {}
    slides["mermaid"]["content1"] = mo.vstack([mo.md(r"""
    ## 📊 Mermaid Integration in Marimo
    ✅ Supports flowcharts, sequence diagrams, Gantt charts, and more  
    ✅ No extra libraries needed—just use `mo.mermaid()`"""),diagramEditor]
                                               )
    slides["mermaid"]["content2"] = mo.mermaid(diagramEditor.value).style({"margin-left": "100px", "margin-right": "auto"})
    slides["mermaid"]["title"] = mo.md(f"# 📌 Marimo + Mermaid: Diagrams Made Easy")


    sc.create_slide(slides["mermaid"])
    return


@app.cell
def _(mo, run_sql_query):
    # SQL Query Editor
    queryEditorSQL = mo.ui.text_area(label="Enter SQL Query", value="SELECT * FROM 'train.csv';", full_width=True)
    executeButtonSQL = mo.ui.button(label="Run Query", on_click=lambda value: run_sql_query(), value="")
    return executeButtonSQL, queryEditorSQL


@app.cell
def _(executeButtonSQL, mo, queryEditorSQL, sc, slides):
    slides["sql_query"] = {}

    queryResult = mo.sql(queryEditorSQL.value)

    slides["sql_query"]["content1"] = mo.vstack([
        mo.md(r"""

        ✅ Enter an SQL query in the text box below

        ✅ Click the "Run Query" button to execute

        ✅ See the results rendered instantly

        ---
        """),
        queryEditorSQL,
        executeButtonSQL
    ])

    slides["sql_query"]["content2"] = mo.as_html(queryResult)
    slides["sql_query"]["title"] = mo.md(f"# 🗄️ SQL Query Execution in Marimo")

    sc.create_slide(slides["sql_query"], layout_type="side-by-side")
    return (queryResult,)


@app.cell
def _(mo):
    dates = mo.sql(
        f"""
        SELECT date from 'train.csv'
        """,
        output=False
    )
    return (dates,)


@app.cell
def _(dates, mo):
    datePicker = mo.ui.date_range.from_series(dates["date"], label="Date Range", value=[dates["date"].min(), dates["date"].max()])
    return (datePicker,)


@app.cell
def _(datePicker, mo):
    filtered = mo.sql(
        f"""
        SELECT * FROM 'train.csv' WHERE date BETWEEN '{str(datePicker.value[0])}' AND '{str(datePicker.value[1])}'
        """,
        output=False,
    )
    return (filtered,)


@app.cell
def _(filtered, mo):
    timeseries = mo.sql(
        f"""
        SELECT date, streetname, CAST(SUM(n_pedestrians) AS INT) AS count FROM filtered GROUP BY streetname, date
        """,
        output=False,
    )
    return (timeseries,)


@app.cell
def _(filtered, mo):
    summedData = mo.sql(
        f"""
        SELECT date, CAST(SUM(n_pedestrians) AS INT) AS count FROM filtered GROUP BY date
        """,
        output=False,
    )
    return (summedData,)


@app.cell
def _(mo, summedData):
    metrics = mo.sql(
        f"""
        SELECT AVG(count) as average, MIN(count) as minimum, MAX(count) as maximum, CAST(SUM(count) AS INT) AS total
         FROM summedData
        """,
        output=False
    )
    return (metrics,)


@app.cell
def _(alt, timeseries):
    # Create the Altair plot
    plotts = alt.Chart(timeseries).mark_line().encode(
        x='date:T',        # `:T` ensures it's treated as a temporal field
        y='count:Q',       # `:Q` ensures it's quantitative (numeric)
        color='streetname:N'  # `:N` treats it as a categorical variable
    ).interactive()
    return (plotts,)


@app.cell
def _(datePicker, metrics, mo, plotts, sc, slides):
    slides["dashboard"] = {}
    slides["dashboard"]["title"] = mo.md(
        r"""
        # 📊 Creating a Simple Dashboard
        """
    )

    slides["dashboard"]["content1"] = mo.hstack([mo.vstack([
        datePicker,
        plotts
        ]), mo.vstack([mo.hstack([mo.stat(label="The average was", value=round(metrics["average"][0]), caption="people per day"),
                       mo.stat(label="The minimum was", value=metrics["minimum"][0], caption="people per day")]),
                    mo.hstack([
                      mo.stat(label="The maximum was", value=metrics["maximum"][0], caption="people per day"),
                      mo.stat(label="The total was", value=metrics["total"][0], caption="people")])])
                                                 ])

    sc.create_slide(slides["dashboard"], layout_type="1-column")
    return


@app.cell
def _(mo, pd):
    projects = pd.DataFrame({
        "ID": ["P1", "P2", "P3", "P4", "P5"],
        "NPV": [100, 200, 150, 120, 300],  # Net Present Value
        "Capital_Y1": [50, 80, 40, 30, 120],  # Year 1 requirement
        "Capital_Y2": [20, 40, 30, 10, 60],  # Year 2 requirement
    })
    cap_y1 = mo.ui.slider(0, 320, value=150, label="Year 1 Allowance", show_value=True, step=10)
    cap_y2 = mo.ui.slider(0, 160, value=100, label="Year 2 Allowance", show_value=True, step=10)

    projectTable = mo.ui.table(projects, show_column_summaries=False, selection=None, show_download=False)
    return cap_y1, cap_y2, projectTable, projects


@app.cell
def _(mo, optimize):
    run_optimization = mo.ui.button(label="Optimize Investment Selection", on_click=lambda value: optimize(), value = "")
    return (run_optimization,)


@app.cell
def _(mo, run_optimization):
    if run_optimization.value == "":
        optimizationResultViewer = mo.md("No optimization result yet.")
    else:
        optimizationResultViewer = run_optimization.value
    return (optimizationResultViewer,)


@app.cell
def _(LinearConstraint, cap_y1, cap_y2, milp, mo, np, projects):
    def optimize():
        # Number of projects
        n = len(projects)

        # Objective: maximize total NPV --> minimize negative NPV
        # Create a vector of coefficients (we minimize, so use -NPV)
        c = -projects["NPV"].to_numpy()

        # Constraint matrix: each row represents one budget constraint
        A = np.vstack([
            projects["Capital_Y1"].to_numpy(),
            projects["Capital_Y2"].to_numpy()
        ])

        # Right-hand side for each constraint
        ub = np.array([cap_y1.value, cap_y2.value])
        # Lower bounds for constraints: no lower bound (-infinity)
        lb = -np.inf * np.ones(2)

        # Create a linear constraint object for the budget limits
        budget_constraint = LinearConstraint(A, lb, ub)

        # Variable bounds: each x_i must lie between 0 and 1
        bounds = [np.zeros(n), np.ones(n)]

        # Specify that all variables are integer (binary)
        integrality = np.ones(n, dtype=int)

        # Solve the MILP problem using SciPy’s milp
        res = milp(c=c,
                   integrality=integrality,
                   bounds=bounds,
                   constraints=budget_constraint)

        # Round the solution to obtain binary decisions
        selected_indices = np.where(np.round(res.x) == 1)[0]
        selected_projects = projects.iloc[selected_indices]
        total_npv = selected_projects["NPV"].sum() if not selected_projects.empty else 0

        return mo.vstack([
            mo.md("### ✅ Selected Projects"),
            mo.hstack(selected_projects["ID"].tolist()),
            mo.md(f"**Total NPV:** {total_npv}")
        ])
    return (optimize,)


@app.cell
def _(mo, sc, slides):
    slides["optimize"] = {}

    slides["optimize"]["title"] = mo.md(
    r"""
    # 📌 A knapsack problem
    """
    )

    slides["optimize"]["content1"] = mo.md(
    r"""
    * We have N investment projects, each with:

    * Net Present Value (NPV): The total expected return.
    * Annual Capital Requirement: How much budget it needs per year.
    * We need to select the best combination of projects to maximize total NPV, while ensuring we don’t exceed yearly capital allowances.
    """
    )

    sc.create_slide(slides["optimize"], layout_type="1-column")
    return


@app.cell
def _(
    cap_y1,
    cap_y2,
    mo,
    optimizationResultViewer,
    projectTable,
    run_optimization,
    sc,
    slides,
):
    slides["opt2"] = {}

    slides["opt2"]["title"] = mo.md(
        r"""
        # Knapsack Solver
        """
    )
    slides["opt2"]["content1"] = mo.vstack([
    mo.md("### 📊 Investment Projects"),
    projectTable,
    mo.md(f"### 🏦 Yearly Capital Allowances"),
        cap_y1,
    cap_y2,
        run_optimization
    ])


    slides["opt2"]["content2"] = optimizationResultViewer



    sc.create_slide(slides["opt2"])
    return


@app.cell
def _(mo, np, pd):
    # Define Warehouses with Coordinates
    warehouses = pd.DataFrame({
        "ID": ["W1", "W2", "W3"],
        "X": [10, 50, 80],  # X-coordinates
        "Y": [20, 60, 90],  # Y-coordinates
        "Fixed_Cost": [1500, 1200, 950]  # Base fixed costs for opening
    })

    # Define Customers with Coordinates
    customers = pd.DataFrame({
        "ID": ["C1", "C2", "C3", "C4", "C5", "C6"],
        "X": [15, 45, 85, 20, 55, 75],  # X-coordinates
        "Y": [25, 55, 95, 15, 65, 85],  # Y-coordinates
        "Demand": [6, 4, 3, 6, 2, 4]
    })

    # Compute Euclidean Distance Costs
    distance_costs = []
    cost_per_unit_distance = 2  # Define a cost per unit of distance

    for _, customer in customers.iterrows():
        for _, warehouse in warehouses.iterrows():
            distance = np.sqrt((customer["X"] - warehouse["X"])**2 + (customer["Y"] - warehouse["Y"])**2)
            cost = distance * cost_per_unit_distance
            distance_costs.append({"Customer": customer["ID"], "Warehouse": warehouse["ID"], "Cost": round(cost, 2)})

    # Convert distance cost data to DataFrame
    distance_costs = pd.DataFrame(distance_costs)


    warehouse_cost_factor = mo.ui.slider(0.1, 1.5, value=1.0, step=0.1, label="Warehouse Cost Multiplier", show_value=True)

    warehouseTable = mo.ui.table(warehouses, show_column_summaries=False, selection=None, show_download=False)
    customerTable = mo.ui.table(customers, show_column_summaries=False, selection=None, show_download=False)
    return (
        cost,
        cost_per_unit_distance,
        customer,
        customerTable,
        customers,
        distance,
        distance_costs,
        warehouse,
        warehouseTable,
        warehouse_cost_factor,
        warehouses,
    )


@app.cell
def _(mo):
    run_warehouse_optimization = mo.ui.run_button(
        label="Optimize Warehouse Selection"
    )
    return (run_warehouse_optimization,)


@app.cell
def _(
    LinearConstraint,
    customers,
    distance_costs,
    milp,
    np,
    pd,
    warehouse_cost_factor,
    warehouses,
):
    def optimize_warehouses():
        # Number of warehouses and customers
        W = len(warehouses)
        C = len(customers)

        # Get ordered lists of IDs
        wh_ids = warehouses["ID"].tolist()
        cust_ids = customers["ID"].tolist()

        # Create mapping from warehouse ID to index (for open decision variables)
        open_index = {wid: i for i, wid in enumerate(wh_ids)}

        # Create mapping for shipping variables: (customer, warehouse) -> index
        # Shipping variables start after the W open variables.
        ship_index = {}
        for i, c in enumerate(cust_ids):
            for j, w in enumerate(wh_ids):
                ship_index[(c, w)] = W + i * W + j

        n_vars = W + C * W  # total number of decision variables

        # ---- Objective Function ----
        # We minimize: fixed costs + transportation costs.
        # Build objective vector c_obj (length n_vars)
        c_obj = np.zeros(n_vars)
        # Fixed cost terms for each warehouse
        for i, row in warehouses.iterrows():
            c_obj[i] = row["Fixed_Cost"] * warehouse_cost_factor.value
        # Transportation cost terms for each (customer, warehouse) pair
        # (Assumes exactly one matching row in distance_costs for each pair)
        for (c, w), idx in ship_index.items():
            cost_val = distance_costs.loc[
                (distance_costs["Customer"] == c) & (distance_costs["Warehouse"] == w),
                "Cost"
            ].values[0]
            c_obj[idx] = cost_val

        # ---- Constraints ----
        # There are two sets of constraints:
        # 1. For each customer: sum_{w} ship[c, w] == Demand(c)
        n_cons1 = C
        A1 = np.zeros((n_cons1, n_vars))
        b_eq = np.zeros(n_cons1)
        for i, row in customers.iterrows():
            for w in wh_ids:
                idx = ship_index[(row["ID"], w)]
                A1[i, idx] = 1
            b_eq[i] = row["Demand"]

        # 2. For each (customer, warehouse): ship[c, w] - Demand(c)*open[w] <= 0
        n_cons2 = C * W
        A2 = np.zeros((n_cons2, n_vars))
        b_ub_2 = np.zeros(n_cons2)  # right-hand side is 0 for each constraint
        row_counter = 0
        # Loop over customers and warehouses to fill A2
        for i, cust in customers.iterrows():
            for j, wh in warehouses.iterrows():
                # Coefficient for shipping variable for (customer, warehouse)
                ship_idx = ship_index[(cust["ID"], wh["ID"])]
                A2[row_counter, ship_idx] = 1
                # Coefficient for open warehouse variable (note: negative coefficient)
                open_idx = open_index[wh["ID"]]
                A2[row_counter, open_idx] = -cust["Demand"]
                row_counter += 1

        # Combine constraints:
        # For customer demand, we require equality.
        # For shipping constraints, we require: (A2 * x) <= 0.
        A_total = np.vstack([A1, A2])
        lower_total = np.concatenate([b_eq, -np.inf * np.ones(n_cons2)])
        upper_total = np.concatenate([b_eq, np.zeros(n_cons2)])
        constraints = LinearConstraint(A_total, lower_total, upper_total)

        # ---- Bounds ----
        # Initialize lower bounds for all variables (all are nonnegative)
        lower_bounds = np.zeros(n_vars)

        # Initialize upper bounds array
        upper_bounds = np.empty(n_vars)

        # For the first W variables (open warehouse decisions), upper bound is 1
        upper_bounds[:W] = 1.0

        # For shipping variables, set the upper bound to the corresponding customer's demand.
        # Recall: shipping variables start at index W.
        for i in range(C):
            # Get the demand for customer i (assuming customers are ordered as in 'customers' DataFrame)
            demand = customers.iloc[i]["Demand"]
            for j in range(W):
                idx = W + i * W + j
                upper_bounds[idx] = demand

        # Create the bounds object with separate lower and upper arrays
        bounds = [lower_bounds, upper_bounds]



        # ---- Integrality ----
        # Create an integrality vector: 1 for integer variables (open warehouses), 0 for continuous (shipping).
        integrality = np.zeros(n_vars, dtype=int)
        integrality[:W] = 1  # first W variables (open) are binary

        # ---- Solve the MILP ----
        res = milp(c=c_obj,
                   integrality=integrality,
                   bounds=bounds,
                   constraints=constraints)

        # ---- Extract the Results ----
        x = res.x
        # Determine which warehouses are open by checking the first W entries
        active_warehouses = [wh_ids[i] for i in range(W) if round(x[i]) == 1]

        # Compute total fixed cost
        total_fixed = sum(
            row["Fixed_Cost"] * warehouse_cost_factor.value
            for _, row in warehouses.iterrows() if row["ID"] in active_warehouses
        )

        # Compute total transportation cost
        total_transport = 0
        for (c, w), idx in ship_index.items():
            cost_val = distance_costs.loc[
                (distance_costs["Customer"] == c) & (distance_costs["Warehouse"] == w),
                "Cost"
            ].values[0]
            total_transport += x[idx] * cost_val

        # Build the result DataFrame
        result_df = pd.DataFrame({
            "Cost Component": ["Fixed Costs", "Transportation Costs"],
            "Value": [total_fixed, total_transport],
            "Scenario": [warehouse_cost_factor.value, warehouse_cost_factor.value],
            "activeWarehouses": [active_warehouses, active_warehouses],
            "nWarehouses": [str(len(active_warehouses)), str(len(active_warehouses))],
            "totalCost": [total_fixed + total_transport, total_fixed + total_transport]
        })
        return result_df
    return (optimize_warehouses,)


@app.cell
def _():
    solutions =  []
    outputs = []
    return outputs, solutions


@app.cell
def _(
    alt,
    customers,
    mo,
    optimize_warehouses,
    pd,
    run_warehouse_optimization,
    solutions,
    warehouses,
):
    chart = None
    if run_warehouse_optimization.value:
        solution = optimize_warehouses()
        # Assume the list of opened warehouses
        opened_warehouses = solution["activeWarehouses"][0]
        
        # Mark opened warehouses
        warehouses["Opened"] = warehouses["ID"].apply(lambda x: x in opened_warehouses)
        
        # Create base chart
        base = alt.Chart().mark_circle(size=100).encode(
            x=alt.X("X", title="X Coordinate"),
            y=alt.Y("Y", title="Y Coordinate"),
            color=alt.Color("Type", scale=alt.Scale(domain=["Customer", "Opened Warehouse", "Closed Warehouse"], range=["blue", "green", "gray"])),
            tooltip=["ID", "X", "Y"]
        )
        
        # Customers
        customer_chart = base.encode(
            alt.ShapeValue("circle"),
            alt.ColorValue("blue")
        ).transform_calculate(Type="Customer").transform_filter(alt.datum.Type == "Customer")
        
        # Opened Warehouses
        opened_chart = base.encode(
            alt.ShapeValue("triangle"),
            alt.ColorValue("green")
        ).transform_calculate(Type="Opened Warehouse").transform_filter(alt.datum.Type == "Opened Warehouse")
        
        # Closed Warehouses
        closed_chart = base.encode(
            alt.ShapeValue("triangle"),
            alt.ColorValue("gray")
        ).transform_calculate(Type="Closed Warehouse").transform_filter(alt.datum.Type == "Closed Warehouse")
        
        # Combine all charts
        chart = alt.layer(customer_chart, opened_chart, closed_chart).properties(
            width=400,
            height=400,
            title="Warehouse and Customer Locations"
        ).configure_legend(labelFontSize=12, titleFontSize=14)
        
        # Display chart
        chart = alt.Chart(pd.concat([customers.assign(Type="Customer"), 
                                     warehouses.assign(Type=["Opened Warehouse" if w else "Closed Warehouse" for w in warehouses["Opened"]])])
                         ).mark_point(filled=True, size=100).encode(
            x=alt.X("X:Q", scale=alt.Scale(domain=[0, 125])),
            y=alt.Y("Y:Q", scale=alt.Scale(domain=[0, 125])),
            color=alt.Color("Type:N", scale=alt.Scale(domain=["Customer", "Opened Warehouse", "Closed Warehouse"], range=["blue", "green", "gray"])),
            shape=alt.Shape("Type:N", scale=alt.Scale(domain=["Customer", "Opened Warehouse", "Closed Warehouse"], range=["circle", "triangle", "triangle"])),
            tooltip=["ID", "X", "Y", "Type"]
        ).properties(
            width=400,
            height=400,
            title="Warehouse and Customer Locations"
        )

        solutions.append(solution)

    if len(solutions) > 0:
        solution = solutions[-1]
        temp = pd.concat(solutions)
        temp.drop("activeWarehouses", axis=1, inplace=True)
        temp = temp.drop_duplicates()
        temp.sort_values(by=["Scenario"], inplace=True)
        plot = alt.Chart(temp).mark_bar().encode(
        x=alt.X('Scenario:N', title='Scenario'),  # Nominal (categorical) x-axis
        y=alt.Y('Value:Q', title='Value'),  # Quantitative y-axis
        color=alt.Color('Cost Component:N', title='Cost Component'),  # Fill color
        tooltip=[
            alt.Tooltip('nWarehouses:Q', title='Warehouses'),
            alt.Tooltip('totalCost:Q', title='Total Cost')
        ]
    ).properties(
        title="Bar Chart"
    ).configure_legend(
        orient='bottom'  # Move legend to the bottom
    )
        warehouse_optimization_result = mo.vstack([
            chart,
            mo.md(f"**Total Cost:** {round(solution['Value'].sum(),1)}"),
            mo.md("### 📊 Cost Breakdown"),
            plot,
        ])
    else:
        warehouse_optimization_result = mo.md("No optimization result yet.")
    return (
        base,
        chart,
        closed_chart,
        customer_chart,
        opened_chart,
        opened_warehouses,
        plot,
        solution,
        temp,
        warehouse_optimization_result,
    )


@app.cell
def _(
    customerTable,
    mo,
    run_warehouse_optimization,
    sc,
    slides,
    warehouseTable,
    warehouse_cost_factor,
    warehouse_optimization_result,
):
    slides["warehouse_solver"] = {}

    slides["warehouse_solver"]["title"] = mo.md(
        r"""
        # WLP Solver
        """
    )
    slides["warehouse_solver"]["content1"] = mo.vstack([
        mo.md("### 🏢 Warehouses"),
        warehouseTable,
        mo.md("### 📦 Customers"),
        customerTable,
        mo.md(f"### 💰 Cost Parameters"),
        warehouse_cost_factor,
        run_warehouse_optimization
    ])

    slides["warehouse_solver"]["content2"] = warehouse_optimization_result

    sc.create_slide(slides["warehouse_solver"])
    return


@app.cell
def _(mo, sc, slides):
    slides["deploy"] = {}
    slides["deploy"]["title"] = mo.md("# Simple deployment options")
    slides["deploy"]["content1"] = mo.md(r"""
    ## 🚀 Deploying Marimo Notebooks

    Marimo offers flexible deployment options, allowing you to run notebooks **locally** or as **WebAssembly (WASM) applications**.


    ### ✅ **1. Run Locally**
    - The simplest way to use Marimo is to run it on your local machine.
    - This launches an interactive UI accessible via **localhost** in your browser.
    - Ideal for **development, personal use, and data exploration**.


    ### 🌍 **2. WebAssembly (WASM) Deployment**
    - Run Marimo **entirely in the browser**—no server required!
    - Uses **Pyodide** to execute Python code directly in WebAssembly.
    - Steps to deploy as a WASM app:

      1. Convert your notebook

      2. Upload the generated `index.html` file to any static hosting service (e.g., **GitHub Pages, Netlify, Vercel**).

      3. Users can now run your notebook **without Python installed!**
    """)

    sc.create_slide(slides["deploy"], layout_type="1-column")
    return


@app.cell
def _(mo, sc, slides):
    slides["comp"] = {}

    slides["comp"]["title"] = mo.md(
        r"""
        # 🎯 Final Thoughts
        """
    )

    slides["comp"]["content1"] = mo.md(
        r"""
    ### 🚀 Jupyter vs. Marimo: Side-by-Side

    | Feature              | Jupyter Notebook | Marimo Notebook |
    |:---------------------|:----------------|:----------------|
    | Hidden state issues | ✅ Yes           | ❌ No           |
    | UI Interactivity    | ❌ Limited       | ✅ Built-in     |
    | Live Updates       | ❌ No            | ✅ Yes          |
    | Easy Deployment    | ❌ Requires setup | ✅ Self-contained |
    | Lightweight        | ❌ Heavy         | ✅ Fast         |
        """
    )

    slides["comp"]["content2"] = mo.md(
        r"""


    ### Marimo is a modern alternative to Jupyter
    - Best for interactive, stateful notebooks
    - Helps create reproducible and reactive workflows
    - 🚀 Try it out and see the difference!

    ### 🔧 Getting Started with Marimo

    **Install Marimo**

    ```
    pip install marimo
    ```

    **Run a Notebook**

    ```
    marimo run my_notebook.py
    ```

    """
    )


    sc.create_slide(slides["comp"], layout_type="side-by-side")
    return


@app.cell
def _(mo):
    def fib(n):
        if n <= 1:
            return n
        else:
            return fib(n-1) + fib(n-2)

    mo.show_code(fib(3))
    return (fib,)


@app.cell
def _(fib, mo, sc, slides):
    slides["code"] = {}

    slides["code"]["title"] = mo.md("Coding in Marimo")

    slides["code"]["content1"] = mo.show_code(fib(3))

    sc.create_slide(slides["code"], layout_type="1-column")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
