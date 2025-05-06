import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="SQL Murder Mystery")


@app.cell(hide_code=True)
def _():

    import requests
    import marimo as mo    
    import sqlalchemy



    # URL of the dataset (must allow direct downloads)
    url = "https://github.com/NUKnightLab/sql-mysteries/raw/refs/heads/master/sql-murder-mystery.db"

    # Download and save the file
    filename = "murder.db"

    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"SQL DB setup successfull")
    else:
        print(f"Failed to download, status: {response.status_code}")

    DATABASE_URL = "sqlite:///murder.db"
    engine = sqlalchemy.create_engine(DATABASE_URL)
    return engine, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # SQL Murder Mystery

    Welcome to the **SQL Murder Mystery**! This interactive exercise challenges you to solve a fictional murder case using SQL queries. The data is stored in a SQLite database and contains information about people, crime scenes, interviews, and more.

    ## Database Schema

    The schema below shows the structure of the database. It includes tables such as `person`, `crime_scene_report`, `interview`, and `drivers_license`.

    ![Database Schema](https://raw.githubusercontent.com/NUKnightLab/sql-mysteries/master/schema.png)

    ## Getting Started

    **1. Simple SELECT query:**  
    A `SELECT` statement is used to retrieve data from a table. You can:

    - Use `SELECT *` to get **all columns** from a table.
    - Or specify individual columns to **narrow down** the results (e.g., `SELECT name, ssn FROM person`).

    Try both styles in the query cell below:

    ```sql
    -- Get all columns
    SELECT * FROM person;

    -- Get selected columns only
    SELECT name, ssn FROM person;
    ```
    """
    )
    return


@app.cell
def _(engine, mo, person):
    _df = mo.sql(
        f"""
        SELECT
            *
        FROM
            person
        LIMIT 5
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **2. JOIN query:**  
    A `JOIN` in SQL is used to combine rows from two or more tables based on a related column between them. It allows you to connect data across tables — for example, linking a person’s basic info with their vehicle license information.

    In this case, we are combining:
    - The `person` table, which includes `name`, `address_number`, `address_street_name`, and a `license_id`, and
    - The `drivers_license` table, which holds license-specific info like `plate_number`

    By matching `person.license_id = drivers_license.id`, we can retrieve each person’s name, address, and plate number — even though that data is spread across two separate tables.

    ```sql
    SELECT person.name, person.address_number, person.address_street_name, drivers_license.plate_number
    FROM person
    JOIN drivers_license
    ON person.license_id = drivers_license.id;
    ```

    Try running the query in the cell below.
    """
    )
    return


@app.cell
def _(drivers_license, engine, mo, person):
    _df = mo.sql(
        f"""
        SELECT
            person.name,
            person.address_number,
            person.address_street_name,
            drivers_license.plate_number
        FROM
            person
        JOIN
            drivers_license
        ON
            person.license_id = drivers_license.id
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **3. Filtering with WHERE clause:**  
    Use the `WHERE` clause to filter rows based on specific conditions — such as city names, dates, or suspect features.

    For example, to find crime scenes in 'SQL City' on January 15, 2018:

    ```sql
    SELECT * 
    FROM crime_scene_report
    WHERE city = 'SQL City' AND date = 20180115;
    ```

    Try modifying the city or date to explore other reports.
    """
    )
    return


@app.cell
def _(crime_scene_report, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM crime_scene_report
        WHERE city = 'SQL City' AND date = 20180115;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **4. Aggregation with GROUP BY and COUNT():**  
    `GROUP BY` lets you summarize rows by a shared attribute, and `COUNT()` tells you how many entries fall into each group.

    Example: Count how many licenses exist for each hair color:

    ```sql
    SELECT hair_color, COUNT(*) AS total
    FROM drivers_license
    GROUP BY hair_color;
    ```

    This helps spot patterns in the data.
    """
    )
    return


@app.cell
def _(drivers_license, engine, mo):
    _df = mo.sql(
        f"""
        SELECT hair_color, COUNT(*) AS total
        FROM drivers_license
        GROUP BY hair_color
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **5. Subqueries (SELECT inside SELECT):**  
    Subqueries allow you to filter results based on the outcome of another query.

    Example: Find people whose SSNs match those with an income above 90,000:

    ```sql
    SELECT name
    FROM person
    WHERE ssn IN (
        SELECT ssn
        FROM income
        WHERE annual_income > 90000
    );
    ```

    This is useful for cross-checking conditions across tables.
    """
    )
    return


@app.cell
def _(engine, income, mo, person):
    _df = mo.sql(
        f"""
        SELECT name
        FROM person
        WHERE ssn IN (
            SELECT ssn
            FROM income
            WHERE annual_income > 90000
        )
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # 🕵️ Now It's Your Turn!

    A **crime** has taken place and the detective needs your help to solve it.

    You remember hearing that the crime was a **murder** which happened on **January 15, 2018**, and it took place in **SQL City**.  
    The detective gave you access to the **crime scene report**, but... you lost it.  
    Luckily, you still remember a few key details — and you have access to the database.

    ### 🧩 Your Challenge:
    Use the SQL skills you've learned to:

    1. Start by retrieving the corresponding crime scene report.
    2. Use the leads in the report to investigate further.
    3. Combine queries, joins, filters, and subqueries as needed.
    4. Once you've identified the killer, insert their name in the solution box at the bottom.

    ## 🗺️ Database Schema

    Use this schema diagram to navigate across tables and plan your investigation.

    ![Database Schema](https://raw.githubusercontent.com/NUKnightLab/sql-mysteries/master/schema.png)

    ---  
    Use the two empty SQL cells below to get started.
    """
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        -- Write your SQL query here...
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        -- Write your SQL query here...
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, solution):
    _df = mo.sql(
        f"""
        -- Replace the text below with the name of the person you found
        INSERT INTO solution VALUES (1, 'Insert the name of the person you found here');
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, solution):
    _df = mo.sql(
        f"""
        -- This will return whether your solution is correct
        SELECT value FROM solution;
        """,
        engine=engine
    )
    return


if __name__ == "__main__":
    app.run()
