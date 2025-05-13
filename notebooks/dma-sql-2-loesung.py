import marimo

__generated_with = "0.13.6"
app = marimo.App(width="full", app_title="SQL Einführung 2")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Komplexe Abfragen auf mehreren Tabellen""")
    return


@app.cell(hide_code=True)
def _():

    import requests
    import marimo as mo    
    import sqlalchemy


    # URL of the dataset (must allow direct downloads)
    url = "https://raw.githubusercontent.com/WIBA-DMA/exam-2024-pprm/refs/heads/main/bundesliga.db"

    # Download and save the file
    filename = "bundesliga.db"

    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"SQL DB setup successful")
    else:
        print(f"Failed to download, status: {response.status_code}")

    DATABASE_URL = "sqlite:///bundesliga.db"
    engine = sqlalchemy.create_engine(DATABASE_URL)


    # URL of the dataset (must allow direct downloads)
    url = "https://raw.githubusercontent.com/WIBA-DMA/exam-2024-pprm/refs/heads/main/bundesliga_matches.db"

    # Download and save the file
    filename = "bundesliga_matches.db"

    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"SQL DB setup successful")
    else:
        print(f"Failed to download, status: {response.status_code}")

    DATABASE_URL = "sqlite:///bundesliga_matches.db"
    engine_matches = sqlalchemy.create_engine(DATABASE_URL)
    return engine, engine_matches, mo, requests, sqlalchemy


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Predict Tasks""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### UPDATE""")
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * from aktuelleTabelle;
        """,
        engine=engine
    )
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        UPDATE aktuelleTabelle
        SET Spiele = 31, S = 25, U = 6, N = 0, Tore = "77:22", Tordifferenz = 55, Punkte = 81
        WHERE Mannschaft = "Bayer 04 Leverkusen";
        """,
        engine=engine
    )
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * from aktuelleTabelle;
        """,
        engine=engine
    )
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        UPDATE aktuelleTabelle
        SET Spiele = 0, S = 0, U = 0, N = 0, Tore = "0:0", Tordifferenz = 0, Punkte = 0
        WHERE Spiele > 0;
        """,
        engine=engine
    )
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * from aktuelleTabelle;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### INSERT""")
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        INSERT INTO aktuelleTabelle
        (Mannschaft, Spiele, S, U, N, Tore, Tordifferenz, Punkte)
        VALUES
        ("Würzburger Kickers",0,0,0,0,"0:0",0,0);
        """,
        engine=engine
    )
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM aktuelleTabelle;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### INSERT 2""")
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        INSERT INTO aktuelleTabelle
        SELECT Mannschaft || " B-Team" AS Mannschaft, Spiele,  S,  U,  N,  Tore,  Tordifferenz,  Punkte FROM aktuelleTabelle
        LIMIT 2;
        """,
        engine=engine
    )
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM aktuelleTabelle;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### SELECT modifiers""")
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) from aktuelleTabelle;
        """,
        engine=engine
    )
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        SELECT DISTINCT substr(Mannschaft, 0, 11) FROM aktuelleTabelle;
        """,
        engine=engine
    )
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT (DISTINCT substr(Mannschaft, 0, 11)) FROM aktuelleTabelle;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### DELETE""")
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        DELETE FROM aktuelleTabelle WHERE Mannschaft LIKE '%B-Team';
        """,
        engine=engine
    )
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        DELETE FROM aktuelleTabelle
        WHERE Mannschaft = "Würzburger Kickers";
        """,
        engine=engine
    )
    return


@app.cell
def _(aktuelleTabelle, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM aktuelleTabelle;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Aggregation""")
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT * from ewigeTabelle;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte, Saison
        FROM ewigeTabelle
        WHERE Punkte = (SELECT MAX(Punkte) FROM ewigeTabelle);
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte, Saison
        FROM ewigeTabelle
        WHERE
        Punkte = (SELECT MAX(Punkte) FROM ewigeTabelle WHERE Rang = 18)
        AND Rang = 18;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, S, Saison
        FROM ewigeTabelle
        WHERE
        S = (SELECT MIN(S) FROM ewigeTabelle WHERE Rang = 1)
        AND Rang = 1;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### GROUP BY""")
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, COUNT(*) FROM ewigeTabelle WHERE Rang = 1 GROUP BY Mannschaft;
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Mengenoperationen""")
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft FROM ewigeTabelle WHERE Saison = "2022/2023"
        INTERSECT
        SELECT Mannschaft FROM ewigeTabelle WHERE Saison = "2021/2022";
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft FROM ewigeTabelle WHERE Saison = "2022/2023"
        EXCEPT
        SELECT Mannschaft FROM ewigeTabelle WHERE Saison = "2021/2022";
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Modify Tasks - Aggregation

    - Welche Mannschaft braucht wieviel Tore pro Punkt?
    """
    )
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, (1.0 * Tore) / (1 * Punkte) AS PktProSieg FROM ewigeTabelle
        GROUP BY Mannschaft
        ORDER BY PktProSieg DESC
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Was war die niedrigste Punktzahl je Verein?""")
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, MIN(Punkte) AS minPkt FROM ewigeTabelle
        GROUP BY Mannschaft
        ORDER BY minPkt ASC
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Welcher Verein hat wieviele Saisons / Spiele gespielt?""")
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, COUNT(Mannschaft) AS AnzahlSaisons FROM ewigeTabelle
        GROUP BY Mannschaft
        ORDER BY AnzahlSaisons DESC
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Wie viel Tore wurden pro Saison geschossen?""")
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Saison, SUM(Tore) AS Saisontore FROM ewigeTabelle
        GROUP BY Saison
        ORDER BY Saisontore DESC
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Welche Platzierungen haben die Bayern, der BVB und Gladbach wie oft belegt?""")
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Rang, Count(Mannschaft) AS Anzahl FROM ewigeTabelle
        WHERE Mannschaft LIKE "%Bayern München%"
        GROUP BY Rang
        ORDER BY Rang ASC
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Rang, Count(Mannschaft) AS Anzahl FROM ewigeTabelle
        WHERE Mannschaft LIKE "%Borussia Dortmund%" 
        GROUP BY Rang
        ORDER BY Rang ASC
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Rang, Count(Mannschaft) AS Anzahl FROM ewigeTabelle
        WHERE Mannschaft LIKE "%Borussia Mönchengladbach%" 
        GROUP BY Rang
        ORDER BY Rang ASC
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Welches Bundesliga-Matchup ist historisch am torreichsten?""")
    return


@app.cell
def _(engine_matches, mo, results):
    _df = mo.sql(
        f"""
        SELECT Team, Opponent, AVG(GoalsFor + GoalsAgainst) AS AvgGoals FROM results
        GROUP BY Team, Opponent
        ORDER BY AvgGoals DESC
        LIMIT 1
        """,
        engine=engine_matches
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Welche Mannschaft schießt daheim die meisten (die wenigsten) Tore pro Spiel?""")
    return


@app.cell
def _(engine_matches, mo, results):
    _df = mo.sql(
        f"""
        SELECT Team, AVG(GoalsFor) AS AvgGoalsFor FROM results
        WHERE Home = 1
        GROUP BY Team
        ORDER BY AvgGoalsFor DESC
        LIMIT 3
        """,
        engine=engine_matches
    )
    return


@app.cell
def _(engine_matches, mo, results):
    _df = mo.sql(
        f"""
        SELECT Team, AVG(GoalsFor) AS AvgGoalsFor FROM results
        WHERE Home = 1
        GROUP BY Team
        ORDER BY AvgGoalsFor ASC
        LIMIT 3
        """,
        engine=engine_matches
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Modify Tasks - GROUP BY

    - Wie viele Punkte holen die Vereine durchschnittlich pro Spiel?
    """
    )
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, 1.0*SUM(Punkte) / SUM(S+U+N) AS PpS
        FROM ewigeTabelle
        GROUP BY Mannschaft
        ORDER BY PpS DESC
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Wie viele Tore schießen die Vereine durchschnittlich pro Spiel?""")
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, 1.0*SUM(Tore) / SUM(S+U+N) AS TpS
        FROM ewigeTabelle
        GROUP BY Mannschaft
        ORDER BY TpS DESC
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Welche Mannschaft braucht wieviel Tore pro Punkt?""")
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, 1.0*SUM(Tore) / SUM(Punkte) AS TpP
        FROM ewigeTabelle
        GROUP BY Mannschaft
        ORDER BY TpP DESC
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Was war die niedrigste Punktzahl je Verein?""")
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, MIN(Punkte) AS minPkt
        FROM ewigeTabelle
        GROUP BY Mannschaft
        ORDER BY minPkt ASC
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Welcher Verein hat wieviele Saisons / Spiele gespielt?""")
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, COUNT(Mannschaft) AS saisons FROM ewigeTabelle
        GROUP BY Mannschaft
        ORDER BY saisons DESC
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) FROM ewigeTabelle
        WHERE Mannschaft LIKE "%Bayern%"
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Wie viel Tore wurden pro Saison geschossen?""")
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT saison, SUM(Tore) AS sumTore FROM ewigeTabelle
        GROUP BY saison
        ORDER BY sumTore DESC
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Modify Tasks - HAVING
    - Von den Vereinen die mindestens drei Mal Meister wurden, wer wurde wie oft Meister?
    """
    )
    return


@app.cell
def _(engine, ewigeTabelle, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, COUNT(Mannschaft) AS anzMeister FROM ewigeTabelle
        WHERE Rang = 1
        GROUP BY Mannschaft
        HAVING anzMeister >=3
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Gegen welchen Verein hat Bayern daheim die beste Gewinnrate (mind. 20 Partien)?""")
    return


@app.cell
def _(engine_matches, mo, results):
    _df = mo.sql(
        f"""
        SELECT Opponent, (ROUND(1.0*Wins / Games,3)*100) || '%' AS Quote, Games FROM -- Siegquote aus Siegen und Spielen bestimmen als Prozentzahl  mit einer Stelle, dahinter Prozentzeichen
        (SELECT  -- 
            Opponent,
            SUM(GoalsFor > GoalsAgainst) AS Wins, -- Sieg codieren wenn Tor größer als Gegentore
            COUNT(Opponent) AS Games -- Anzahl Spiele gegen Opponent
        FROM
            results
        WHERE
            Team LIKE "%Bayern München" -- ZUsammenfassen aller Schreibweisen von FCB
            AND Home = 1 -- nur Heimspiele
        GROUP BY
            Opponent -- Gruppierung nach Gegner
        HAVING
            Games >= 20) -- mind. 20 Spiele
        ORDER BY Quote DESC -- Absteigend sortieren nach Siegquote
        """,
        engine=engine_matches
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Welches Bundesliga-Matchup ist historisch am torärmsten (mind. 40 Partien)?""")
    return


@app.cell
def _(engine_matches, mo, results):
    _df = mo.sql(
        f"""
        SELECT
            Team,
            Opponent,
            ROUND(AVG(GoalsFor + GoalsAgainst) / 2,2) AS Tore,
            COUNT(TEAM) / 2 AS Spiele
        FROM
            results
        GROUP BY
            Team,
            Opponent
        HAVING
            Spiele >= 40
        ORDER BY Tore DESC
        """,
        engine=engine_matches
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- Welche Mannschaften haben gegen mindestens 5 Vereine mit mindestens 5 Toren Vorsprung auswärts gewonnen?""")
    return


@app.cell
def _(engine_matches, mo, results):
    _df = mo.sql(
        f"""
        SELECT Team, COUNT(DISTINCT(Opponent)) AS anzahl FROM results
        WHERE GoalsFor - GoalsAgainst >= 5
        GROUP BY Team
        HAVING anzahl >= 5
        """,
        engine=engine_matches
    )
    return


@app.cell
def _(engine_matches, mo, results):
    _df = mo.sql(
        f"""
        SELECT * FROM results
        WHERE GoalsFor - GoalsAgainst >= 5
        AND Team = "VfL Bochum"
        """,
        engine=engine_matches
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- In welchen Saisons gab es mindestens 15 Spiele mit einer Tordifferenz von 5 Toren?""")
    return


@app.cell
def _(engine_matches, mo, results):
    _df = mo.sql(
        f"""
        SELECT SeasonLabel, COUNT(Team) AS anzahl FROM results
        WHERE GoalsFor - GoalsAgainst >= 5
        GROUP BY SeasonLabel
        HAVING anzahl >= 15
        """,
        engine=engine_matches
    )
    return


@app.cell
def _(engine_matches, mo, results):
    _df = mo.sql(
        f"""
        SELECT * FROM results
        WHERE GoalsFor - GoalsAgainst >= 5
        AND SeasonLabel = "1965/66"
        """,
        engine=engine_matches
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Übungsaufgaben""")
    return


@app.cell(hide_code=True)
def _(requests, sqlalchemy):
    # URL of the dataset (must allow direct downloads)
    url2 = "https://raw.githubusercontent.com/WIBA-DMA/exam-2024-pprm/refs/heads/main/rheinwerk.db"

    # Download and save the file
    filename2 = "rheinwerk.db"

    response2 = requests.get(url2)
    if response2.status_code == 200:
        with open(filename2, "wb") as file2:
            file2.write(response2.content)
        print(f"SQL DB setup successfull")
    else:
        print(f"Failed to download, status: {response2.status_code}")

    DATABASE_URL2 = "sqlite:///rheinwerk.db"
    engine2 = sqlalchemy.create_engine(DATABASE_URL2)
    return (engine2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Make - Aufgabe 1
    - In dieser Aufgabe schreiben Sie SQL Abfragen um neue Zeilen einzufügen.

        - Nehmen Sie weitere Qualifikationen in die Tabelle _qualifikationen_ auf. Die neue Zeile soll mit einer expliziten Spaltenangabe in die Tabelle eingefügt werden. In die Spaltenliste soll Folgendes aufgenommen werden: _qid_, _bezeichnung_, _kuerzel_ und _kategorie_. Wir möchten die Qualifikation _SQL_ eintragen, die mit dem Kürzel _ITE_ in die Kategorie _Informatik_ aufgenommen werden soll. 

        - In jedem größeren Unternehmen gibt es Administratoren. Diese Qualifikation werden wir als Nächstes in die Tabelle eintragen. Geben Sie als Bezeichnung _Administrator_, als Kürzel _ADA_ und als Kategorie _Support_ ein.
    """
    )
    return


@app.cell
def _(engine2, mo, qualifikationen):
    _df = mo.sql(
        f"""
        SELECT * from qualifikationen
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo, qualifikationen):
    _df = mo.sql(
        f"""
        INSERT INTO qualifikationen
        (qid, bezeichnung, kuerzel, kategorie)
        VALUES
        (1,"SQL","ITE","Informatik"),
        (2,"Administrator","ADA","Support"); 
        """,
        engine=engine2
    )
    return


app._unparsable_cell(
    r"""
    SELECT * from qualifikationen
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Make - Aufgabe 2
    - In dieser Aufgabe schreiben Sie SQL Abfragen um bestehende Zeilen zu verändern.

        - Die Zeile mit dem Schlüsselwert 2 der Spalte _qid_ der Tabelle _qualglobal_ identifiziert einen Datensatz in dem der Spalte _bezeichnung_ der Wert _Second Level Support_ zugeordnet ist. Ändern Sie die Bezeichnung zu dem Wert _Second Level Helpdesk_.

        - Jetzt soll die Bezeichnung des Datensatzes mit Schlüsselwert 3 geändert werden. Ändern Sie die _bezeichnung_ zu _First Level Helpdesk_ und das _kuerzel_ zu _FLH_.

        - Das Unternehmen beabsichtigt auf eine freie Office-Suite umzusteigen. Daher soll den Werten der Spalte _kategorie_, die derzeit dem Wert _Office_ entsprechen, ein _NULL_-Wert zugeordnet werden.
    """
    )
    return


@app.cell
def _(engine2, mo, qualglobal):
    _df = mo.sql(
        f"""
        SELECT * FROM qualglobal;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo, qualglobal):
    _df = mo.sql(
        f"""
        UPDATE qualglobal
        SET bezeichnung = "Second Level Helpdesk", kuerzel = "SLH"
        WHERE qid = 2;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo, qualglobal):
    _df = mo.sql(
        f"""
        UPDATE qualglobal
        SET bezeichnung = "First Level Helpdesk", kuerzel = "FLH"
        WHERE qid = 3;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo, qualglobal):
    _df = mo.sql(
        f"""
        UPDATE qualglobal
        SET kategorie = NULL
        WHERE kategorie = "Office"
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo, qualglobal):
    _df = mo.sql(
        f"""
        SELECT * FROM qualglobal;
        """,
        engine=engine2
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Make - Aufgabe 3 - Zeilen löschen
    - In dieser Aufgabe schreiben Sie SQL Abfragen um bestehende Zeilen zu löschen.

        - Als Erstes soll die Zeile mit dem Schlüsselwert 2 aus der Tabelle _qualglobalarchiv_ gelöscht werden.

        - Nun sollen die Eintrage mit der _qid_ 5, 6 und 7 gelöscht werden.

        - Löschen Sie alle verbleibenden Einträge der Tabelle _qualglobalarchiv_.
    """
    )
    return


@app.cell
def _(engine2, mo, qualglobalarchiv):
    _df = mo.sql(
        f"""
        SELECT * FROM qualglobalarchiv;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo, qualglobalarchiv):
    _df = mo.sql(
        f"""
        DELETE FROM qualglobalarchiv
        WHERE qid in (2, 5, 6, 7)
        """,
        engine=engine2
    )
    return


app._unparsable_cell(
    r"""
    SELECT * FROM qualglobalarchiv;
    """,
    name="_"
)


@app.cell
def _(engine2, mo, qualglobalarchiv):
    _df = mo.sql(
        f"""
        DELETE FROM qualglobalarchiv;
        """,
        engine=engine2
    )
    return


app._unparsable_cell(
    r"""
    SELECT * FROM qualglobalarchiv;
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Make - Aufgabe 4 - Spaltenwerte gruppieren
    - In dieser Aufgabe schreiben Sie SQL Abfragen um Aggregate über Gruppen zu berechnen.

        - In der Tabelle _kreditinstitut_auszug_ sind sämtliche Kreditinstitute und deren Bankleitzahlen erfasst. Jeder Bankleitzahl können mehrere Kreditinstitute zugeordnet sein. Ermittelen Sie wieviele Kreditinstitute den jeweiligen Bankleitzahlen zugeordnet sind.

        - Ermitteln Sie, basierend auf der Tabelle _bonus_, die Summe der Auszahlungen für Bonuszahlungen, die jeweils an einem Tag ausgeschüttet werden.

        - Ermitteln Sie, basierend auf der Tabelle _bonus_, den durchschnittlichen Bonus den die Mitarbeiter jeweils erhalten haben.
    """
    )
    return


@app.cell
def _(engine2, kreditinstitut_auszug, mo):
    _df = mo.sql(
        f"""
        SELECT bankleitzahl, COUNT(bezeichnung) from kreditinstitut_auszug
        GROUP BY bankleitzahl
        """,
        engine=engine2
    )
    return


@app.cell
def _(bonus, engine2, mo):
    _df = mo.sql(
        f"""
        SELECT auszahlungsdatum, SUM(bonuszahlung) AS zahlung FROM bonus
        GROUP BY auszahlungsdatum;
        """,
        engine=engine2
    )
    return


@app.cell
def _(bonus, engine2, mo):
    _df = mo.sql(
        f"""
        SELECT AVG(bonuszahlung) AS durchschnitt, COUNT(bonuszahlung) AS zahlungen FROM bonus
        GROUP BY mitarbeiterid;
        """,
        engine=engine2
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Make - Aufgabe 5 - Nach aggregierten Werten einer Gruppierung filtern
    - In dieser Aufgabe schreiben Sie SQL Abfragen um Aggregate über Gruppen zu berechnen und basierend auf diesen Aggregaten zu filtern.

        - Ermitteln Sie in der Tabelle _kreditinstitut_auszug_ alle Bankleitzahlen, denen mehr als ein Kreditinstitut zugeordnet ist.

        - In der Tabelle _arbeitszeit_auszug_ sind die Arbeitszeiten eines jeden Mitarbeiters pro Tag hinterlegt. Erstellen Sie einen Bericht, der auswertet, wie viele Stunden jeder Mitarbeiter pro Monat gearbeitet hat. Diese Auswertung bezieht sich immer auf das jeweilige Jahr. Geben Sie nur Mitarbeiter aus die mindestens 100 Stunden gearbeitet haben.
    """
    )
    return


@app.cell
def _(engine2, kreditinstitut_auszug, mo):
    _df = mo.sql(
        f"""
        SELECT bankleitzahl, COUNT(bezeichnung) AS anzahl from kreditinstitut_auszug
        GROUP BY bankleitzahl
        HAVING anzahl > 1
        """,
        engine=engine2
    )
    return


@app.cell
def _(arbeitszeit_auszug, engine2, mo):
    _df = mo.sql(
        f"""
        SELECT monat, SUM(anzahlstunden) AS summe FROM arbeitszeit_auszug
        GROUP BY monat, mitarbeiterid
        HAVING summe >= 100
        """,
        engine=engine2
    )
    return


if __name__ == "__main__":
    app.run()
