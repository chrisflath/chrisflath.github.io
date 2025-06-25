import marimo

__generated_with = "0.14.7"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Data Setup""")
    return


@app.cell
def _():
    import sqlalchemy

    DATABASE_URL = "sqlite:///public/data.db"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    import sqlalchemy

    DATABASE_URL = "sqlite:///public/nba.db"
    engine2 = sqlalchemy.create_engine(DATABASE_URL)
    return engine, engine2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Investigating Harold Shipman""")
    return


@app.cell
def _(engine, mo):
    shipmanTimes = mo.sql(
        f"""
        SELECT Hour,
        max(case when physician = 'Shipman' then percentage end) AS Shipman,
        max(case when physician <> 'Shipman' then percentage end) AS Comparison
        FROM shipman_times
        GROUP BY Hour;
        """,
        engine=engine
    )
    return (shipmanTimes,)


@app.cell
def _(shipmanTimes):
    shipmanTimes.to_pandas().plot(kind="line", x="Hour", y=["Shipman", "Comparison"], title="Shipman vs Comparison by Hour")
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        SELECT gender, ROUND(AVG(AGE)) AS meanAge, COUNT(*)
        from shipman_victims
        GROUP BY gender;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    shipmanOverTime = mo.sql(
        f"""
        SELECT yearofdeath, COUNT(*) as count
        from shipman_victims
        GROUP BY yearofdeath;
        """,
        engine=engine
    )
    return (shipmanOverTime,)


@app.cell
def _(shipmanOverTime):
    shipmanOverTime.to_pandas().plot(kind="line", x="yearOfDeath", y="count", title="Shipman vs Comparison by Hour")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Testcenter Betrug?""")
    return


@app.cell(hide_code=True)
def _(engine, mo):
    _df = mo.sql(
        f"""
        -- 1) Zieltabelle anlegen
        CREATE TEMP TABLE IF NOT EXISTS test_counts (
          dt          TEXT,         -- ISO-Datum
          test_center TEXT,
          tests_count INTEGER
        );
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(engine, mo):
    _df = mo.sql(
        f"""
        -- 2) Simulation mit rekursivem CTE
        WITH RECURSIVE
          -- 2a) 200 Tage zurück bis heute
          dates(dt, n) AS (
            SELECT date('now','-199 days'), 1
            UNION ALL
            SELECT date(dt, '+1 day'), n+1
            FROM dates
            WHERE n < 200
          ),
          -- 2b) Zentren mit ihren λ-Werten
          centers(test_center, lambda) AS (
            VALUES
              ('Zentrum_A',         80),
              ('Zentrum_B',        100),
              ('Zentrum_C',        120),
              ('Zentrum_D',         90),
              ('Zentrum_E', 100)
          ),
          -- 2c) Alle Kombinationen Datum × Zentrum
          grid AS (
            SELECT d.dt, c.test_center, c.lambda
            FROM dates d
            CROSS JOIN centers c
          ),
          -- 3) Poisson-Sampling via Inversion
          base AS (
            SELECT
              dt,
              test_center,
              CAST(
                -lambda * ln(
                  abs(random()) / 9223372036854775807.0
                )
              AS INTEGER) AS raw_count
            FROM grid
          ),
          -- 4) “Lift” im Schummel-Zentrum
          lifted AS (
            SELECT
              dt,
              test_center,
              CASE
                WHEN test_center = 'Zentrum_E'
                 AND raw_count < 80
                THEN
                  80
                  + CAST(
                      -20 * ln(
                        abs(random()) / 9223372036854775807.0
                      )
                    AS INTEGER)
                ELSE
                  raw_count
              END AS tests_count
            FROM base
          )
        -- 5) Einfügen
        INSERT INTO test_counts (dt, test_center, tests_count)
        SELECT dt, test_center, tests_count
        FROM lifted
        ORDER BY dt, test_center;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    tsTests = mo.sql(
        f"""
        SELECT * FROM test_counts
        """,
        engine=engine
    )
    return (tsTests,)


@app.cell
def _(tsTests):
    tsTests.to_pandas().set_index(['dt', 'test_center'])['tests_count'].unstack('test_center').plot(kind="line", title="Tests per Center Over Time")
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        CREATE TEMP TABLE first_digits AS
        SELECT test_center, SUBSTR(tests_count, 1, 1) AS first_digit
        FROM test_counts
            GROUP BY test_center, dt
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        SELECT test_center, first_digit, COUNT(*) AS count
        FROM first_digits
        GROUP BY first_digit,test_center
        ORDER BY first_digit;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    testBenford = mo.sql(
        f"""
        -- 1) Beobachtete Counts pro Zentrum × Ziffer
        CREATE TEMP TABLE tc_observed AS
        SELECT
          test_center,
          first_digit,
          COUNT(*) AS observed_count
        FROM first_digits
        GROUP BY test_center, first_digit
        ;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        -- 2) Gesamt-Counts pro Zentrum
        CREATE TEMP TABLE tc_total AS
        SELECT
          test_center,
          COUNT(*) AS total_count
        FROM first_digits
        GROUP BY test_center
        ;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        -- 3) Observed Probabilities berechnen
        CREATE TEMP TABLE tc_obs_prob AS
        SELECT
          o.test_center,
          o.first_digit,
          o.observed_count,
          t.total_count,
          ROUND(o.observed_count * 1.0 / t.total_count, 3) AS observed_prob
        FROM tc_observed o
        JOIN tc_total t
          ON o.test_center = t.test_center
        ;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        -- 4) Erwartete Counts und Probabilities hinzuholen
        CREATE TEMP TABLE tc_expected AS
        SELECT
          p.test_center,
          p.first_digit,
          p.observed_count,
          p.total_count,
          p.observed_prob,
          e.probability        AS expected_prob,
          ROUND(p.total_count * e.probability, 2) AS expected_count
        FROM tc_obs_prob p
        JOIN expected_benford e
          ON p.first_digit = e.digit
        ;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    deviations = mo.sql(
        f"""
        -- 6) Finale Ausgabe: sortiert nach größter Abweichung
        SELECT *
        FROM tc_deviation
        ORDER BY abs_deviation DESC
        ;
        """,
        engine=engine
    )
    return (deviations,)


@app.cell
def _(deviations):
    df = deviations.to_pandas()
    df['ratio'] = df['observed_prob'] / df['expected_prob']
    df.set_index(['first_digit', 'test_center'])['ratio'].unstack('test_center').plot(kind="bar")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Titanic Exploration""")
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM titanic;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# NBA Explorative Data Analysis""")
    return


@app.cell
def _(engine2, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM
        salary
        LIMIT 10;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo):
    _df = mo.sql(
        f"""
        select * FROM
        salary
        LIMIT 100,10;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM 
        (SELECT Player, Tm, Amount, ROW_NUMBER () OVER (ORDER BY Player) as row FROM salary)
        WHERE mod(row,50)==0;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo):
    _df = mo.sql(
        f"""
        SELECT MIN(Amount) AS Minimum FROM salary;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo):
    _df = mo.sql(
        f"""
        SELECT Amount AS FirstQuartile FROM salary ORDER BY Amount LIMIT (SELECT COUNT(Amount) FROM salary)/4,1;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo):
    _df = mo.sql(
        f"""
        SELECT Amount AS Median FROM salary ORDER BY Amount LIMIT 2*(SELECT COUNT(Amount) FROM salary)/4,1;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo):
    _df = mo.sql(
        f"""
        SELECT Amount AS ThirdQuartile FROM salary ORDER BY Amount LIMIT 3*(SELECT COUNT(Amount) FROM salary)/4,1;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo):
    _df = mo.sql(
        f"""
        SELECT MAX(Amount) AS Maximum FROM salary;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo):
    salaryTeams = mo.sql(
        f"""
        SELECT Tm, AVG(Amount) as AVGSalary FROM salary GROUP BY Tm;
        """,
        engine=engine2
    )
    return (salaryTeams,)


@app.cell
def _(salaryTeams):
    salaryTeams.to_pandas().plot(kind="bar", x="Tm", y="AVGSalary")
    return


@app.cell
def _(engine2, mo):
    playerCount = mo.sql(
        f"""
        SELECT Tm, Pos, COUNT(Player) as playerCount FROM players WHERE Tm NOT LIKE "TOT" GROUP BY Tm, Pos;
        """,
        engine=engine2
    )
    return (playerCount,)


@app.cell
def _(playerCount):
    playerCount.to_pandas().set_index(['Tm', 'Pos'])['playerCount'].unstack('Pos').plot(kind="bar")
    return


@app.cell
def _(engine2, mo):
    salaryPos = mo.sql(
        f"""
        SELECT players.Pos, AVG(Amount)
        FROM salary LEFT JOIN players ON players.Player == salary.Player
        GROUP BY Pos;
        """,
        engine=engine2
    )
    return (salaryPos,)


@app.cell
def _(salaryPos):
    salaryPos.to_pandas().plot(kind="bar", x="Pos")
    return


@app.cell
def _(engine2, mo):
    _df = mo.sql(
        f"""
        SELECT CASE
        WHEN Amount > 20000000 then "super-high"
        WHEN Amount > 10000000 then "high"
        ELSE "low"
        END as salaryLabel,
        COUNT(*) FROM salary
        GROUP BY salaryLabel;
        """,
        engine=engine2
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Analyseziele: Spieler und Gehälter

    ## 🔍 1. Beziehung zwischen Alter und Gehalt untersuchen
    **Ziel:** Herausfinden, ob ältere Spieler tendenziell mehr oder weniger verdienen.

    **Analyseideen:**
    - Streudiagramm oder Korrelationsanalyse (Alter vs. Durchschnittsgehalt)
    - Gruppierung nach Altersklassen (z. B. <25, 25–30, 30–35, >35)

    ---

    ## ⚽ 2. Gehaltsunterschiede je nach Spielerposition
    **Ziel:** Ermitteln, wie sich die Gehälter zwischen verschiedenen Spielerpositionen unterscheiden.

    **Analyseideen:**
    - Balkendiagramme oder Boxplots der Gehälter nach Position
    - Vergleich von Mittelwert, Median, Perzentilen je Position

    ---

    ## 🤝 3. Zusammenhang zwischen Teamgröße und durchschnittlichem Teamgehalt
    **Ziel:** Analysieren, ob Teams mit mehr Spielern im Durchschnitt höhere oder niedrigere Gehälter zahlen.

    **Analyseideen:**
    - Aggregation pro Team: Spieleranzahl & Durchschnittsgehalt berechnen
    - Scatterplot (Teamgröße vs. Durchschnittsgehalt)

    ---

    ## 📊 4. Gehaltsverteilung mittels Perzentilen verstehen
    **Ziel:** Die Verteilung der Gehälter besser begreifen und zentrale Lagen analysieren.

    **Analyseideen:**
    - Berechnung von Perzentilen (z. B. 10., 25., 50., 75., 90.)
    - Boxplot zur Visualisierung

    ---

    ## 💸 5. Top-N-verdienende Spieler identifizieren
    **Ziel:** Die höchsten Gehälter im Datensatz sichtbar machen.

    **Analyseideen:**
    - Sortierung nach Gehalt, Auswahl der Top-N
    - Darstellung in Tabelle oder Balkendiagramm
    - Analyse: Welche Positionen und Teams dominieren die Top-N?

    ---

    ## 📈 6. Altersverteilung der Spieler analysieren
    **Ziel:** Einblick in die Altersstruktur des Spielerkaders gewinnen.

    **Analyseideen:**
    - Histogramm der Spieleralter
    - Kennzahlen berechnen (Durchschnitt, Median, Min, Max, Standardabweichung)
    - Altersgruppen bilden und visuell vergleichen

    ---


    """
    )
    return


@app.cell(hide_code=True)
def _():
    return


if __name__ == "__main__":
    app.run()
