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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Solution    

    ### Step 1: Get the Crime Scene Report

    We start by locating the crime scene report for the **murder** in **SQL City** on **January 15, 2018**.
    """
    )
    return


@app.cell
def _(crime_scene_report, engine, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM crime_scene_report
        WHERE type = 'murder' AND city = 'SQL City' AND date = 20180115;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ### Step 2: Interview the Witnesses

    We now look into the **interview** table for the IDs mentioned in the previous result: ID 14887 and 16371.
    """
    )
    return


@app.cell
def _(engine, interview, mo, person):
    _df = mo.sql(
        f"""
        SELECT transcript 
        FROM interview 
        WHERE person_id IN (
            SELECT id 
            FROM person 
            WHERE (address_street_name = 'Northwestern Dr' AND address_number = (
                    SELECT MAX(address_number) 
                    FROM person 
                    WHERE address_street_name = 'Northwestern Dr'
                ))
            OR (name LIKE 'Annabel%' AND address_street_name = 'Franklin Ave')
        );
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ### Step 3: Find the Gym Member

    From the interviews, we learned the suspect had a **membership at the local gym**, and his **license plate** was seen. We now connect this to the **drivers_license** table.
    """
    )
    return


@app.cell
def _(
    drivers_license,
    engine,
    get_fit_now_check_in,
    get_fit_now_member,
    mo,
    person,
):
    _df = mo.sql(
        f"""
        -- Step 1: Find all gold members with "48Z" in their ID who checked in on Jan 9
        SELECT p.id, p.name, d.plate_number, d.gender
        FROM get_fit_now_member AS p
        JOIN get_fit_now_check_in AS c
            ON p.id = c.membership_id
        JOIN person AS per
            ON p.person_id = per.id
        JOIN drivers_license AS d
            ON per.license_id = d.id
        WHERE p.membership_status = 'gold'
        AND p.id LIKE '48Z%'
        AND c.check_in_date = '20180109'
        AND d.gender = 'male'
        AND d.plate_number LIKE '%H42W%';
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ### Step 4: Confirm the Murderer

    We now confirm the guilty person using the transcript from the interview table.
    """
    )
    return


@app.cell
def _(engine, mo, solution):
    _df = mo.sql(
        f"""
        -- Replace the text below with the name of the person you found
        INSERT INTO solution VALUES (1, 'Jeremy Bowers');
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ### Step 5: The Master Query

    Congrats, you found the murderer! But wait, there's more... If you think you're up for a challenge, try querying the interview transcript of the murderer to find the real villain behind this crime. If you feel especially confident in your SQL skills, try to complete this final step with no more than 2 queries. Use this same INSERT statement with your new suspect to check your answer.
    """
    )
    return


@app.cell
def _(engine, interview, mo):
    _df = mo.sql(
        f"""
        SELECT transcript
        FROM interview
        WHERE person_id = 67318;
        """,
        engine=engine
    )
    return


@app.cell
def _(drivers_license, engine, facebook_event_checkin, income, mo, person):
    _df = mo.sql(
        f"""
        SELECT name, annual_income
        FROM (
            SELECT person.id AS person_id, person.name, income.annual_income
            FROM drivers_license
            JOIN person ON drivers_license.id = person.license_id
            JOIN income ON person.ssn = income.ssn
            WHERE gender = 'female'
              AND hair_color = 'red'
              AND car_make = 'Tesla'
              AND car_model = 'Model S'
              AND height BETWEEN 64 AND 68
        ) AS rich_suspects
        JOIN (
            SELECT person_id, COUNT(*) AS n_checkins
            FROM facebook_event_checkin
            WHERE event_name = 'SQL Symphony Concert'
              AND date LIKE '201712%'
            GROUP BY person_id
            HAVING n_checkins = 3
        ) AS symphony_attenders
        ON rich_suspects.person_id = symphony_attenders.person_id
        """,
        engine=engine
    )
    return


if __name__ == "__main__":
    app.run()
