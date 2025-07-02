import marimo

__generated_with = "0.14.6"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import requests
    import matplotlib
    return mo, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Data Setup""")
    return


@app.cell
def _(requests):
    url = "https://chrisflath.github.io/notebooks/public/data.db"

    # Download and save the file
    filename = "data.db"

    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"SQL DB setup successfull")
    else:
        print(f"Failed to download, status: {response.status_code}")

    url = "https://chrisflath.github.io/notebooks/public/nba.db"

    # Download and save the file
    filename = "nba.db"

    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"SQL DB setup successfull")
    else:
        print(f"Failed to download, status: {response.status_code}")


    import sqlalchemy

    DATABASE_URL = "sqlite:///data.db"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    import sqlalchemy

    DATABASE_URL = "sqlite:///nba.db"
    engine2 = sqlalchemy.create_engine(DATABASE_URL)
    return engine, engine2


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Dr. Harold Shipman – Vom vertrauenswürdigen Arzt zum Serienmörder

    **Wer war Harold Shipman?**  
    Harold Frederick Shipman (1946–2004) war ein britischer Allgemeinmediziner, der jahrzehntelang in Hyde, Greater Manchester, praktizierte. Er genoss bei vielen Patienten hohes Ansehen, bis 1998 erste Verdachtsmomente auftraten. Schließlich stellte sich heraus, dass er mindestens 215 seiner Patienten ermordet hatte – womit er zu einem der größten Serienmörder in der modernen Kriminalgeschichte wurde.

    ---

    ### Die datenbasierte Spur: Wie Statistik zur Aufklärung beitrug

    1. **Ungewöhnliche Sterberaten**  
       – Ein Inspektor bemerkte, dass in Shipmans Praxis überproportional viele Patienten – vor allem ältere Frauen – unter seiner Obhut verstarben.  
       – Ein Vergleich mit anderen Hausarztpraxen zeigte, dass Shipmans Sterberaten in bestimmten Altersgruppen und Zeitfenstern signifikant höher lagen.

    2. **Analyse der Todeszeitpunkte**  
       – Mithilfe statistischer Auswertungen (z. B. stündliche Verteilungen) konnte man nachweisen, dass ein ungewöhnlich großer Teil der Todesfälle in den späten Vormittagsstunden stattfand – eine Uhrzeit, die viele andere Ärzte nicht aufwiesen.  
       – Die Wahrscheinlichkeit, dass so viele Todesfälle zufällig in dieses Zeitfenster fielen, war extrem gering.

    3. **Demografische Muster**  
       – Durchschnittsalter, Geschlechterverteilung und Vorerkrankungen der Opfer passten nicht zu üblichen Mortalitätsstatistiken.  
       – Viele Opfer waren alleinstehende, älterer Frauen, die oft keine nahen Angehörigen hatten, die Verdacht schöpften.

    4. **Toxikologische Befunde und Autopsien**  
       – Initial durchgeführte Obduktionen ergaben in einigen Fällen Spuren von starken Opiaten (z. B. Diamorphin), die in keiner ärztlichen Verordnung dokumentiert waren.  
       – Die ungewöhnlich häufige Präsenz dieser Substanzen weckte weitere Zweifel.

    5. **Kombinierter Beweis – Statistik trifft Forensik**  
       – Die statistischen Auffälligkeiten lieferten den Ermittlern eine rationale Grundlage, um gezielte Nachuntersuchungen (Re-Autopsien) anzustoßen.  
       – So konnten sie in mehreren Fällen bestätigen, dass die Todesursache manipuliert war.

    ---

    ### Bedeutung und Lehren

    - **Rolle der Datenanalyse**  
      Die akribische Auswertung von Praxisdaten – Sterberaten, Zeitmuster, demografische Merkmale – war entscheidend, um Anfangsverdacht zu erhärten und die Ermittlungen in die richtige Richtung zu lenken.  
    - **Benford’sches Gesetz als Beispiel**  
      In ähnlichen Fällen kann man auch Benford’s Gesetz nutzen, um tarifäre oder abrechnungsbezogene Manipulationen aufzudecken.  
    - **Vertrauen versus Kontrolle**  
      Shipmans Fall zeigt, wie wichtig unabhängige, datenbasierte Kontrollen in Gesundheitswesen und anderen Berufen mit großer Vertrauensmacht sind.

    > „Statistik ist kein Ersatz für menschliches Urteilsvermögen – aber sie kann den Blick schärfen, wo wir ohne sie allenfalls Zufall sehen würden.“  
    > *(frei nach William Edward Deming)*
    """
    )
    return


@app.cell
def _(engine, mo, shipman_times):
    shipmanTimes = mo.sql(
        f"""
        SELECT Hour,
        max(case when physician = 'Shipman' then percentage end) AS Shipman,
        max(case when physician <> 'Shipman' then percentage end) AS Vergleichsgruppe
        FROM shipman_times
        GROUP BY Hour;
        """,
        engine=engine
    )
    return (shipmanTimes,)


@app.cell
def _(shipmanTimes):
    shipmanTimes.plot(kind="line", x="Hour", y=["Shipman", "Vergleichsgruppe"], title="Shipman vs Vergleichsgruppe nach Stunde")
    return


@app.cell
def _(engine, mo, shipman_victims):
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
def _(engine, mo, shipman_victims):
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
    shipmanOverTime.plot(kind="line", x="yearOfDeath", y="count", title="Shipman vs Comparison by Hour")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Abrechnungsbetrug bei COVID-Testzentren und Benford’s Gesetz

    ### Kontext: COVID-Testzentren und Abrechnungsmodelle  
    Während der Pandemie wurden in vielen Ländern flächendeckend COVID-Testzentren eingerichtet. Betreiber reichten ihre Leistungsabrechnungen meist tagesaktuell bei öffentlichen Stellen oder Krankenkassen ein. Da die Vergütung pro Test erfolgte, bestand ein finanzieller Anreiz für manche Anbieter, Testzahlen zu manipulieren oder fiktive Tests abzurechnen.

    ---

    ### Typische Formen des Abrechnungsbetrugs  
    1. **Hochstufung geringer Fallzahlen**  
       – Vereinzelte tatsächlich durchgeführte Tests werden als umfangreiche Testtage ausgewiesen.  
    2. **Erfindung ganzer Testtage**  
       – An manchen Tagen wurden gar keine Tests durchgeführt, aber in der Abrechnung auftauchten sie als volumenstarke Tage.  
    3. **Mix aus realen und fiktiven Daten**  
       – Teilweise wurden reale Testmengen mit frei erfundenen Zahlen aufgebläht, um Einnahmen zu steigern.

    ---

    ### Datenbasierte Aufdeckung mit Benford’s Gesetz

    #### Was ist Benford’s Gesetz?  
    Benford’s Gesetz (oder Erste-Ziffern-Gesetz) beschreibt die Verteilung der ersten Ziffern in vielen realen Daten­beständen. Es besagt, dass die Ziffer **1** in natürlicher Zahlen­folgen mit rund **30,1 %** als erste Ziffer auftritt, **2** mit **17,6 %**, **3** mit **12,5 %** und so weiter bis **9** mit nur **4,6 %**. Diese Verteilung ergibt sich aus logarithmischen Skalen und gilt für Daten, die sich über mehrere Größenordnungen erstrecken.

    #### Anwendung auf Testcenter-Daten  
    1. **Erfassung der ersten Ziffer**  
       - Man extrahiert aus jedem tagesaktuellen Test-Abrechnungswert die erste Ziffer (z. B. aus 125 Tests → „1“).  
    2. **Beobachtete Häufigkeit vs. Erwartung**  
       - Für jedes Testzentrum berechnet man, wie oft jede Ziffer 1–9 als erste Ziffer auftritt.  
       - Anschließend vergleicht man die beobachteten relativen Häufigkeiten mit den theoretischen Werten aus Benford’s Gesetz.  
    3. **Erkennung signifikanter Abweichungen**  
       - Deutliche Über- oder Unterrepräsentation bestimmter Ziffern (etwa zu viele Tage mit 80–89 Tests statt der erwarteten Verteilung) weist auf mögliche Manipulationen hin.  
       - Besonders auffällig sind Abweichungen in Testzentren, die intensiv in die Prüfung der Behörden geraten sind.

    ---

    ### Bedeutung und Nutzen  
    - **Früherkennung von Betrugsfällen**  
      Automatisierte Benford-Checks können in großen Datenströmen (Tausende Abrechnungszeilen) schnell auffällige Muster entdecken und so gezielte Audits auslösen.  
    - **Ressourcenschonende Kontrolle**  
      Anstatt jede einzelne Abrechnung manuell zu prüfen, ermöglicht das Gesetz eine Priorisierung nach Anomalie-Schwere.  
    - **Vertrauensbildung**  
      Transparente und datengetriebene Prüfverfahren erhöhen das Vertrauen in öffentliche Gesundheitssysteme und senken staatliche Kontrollkosten.

    ---

    > **Fazit:**  
    > Benford’s Gesetz ist kein Allheilmittel, aber ein mächtiges Werkzeug, um in Finanz- und Leistungsdaten – wie COVID-Testabrechnungen – Unregelmäßigkeiten aufzuspüren. In Kombination mit weiteren forensischen Prüfmaßnahmen kann es einen entscheidenden Beitrag zur Aufdeckung und Verhinderung von Abrechnungsbetrug leisten.  
    """
    )
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
    return (test_counts,)


@app.cell(hide_code=True)
def _(base, centers, dates, engine, grid, lifted, mo, test_counts):
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
def _(engine, mo, test_counts):
    tsTests = mo.sql(
        f"""
        SELECT * FROM test_counts
        """,
        engine=engine
    )
    return (tsTests,)


@app.cell
def _(engine, mo, test_counts):
    _df = mo.sql(
        f"""
        SELECT test_center, MAX(tests_count) AS MaxTests, min(tests_count) AS MinTests, AVG(tests_count) AS AvgTests, AVG(tests_count) / MAX(tests_count) AS Auslastung  FROM test_counts GROUP BY test_center
        """,
        engine=engine
    )
    return


@app.cell
def _(mo, tsTests):
    centerSelect = mo.ui.multiselect(tsTests['test_center'].unique(), label="Test Center",value=["Zentrum_A"])
    return (centerSelect,)


@app.cell
def _(centerSelect, mo, tsTests):
    if len(centerSelect.value) > 0:
        plot = tsTests[tsTests['test_center'].isin(centerSelect.value)].set_index(['dt', 'test_center'])['tests_count'].unstack('test_center').plot(kind="line", title="Tests per Center Over Time")
    else:
        plot = mo.md("Bitte mindestens ein Testzentrum wählen.")
    mo.hstack([centerSelect,plot], justify="start")
    return


@app.cell
def _(engine, mo, test_counts):
    _df = mo.sql(
        f"""
        CREATE TEMP TABLE first_digits AS
        SELECT test_center, SUBSTR(tests_count, 1, 1) AS first_digit
        FROM test_counts
            GROUP BY test_center, dt
        """,
        engine=engine
    )
    return (first_digits,)


@app.cell
def _(engine, first_digits, mo):
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
def _(engine, first_digits, mo):
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
def _(engine, first_digits, mo):
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
    return (tc_total,)


@app.cell
def _(engine, mo, tc_observed, tc_total):
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
    return (tc_obs_prob,)


@app.cell
def _(engine, expected_benford, mo, tc_obs_prob):
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
    return (tc_expected,)


@app.cell
def _(engine, mo, tc_expected):
    deviations = mo.sql(
        f"""
        SELECT test_center, first_digit, expected_prob - observed_prob AS deviation
        FROM tc_expected
        ORDER BY deviation DESC
        ;
        """,
        engine=engine
    )
    return (deviations,)


@app.cell
def _(deviations):
    deviations.set_index(['first_digit', 'test_center'])['deviation'].unstack('test_center').plot(kind="bar")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Titanic Exploration""")
    return


@app.cell
def _(engine, mo, titanic):
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
def _(engine2, mo, salary):
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
def _(engine2, mo, salary):
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
def _(engine2, mo, salary):
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
def _(engine2, mo, salary):
    _df = mo.sql(
        f"""
        SELECT MAX(Amount) AS Maximum FROM salary;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo, salary):
    salaryTeams = mo.sql(
        f"""
        SELECT Tm, ROUND(AVG(Amount)/1000000,1) as AVGSalary FROM salary GROUP BY Tm;
        """,
        engine=engine2
    )
    return (salaryTeams,)


@app.cell
def _(salaryTeams):
    salaryTeams.plot(kind="bar", x="Tm", y="AVGSalary")
    return


@app.cell
def _(engine2, mo, players):
    playerCount = mo.sql(
        f"""
        SELECT Tm, Pos, COUNT(Player) as playerCount FROM players WHERE Tm IN ("GSW","OKC","CLE") GROUP BY Tm, Pos;
        """,
        engine=engine2
    )
    return (playerCount,)


@app.cell
def _(playerCount):
    playerCount.set_index(['Tm', 'Pos'])['playerCount'].unstack('Pos').plot(kind="bar")
    return


@app.cell
def _(engine2, mo, players, salary):
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
    salaryPos.plot(kind="bar", x="Pos")
    return


@app.cell
def _(engine2, mo, salary):
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
    ## Kurze Einführung ins NBA-Gehalts- und Kadersystem

    ### 1. Rookie-Verträge  
    - **Dauer & Höhe**  
      - Die meisten Neuankömmlinge (Rookies) erhalten vierjährige Verträge mit festgelegten Gehaltsskalen, basierend auf ihrer Draft-Position.  
      - Die ersten beiden Jahre sind garantiert, die letzten beiden Jahre sind Team-Optionen.  
    - **Beispiel**  
      - Ein Spieler, der als 1. Pick gedraftet wird, startet mit deutlich höherem Basisgehalt als ein 30. Pick.

    ### 2. Free Agency  
    - **Unrestricted Free Agents (UFA)**  
      - Verborgene Spieler können nach Vertragsende mit jedem Team verhandeln.  
    - **Restricted Free Agents (RFA)**  
      - Ihr aktuelles Team kann mit einem offer sheet eines anderen Teams mithalten („Right of First Refusal“).  
    - **Timing**  
      - Die Free Agency beginnt im Sommer (meist Anfang Juli), wenn die „moratorium period“ endet.

    ### 3. Salary Cap (Gehaltsobergrenze)  
    - **Hard Cap vs. Soft Cap**  
      - NBA arbeitet mit einem Soft Cap: Überschreitungen sind in engen Grenzen erlaubt (z. B. durch „Bird Rights“ für Bestands­spieler).  
    - **Luxussteuer**  
      - Teams, die deutlich über dem Cap liegen, zahlen pro zusätzlichem Dollar eine hohe Abgabe an die Liga – dies soll Ausgeglichenheit fördern.  
    - **Cap Room**  
      - Verfügbarer „Raum“ unter dem Cap entscheidet, wieviel ein Team maximal neu investieren kann, ohne Strafen zu riskieren.

    ### 4. Spielerpositionen & physische Anforderungen  
    | Position        | Hauptaufgaben                                    | Typische Körpermaße (NBA-Durchschnitt)      |
    |-----------------|--------------------------------------------------|---------------------------------------------|
    | Point Guard     | Spielaufbau, Passen, Tempo kontrollieren         | 1,88 m; 85 kg                               |
    | Shooting Guard  | Scoring, Perimeter-Defense                       | 1,96 m; 90 kg                               |
    | Small Forward   | Vielseitigkeit: Scoring, Rebounding, Verteidigen | 2,01 m; 98 kg                               |
    | Power Forward   | Inside-Scoring, Rebounds, Pick-and-Roll          | 2,06 m; 104 kg                              |
    | Center          | Rim-Protection, Rebounds, Post-Play              | 2,11 m; 112 kg                              |

    **Physische Voraussetzungen**  
    - **Athletik**: Sprungkraft, Schnelligkeit und Wendigkeit sind für Guards essenziell.  
    - **Körperkraft**: Große, kräftige Spieler (Forwards/Centers) benötigen Explosivkraft für Rebounds und Verteidigung im Low-Post.  
    - **Ausdauer**: 48 Minuten hartes Tempo erfordert hohe kardiovaskuläre Fitness.

    ---

    > Diese Grundlagen helfen, Zusammenhänge zwischen **Gehalt**, **Alter** und **Kadergröße** zu interpretieren:  
    > - Teams mit größerem Cap Room können teurere Veteranen verpflichten.  
    > - Junge Rookies verdienen zunächst weniger, ihr Cap Value steigt aber mit Leistung.  
    > - Die Balance zwischen erfahrenen, gut bezahlten Stars und günstigen Rookies bestimmt Kaderstruktur und Gehaltsverteilung.  


    ## 🔍 1. Beziehung zwischen Alter und Gehalt untersuchen
    **Ziel:** Herausfinden, ob ältere Spieler tendenziell mehr oder weniger verdienen.

    **Analyseideen:**

    - Streudiagramm oder Korrelationsanalyse (Alter vs. Durchschnittsgehalt)
    - Gruppierung nach Altersklassen (z. B. <25, 25–30, 30–35, >35)
    """
    )
    return


@app.cell
def _(engine2, mo, players, salary):
    ageSalary = mo.sql(
        f"""
        -- 1. Beziehung zwischen Alter und Gehalt untersuchen
        SELECT players.Tm, players.Player, salary.Amount, players.Age, players.Pos FROM players LEFT JOIN salary on players.Player = salary.Player WHERE Amount > 0
         GROUP BY players.Player
        """,
        engine=engine2
    )
    return (ageSalary,)


@app.cell
def _(ageSalary):
    import matplotlib.pyplot as plt

    cats    = ageSalary['Pos'].unique()
    palette = dict(zip(cats, plt.cm.tab10.colors))
    ageSalary['col'] = ageSalary['Pos'].map(palette)

    ageSalary.plot(kind="scatter", x="Age", y="Amount", c=ageSalary['col'])

    for Pos, col in palette.items():
        plt.scatter([], [], c=[col], label=Pos)
    plt.legend(title='Position')
    return (plt,)


@app.cell
def _(engine2, mo, players, salary):
    ageBrackets = mo.sql(
        f"""
        SELECT
                players.Player,
                salary.Amount,
                CASE
                    WHEN players.Age BETWEEN 15 AND 20 THEN '15-20'
                    WHEN players.Age BETWEEN 21 AND 25 THEN '21-25'
                    WHEN players.Age BETWEEN 26 AND 30 THEN '26-30'
                    WHEN players.Age BETWEEN 31 AND 35 THEN '31-35'
                    WHEN players.Age BETWEEN 36 AND 40 THEN '36-40'
                    ELSE '40+'
                END AS AgeGroup,
                players.Pos
            FROM
                players
            LEFT JOIN
                salary ON players.Player = salary.Player
            WHERE
                Amount > 0
            GROUP BY
                players.Player
        """,
        engine=engine2
    )
    return (ageBrackets,)


@app.cell
def _(ageBrackets, plt):
    ageBrackets.plot.box(column="Amount", by="AgeGroup", title="Salary Distribution by Age Group", figsize=(8,4))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## ⚽ 2. Gehaltsunterschiede je nach Spielerposition
    **Ziel:** Ermitteln, wie sich die Gehälter zwischen verschiedenen Spielerpositionen unterscheiden.

    **Analyseideen:**

    - Balkendiagramme oder Boxplots der Gehälter nach Position
    - Vergleich von Mittelwert, Median, Perzentilen je Position
    """
    )
    return


@app.cell
def _(ageSalary, plt):
    ageSalary.plot.box(column="Amount", by="Pos", title="Salary Distribution by Position", figsize=(8,4))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 🤝 3. Zusammenhang zwischen Teamgröße und durchschnittlichem Teamgehalt
    **Ziel:** Analysieren, ob Teams mit mehr Spielern im Durchschnitt höhere oder niedrigere Gehälter zahlen.

    **Analyseideen:**

    - Aggregation pro Team: Spieleranzahl & Durchschnittsgehalt berechnen
    - Scatterplot (Teamgröße vs. Durchschnittsgehalt)
    """
    )
    return


@app.cell
def _(Salary, engine2, mo):
    rosterSizeSalary = mo.sql(
        f"""
        SELECT Tm, COUNT(Player) AS playerCount, AVG(Amount) AS AvgSalary FROM Salary GROUP BY Tm;
        """,
        engine=engine2
    )
    return (rosterSizeSalary,)


@app.cell
def _(rosterSizeSalary):
    rosterSizeSalary.plot(kind="scatter", x="playerCount", y="AvgSalary", title="Team Size vs. Average Salary")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 📊 4. Gehaltsverteilung mittels Perzentilen verstehen
    **Ziel:** Die Verteilung der Gehälter besser begreifen und zentrale Lagen analysieren.

    **Analyseideen:**

    - Berechnung von Perzentilen (z. B. 10., 25., 50., 75., 90.)
    - Boxplot zur Visualisierung
    """
    )
    return


@app.cell
def _(engine2, mo, salary):
    salaryPercentiles = mo.sql(
        f"""
        SELECT AVG(Amount) AS Amount, (ROUND(1.0*row / (SELECT COUNT(*) FROM salary),2)) AS Percentile FROM 
        (SELECT DISTINCT(Player), Tm, Amount, ROW_NUMBER () OVER (ORDER BY Amount) as row FROM salary)
        WHERE Percentile IN (
            0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
        )
        GROUP BY Percentile
        """,
        engine=engine2
    )
    return (salaryPercentiles,)


@app.cell
def _(salaryPercentiles):
    salaryPercentiles.plot(kind="bar", x="Percentile", y="Amount", figsize=(8,4))
    return


@app.cell
def _(ageSalary, plt):
    ageSalary.plot.box(column="Amount", by="Tm", title="Salary Distribution by Team", figsize=(8,4))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 💸 5. Top-N-verdienende Spieler identifizieren
    **Ziel:** Die höchsten Gehälter im Datensatz sichtbar machen.

    **Analyseideen:**

    - Sortierung nach Gehalt, Auswahl der Top-N
    - Darstellung in Tabelle oder Balkendiagramm
    - Analyse: Welche Positionen und Teams dominieren die Top-N?
    """
    )
    return


@app.cell
def _(engine2, mo, salary):
    _df = mo.sql(
        f"""
        -- TOP 3 per Team
        SELECT
            Tm,
            Player,
            Amount
        FROM (
            SELECT
                Tm,
                Player,
                Amount,
                RANK() OVER (PARTITION BY Tm ORDER BY Amount DESC) AS rank_within_team
            FROM
                salary
        ) AS subquery
        WHERE rank_within_team <= 3
        ORDER BY Tm, Amount DESC;
        """,
        engine=engine2
    )
    return


@app.cell
def _(engine2, mo, players, salary):
    _df = mo.sql(
        f"""
        -- TOP 3 Per Position
            SELECT
                Pos,
                Player,
                Amount
            FROM (
                SELECT
                    p.Pos,
                    s.Player,
                    s.Amount,
                    DENSE_RANK() OVER (PARTITION BY p.Pos ORDER BY s.Amount DESC) AS rank_within_position
                FROM
                    salary s
                JOIN
                    players p ON s.Player = p.Player
            ) AS subquery
            WHERE rank_within_position <= 3
                GROUP BY Player
            ORDER BY Pos, Amount DESC;
        """,
        engine=engine2
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 📈 6. Altersverteilung der Spieler analysieren
    **Ziel:** Einblick in die Altersstruktur des Spielerkaders gewinnen.

    **Analyseideen:**

    - Histogramm der Spieleralter
    - Kennzahlen berechnen (Durchschnitt, Median, Min, Max, Standardabweichung)
    - Altersgruppen bilden und visuell vergleichen
    """
    )
    return


@app.cell(hide_code=True)
def _(ageSalary):
    ageSalary["Age"].plot(kind="hist", bins=20, title="Age Distribution of Players", figsize=(8,4))
    return


@app.cell
def _(ageSalary):
    ageSalary
    return


@app.cell
def _(ageSalary, plt):
    ageSalary.plot.box(column="Amount", by="Pos", title="Salary Distribution by Team", figsize=(8,4))
    plt.show()
    return


@app.cell
def _(ageSalary, mo):
    posSelect = mo.ui.dropdown(ageSalary["Pos"], value = "C")
    return (posSelect,)


@app.cell
def _(ageSalary, mo, posSelect):
    mo.hstack([posSelect, ageSalary[ageSalary["Pos"] == posSelect.value]["Age"].plot(kind="hist", bins=[18,20,22,24,26,28,30,32,34,36,38,40], title=f"Age Distribution Position {posSelect.value}", figsize=(8,4))])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
