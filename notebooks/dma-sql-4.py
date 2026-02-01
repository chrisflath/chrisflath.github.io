# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "polars",
#     "plotly",
# ]
# ///

import marimo

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 4: CRISP-DM & Fallstudien",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 4: CRISP-DM & Fallstudien

        **Kursfahrplan:** **▸ I: SQL-Grundlagen (S1–4)** · II: Datenmodellierung (S5–7) · III: Fortgeschrittenes SQL (S8–9) · IV: Datenanalyse (S10–13)

        Die gleichen SQL-Werkzeuge (GROUP BY, COUNT, AVG), die wir in Sessions 1–3 für Bundesliga-Daten kennengelernt haben, funktionieren genauso für forensische Datenanalyse. SQL ist domänenunabhängig — das macht es so mächtig.

        In dieser Session lernen Sie:

        - Den **CRISP-DM** Prozess für strukturierte Datenanalyse
        - **Fallstudie Shipman**: Anomalieerkennung bei Mortalitätsdaten
        - **Fallstudie Benford**: Betrugserkennung durch Ziffernanalyse
        - SQL für **forensische Datenanalyse**

        **Aufgabentypen:**
        - 🟢 **Geführt**: Beispiel zum Nachvollziehen
        - 🟡 **Scaffolded**: Teillösung zum Ergänzen
        - 🔵 **Selbstständig**: Eigene Lösung schreiben
        - 🔴 **Debugging**: Fehler finden und beheben
        - 🟣 **Vorhersage**: Was wird das Ergebnis sein?

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## CRISP-DM: Der Analyseprozess

        ```
        Business Understanding → Data Understanding → Data Preparation
                ↑                                              ↓
           Deployment ← Evaluation ← Modeling
        ```

        1. **Business Understanding**: Was ist das Problem?
        2. **Data Understanding**: Welche Daten haben wir?
        3. **Data Preparation**: Daten bereinigen und transformieren
        4. **Modeling**: Analyse durchführen
        5. **Evaluation**: Ergebnisse prüfen
        6. **Deployment**: Lösung einsetzen
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Fallstudie I: Dr. Harold Shipman

        **Hintergrund:**
        - Britischer Hausarzt (1946-2004)
        - Mindestens 215 Patienten ermordet
        - Erst 1998 durch Testamentsfälschung entdeckt
        - Statistische Anomalien waren jahrelang sichtbar!

        **Analysefragen:**
        - Wie viele Todesfälle pro Arzt?
        - Zu welchen Uhrzeiten sterben Patienten?
        - Welche Alters-/Geschlechtsverteilung?
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Daten: Todesfälle

        Wir laden echte (anonymisierte) Mortalitätsdaten aus der Shipman-Untersuchung:
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    import polars as pl

    try:
        # Echte Shipman-Daten von der Website laden
        url = "https://chrisflath.github.io/notebooks/public/todesfaelle.csv"
        todesfaelle = pl.read_csv(url)
    except Exception:
        todesfaelle = pl.DataFrame({
            "Arzt": (["Shipman"] * 15 + ["Referenz"] * 10),
            "Geschlecht": ["W", "W", "M", "W", "W", "M", "W", "W", "M", "W",
                           "W", "M", "W", "W", "W",
                           "W", "M", "W", "M", "W", "W", "M", "W", "M", "W"],
            "Alter": [76, 82, 71, 79, 84, 68, 91, 77, 73, 88,
                      80, 65, 85, 74, 81,
                      85, 79, 72, 66, 90, 78, 81, 87, 69, 83],
            "Todesstunde": [14, 15, 13, 14, 16, 15, 14, 13, 15, 14,
                            16, 14, 15, 13, 14,
                            3, 22, 8, 17, 1, 11, 19, 6, 14, 23],
        })
        mo.callout(mo.md("**Hinweis:** Todesfälle-Daten konnten nicht geladen werden. Es werden Beispieldaten verwendet."), kind="warn")

    return pl, todesfaelle


@app.cell
def _(mo, todesfaelle):
    mo.md(f"**{len(todesfaelle)} Todesfälle aus der Shipman-Untersuchung:**")
    todesfaelle


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 1.1 Geführt: Todesfälle pro Arzt

        Die einfachste Anomalie: Wer hat die meisten Todesfälle?
        """
    )
    return


@app.cell
def _(mo, todesfaelle):
    _df = mo.sql(
        f"""
        SELECT
            Arzt,
            COUNT(*) AS Anzahl
        FROM todesfaelle
        GROUP BY Arzt
        ORDER BY Anzahl DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Shipman hat 3x so viele Todesfälle wie seine Kollegen!

        ---

        ### 🟢 1.2 Geführt: Todesfälle nach Tageszeit

        Natürliche Todesfälle verteilen sich über den Tag. Mordopfer sterben oft während der "Arbeitszeit" des Täters.
        """
    )
    return


@app.cell
def _(mo, todesfaelle):
    _df = mo.sql(
        f"""
        SELECT
            Arzt,
            CASE
                WHEN Todesstunde BETWEEN 9 AND 17 THEN 'Praxiszeit (9-17)'
                ELSE 'Außerhalb'
            END AS Zeitraum,
            COUNT(*) AS Anzahl
        FROM todesfaelle
        GROUP BY Arzt, Zeitraum
        ORDER BY Arzt, Zeitraum
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Bei Shipman sterben fast alle Patienten während der Praxiszeit!

        ---

        ### 🟡 1.3 Scaffolded: Geschlechterverteilung

        Ergänze die Abfrage, um die Geschlechterverteilung pro Arzt zu zeigen:
        """
    )
    return


@app.cell
def _(mo, todesfaelle):
    # Ergänze die GROUP BY Klausel
    _df = mo.sql(
        f"""
        SELECT
            Arzt,
            Geschlecht,
            COUNT(*) AS Anzahl
        FROM todesfaelle
        GROUP BY ???
        ORDER BY Arzt, Geschlecht
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Arzt,
    Geschlecht,
    COUNT(*) AS Anzahl
FROM todesfaelle
GROUP BY Arzt, Geschlecht
ORDER BY Arzt, Geschlecht
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 1.4 Selbstständig: Durchschnittsalter

        Berechne das Durchschnittsalter der verstorbenen Patienten pro Arzt:
        """
    )
    return


@app.cell
def _(mo, todesfaelle):
    # Deine Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: AVG(), MIN(), MAX() mit GROUP BY Arzt
        -- Erwartete Spalten: Arzt, Durchschnittsalter, Jüngster, Ältester
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Arzt,
    ROUND(AVG(Alter), 1) AS Durchschnittsalter,
    MIN(Alter) AS Jüngster,
    MAX(Alter) AS Ältester
FROM todesfaelle
GROUP BY Arzt
ORDER BY Durchschnittsalter DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟣 Aufgabe 1.5: Vorhersage — Altersverteilung

        **Bevor Sie die Abfrage ausführen:**

        Shipmans Opfer waren typischerweise ältere, alleinstehende Patientinnen.

        Was erwarten Sie?
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pred_age = mo.ui.radio(
        options={
            "correct": "Shipmans Opfer sind im Schnitt deutlich älter",
            "wrong1": "Alle Ärzte haben ähnliche Altersverteilungen",
            "wrong2": "Shipmans Opfer sind jünger als bei anderen Ärzten"
        },
        label="**Vorhersage:** Wie unterscheidet sich das Durchschnittsalter der Verstorbenen bei Shipman vs. anderen Ärzten?"
    )
    pred_age
    return (pred_age,)


@app.cell(hide_code=True)
def _(mo, pred_age):
    if pred_age.value == "correct":
        mo.output.replace(mo.md("✅ **Richtig!** Shipmans Opfer waren überwiegend ältere Patientinnen — das ist eines der Muster, das die Ermittler schließlich auf seine Spur brachte."))
    elif pred_age.value:
        mo.output.replace(mo.md("🤔 Nicht ganz. Denken Sie daran: Shipman wählte gezielt ältere, alleinstehende Patientinnen als Opfer aus."))
    return


@app.cell
def _(mo, todesfaelle):
    _df = mo.sql(
        f"""
        SELECT
            Arzt,
            ROUND(AVG(Alter), 1) AS Durchschnittsalter,
            MIN(Alter) AS Jüngster,
            MAX(Alter) AS Ältester
        FROM todesfaelle
        GROUP BY Arzt
        ORDER BY Durchschnittsalter DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Visualisierung der Shipman-Anomalien

        ### Referenzverteilung: Todesfälle nach Tageszeit

        Die folgende Grafik zeigt die prozentuale Verteilung der Todesfälle nach Tageszeit.
        Die **Referenzverteilung** stammt aus dem Buch *Art of Statistics* (David Spiegelhalter)
        und zeigt das typische Muster anderer Ärzte im Vergleich zu Shipman.
        """
    )
    return


@app.cell
def _(pl):
    import plotly.express as px

    # Referenzdaten: Art of Statistics (Spiegelhalter), Figure 0.2
    # Prozentuale Verteilung der Todesfälle nach Stunde
    referenz = pl.DataFrame({
        "Stunde": list(range(24)),
        "Shipman": [2.6, 1.0, 2.6, 3.0, 0.3, 1.2, 2.9, 1.8, 3.6, 2.6,
                    4.6, 5.8, 2.0, 9.0, 14.1, 13.0, 9.0, 5.8, 3.8, 2.9,
                    3.6, 0.8, 3.6, 2.0],
        "Vergleichsgruppe": [1.1, 3.0, 3.1, 3.8, 4.0, 4.3, 4.2, 4.1, 3.4, 5.6,
                             5.5, 5.8, 4.0, 3.8, 2.0, 3.4, 6.6, 5.2, 3.3, 5.0,
                             4.1, 3.8, 2.9, 4.1]
    })

    # Daten in Long-Format für Plotly
    ref_long = referenz.unpivot(
        index="Stunde",
        on=["Shipman", "Vergleichsgruppe"],
        variable_name="Gruppe",
        value_name="Prozent"
    )

    fig_ref = px.line(
        ref_long,
        x="Stunde",
        y="Prozent",
        color="Gruppe",
        title="Verteilung der Todesfälle nach Tageszeit (%, Referenzdaten)",
        labels={"Stunde": "Todesstunde", "Prozent": "Anteil (%)", "Gruppe": ""},
        color_discrete_map={"Shipman": "#d62728", "Vergleichsgruppe": "#1f77b4"},
        markers=True
    )
    fig_ref.update_layout(xaxis=dict(dtick=1))
    fig_ref
    return fig_ref, px, referenz


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Die Vergleichsgruppe zeigt eine relativ gleichmäßige Verteilung
        über den Tag. Shipmans Todesfälle konzentrieren sich dagegen stark auf die
        Nachmittagsstunden (13-16 Uhr) -- genau seine typische Hausbesuchszeit.

        ---

        ### Unsere Daten: Todesfälle nach Tageszeit
        """
    )
    return


@app.cell
def _(mo, px, todesfaelle):
    # Todesfälle nach Stunde und Arzt aus unseren Daten
    hourly = mo.sql(
        f"""
        SELECT Arzt, Todesstunde, COUNT(*) as Anzahl
        FROM todesfaelle
        GROUP BY Arzt, Todesstunde
        """
    )

    fig_hourly = px.bar(
        hourly,
        x="Todesstunde",
        y="Anzahl",
        color="Arzt",
        barmode="group",
        title="Todesfälle nach Tageszeit (unsere Daten)",
        labels={"Todesstunde": "Stunde", "Anzahl": "Anzahl", "Arzt": "Arzt"}
    )
    fig_hourly
    return fig_hourly, hourly


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Fallstudie II: Benford's Law

        **Das Gesetz der ersten Ziffer:**

        In natürlichen Datensätzen beginnen Zahlen überraschend häufig mit kleinen Ziffern:

        | Ziffer | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
        |--------|---|---|---|---|---|---|---|---|---|
        | Erwartet (%) | 30.1 | 17.6 | 12.5 | 9.7 | 7.9 | 6.7 | 5.8 | 5.1 | 4.6 |

        **Anwendung:** Wenn Zahlen manipuliert/erfunden werden, weichen sie oft von dieser Verteilung ab!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Beispieldaten: Rechnungsbeträge

        Wir haben zwei Datensätze:
        - **Echte Rechnungen** (sollten Benford folgen)
        - **Verdächtige Rechnungen** (gleichmäßiger verteilt)
        """
    )
    return


@app.cell(hide_code=True)
def _(pl):
    import random
    random.seed(42)

    # Echte Rechnungen: Folgen Benford (exponentiell verteilt)
    import math
    echte_betraege = [round(10 ** (random.uniform(1, 4)), 2) for _ in range(200)]

    # Verdächtige Rechnungen: Gleichmäßiger verteilt (wie von Menschen "erfunden")
    verdächtige_betraege = [random.randint(10, 999) + random.random() for _ in range(200)]

    rechnungen_echt = pl.DataFrame({
        "rechnung_id": list(range(1, 201)),
        "betrag": echte_betraege,
        "kategorie": ["echt"] * 200
    })

    rechnungen_verdächtig = pl.DataFrame({
        "rechnung_id": list(range(201, 401)),
        "betrag": verdächtige_betraege,
        "kategorie": ["verdächtig"] * 200
    })

    # Kombiniert
    rechnungen = pl.concat([rechnungen_echt, rechnungen_verdächtig])
    return math, rechnungen, rechnungen_echt, rechnungen_verdächtig, random


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 2.0 Geführt: Verteilung der Rechnungsbeträge

        Bevor wir die Ziffern analysieren — wie sehen die Beträge insgesamt aus?
        Ein **Histogramm** zeigt die Verteilung auf einen Blick:
        """
    )
    return


@app.cell
def _(px, rechnungen):
    fig_hist = px.histogram(
        rechnungen,
        x="betrag",
        color="kategorie",
        barmode="overlay",
        opacity=0.6,
        nbins=40,
        title="Verteilung der Rechnungsbeträge",
        labels={"betrag": "Betrag (€)", "kategorie": "Kategorie"}
    )
    fig_hist


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Echte Rechnungen sind rechtsschief verteilt (viele kleine, wenige große Beträge).
        Verdächtige Rechnungen sind gleichmäßiger verteilt — ein erstes Warnsignal!

        ---

        ### 🟢 2.1 Geführt: Erste Ziffer extrahieren

        Um Benford anzuwenden, müssen wir die erste Ziffer jeder Zahl extrahieren:
        """
    )
    return


@app.cell
def _(mo, rechnungen):
    _df = mo.sql(
        f"""
        SELECT
            betrag,
            CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT)
                AS erste_ziffer
        FROM rechnungen
        WHERE betrag >= 10
        LIMIT 20
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 2.2 Geführt: Benford-Verteilung berechnen

        Jetzt zählen wir, wie oft jede Ziffer vorkommt:
        """
    )
    return


@app.cell
def _(mo, rechnungen):
    benford_analyse = mo.sql(
        f"""
        SELECT
            kategorie,
            CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT)
                AS erste_ziffer,
            COUNT(*) AS anzahl
        FROM rechnungen
        WHERE betrag >= 10
        GROUP BY kategorie, erste_ziffer
        ORDER BY kategorie, erste_ziffer
        """
    )
    return (benford_analyse,)


@app.cell
def _(benford_analyse, px):
    # Visualisierung der Benford-Verteilung
    fig_benford = px.bar(
        benford_analyse,
        x="erste_ziffer",
        y="anzahl",
        color="kategorie",
        barmode="group",
        title="Benford-Analyse: Echte vs. Verdächtige Rechnungen",
        labels={"erste_ziffer": "Erste Ziffer", "anzahl": "Anzahl", "kategorie": "Kategorie"}
    )

    # Erwartete Benford-Linie hinzufügen wäre hier möglich
    fig_benford
    return (fig_benford,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:**
        - Echte Rechnungen: Mehr 1er und 2er (wie Benford vorhersagt)
        - Verdächtige Rechnungen: Gleichmäßiger verteilt (Warnsignal!)

        ---

        ### 🟡 2.3 Scaffolded: Prozentuale Verteilung

        Ergänze die Abfrage, um den Prozentanteil jeder Ziffer zu berechnen:
        """
    )
    return


@app.cell
def _(mo, rechnungen_echt):
    # Ergänze die Berechnung des Prozentanteils
    _df = mo.sql(
        f"""
        SELECT
            CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT)
                AS erste_ziffer,
            COUNT(*) AS anzahl,
            ROUND(COUNT(*) * 100.0 / ???, 1) AS prozent
        FROM rechnungen_echt
        WHERE betrag >= 10
        GROUP BY erste_ziffer
        ORDER BY erste_ziffer
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT)
        AS erste_ziffer,
    COUNT(*) AS anzahl,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rechnungen_echt WHERE betrag >= 10), 1) AS prozent
FROM rechnungen_echt
WHERE betrag >= 10
GROUP BY erste_ziffer
ORDER BY erste_ziffer
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 2.3b: Benford-Abweichung berechnen (scaffolded)

        Vergleiche die beobachteten Prozente mit den theoretischen Benford-Werten.
        Ergänze die fehlende Berechnung der Abweichung:
        """
    )
    return


@app.cell
def _(mo, rechnungen_echt):
    # Ergänze: ABS(b.prozent - e.erwartet) berechnet die Abweichung
    _df = mo.sql(
        f"""
        WITH beobachtet AS (
            SELECT
                CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT) AS erste_ziffer,
                COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rechnungen_echt WHERE betrag >= 10) AS prozent
            FROM rechnungen_echt
            WHERE betrag >= 10
            GROUP BY erste_ziffer
        ),
        benford AS (
            SELECT 1 AS ziffer, 30.1 AS erwartet UNION ALL
            SELECT 2, 17.6 UNION ALL SELECT 3, 12.5 UNION ALL
            SELECT 4, 9.7 UNION ALL SELECT 5, 7.9 UNION ALL
            SELECT 6, 6.7 UNION ALL SELECT 7, 5.8 UNION ALL
            SELECT 8, 5.1 UNION ALL SELECT 9, 4.6
        )
        SELECT
            b.erste_ziffer,
            ROUND(b.prozent, 1) AS beobachtet_pct,
            e.erwartet AS benford_pct,
            ROUND(???, 1) AS abweichung
        FROM beobachtet b
        JOIN benford e ON b.erste_ziffer = e.ziffer
        ORDER BY ???
        -- Ergänze: ABS(b.prozent - e.erwartet) AS abweichung, ORDER BY abweichung DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH beobachtet AS (
    SELECT
        CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT) AS erste_ziffer,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rechnungen_echt WHERE betrag >= 10) AS prozent
    FROM rechnungen_echt
    WHERE betrag >= 10
    GROUP BY erste_ziffer
),
benford AS (
    SELECT 1 AS ziffer, 30.1 AS erwartet UNION ALL
    SELECT 2, 17.6 UNION ALL SELECT 3, 12.5 UNION ALL
    SELECT 4, 9.7 UNION ALL SELECT 5, 7.9 UNION ALL
    SELECT 6, 6.7 UNION ALL SELECT 7, 5.8 UNION ALL
    SELECT 8, 5.1 UNION ALL SELECT 9, 4.6
)
SELECT
    b.erste_ziffer,
    ROUND(b.prozent, 1) AS beobachtet_pct,
    e.erwartet AS benford_pct,
    ROUND(ABS(b.prozent - e.erwartet), 1) AS abweichung
FROM beobachtet b
JOIN benford e ON b.erste_ziffer = e.ziffer
ORDER BY abweichung DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 2.4 Selbstständig: Abweichung von Benford

        Berechne für die verdächtigen Rechnungen:
        1. Die erste Ziffer
        2. Den Prozentanteil
        3. Die erwartete Benford-Verteilung (30.1%, 17.6%, 12.5%, ...)
        """
    )
    return


@app.cell
def _(mo, rechnungen_verdächtig):
    # Deine Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: Wie in 2.3, aber für rechnungen_verdächtig
        -- 1. Erste Ziffer: CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT)
        -- 2. Prozentanteil: COUNT(*) * 100.0 / (SELECT COUNT(*) ...)
        -- Erwartete Spalten: erste_ziffer, anzahl, prozent
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT)
        AS erste_ziffer,
    COUNT(*) AS anzahl,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rechnungen_verdächtig WHERE betrag >= 10), 1) AS prozent
FROM rechnungen_verdächtig
WHERE betrag >= 10
GROUP BY erste_ziffer
ORDER BY erste_ziffer
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ### 🔴 2.5 Debugging: Fehlerhafte Benford-Analyse

        Diese Abfrage hat mehrere Probleme. Finde und erkläre sie:

        ```sql
        SELECT
            SUBSTR(betrag, 1, 1) AS erste_ziffer,
            COUNT(*)
        FROM rechnungen
        GROUP BY erste_ziffer
        ```
        """
    )
    return


@app.cell
def _(mo, rechnungen):
    # Fehlerhafter Code (siehe Markdown oben):
    #   SUBSTR(betrag, 1, 1) AS erste_ziffer, COUNT(*)
    # Korrigierte Version:
    _df = mo.sql(
        f"""
        SELECT
            CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT)
                AS erste_ziffer,
            COUNT(*) AS anzahl
        FROM rechnungen
        WHERE betrag >= 10
        GROUP BY erste_ziffer
        ORDER BY erste_ziffer
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Probleme:**
        1. `betrag` ist numerisch, muss zu TEXT konvertiert werden
        2. Negative/kleine Zahlen werden nicht behandelt
        3. Dezimalzahlen < 10 haben keine führende Ziffer
        4. COUNT(*) braucht einen Alias

        ---

        ### 🟣 2.6 Vorhersage: Welche Daten folgen Benford?

        Schätze, welche dieser Datensätze Benford's Law folgen würden:

        1. Aktienkurse aller DAX-Unternehmen
        2. Hausnummern in einer Stadt
        3. Körpergrößen von Studierenden
        4. Instagram-Followerzahlen von Influencern
        5. Lottozahlen der letzten 10 Jahre
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Antworten:**
        1. ✅ Ja (wachsen multiplikativ)
        2. ❌ Nein (zugewiesen, nicht natürlich gewachsen)
        3. ❌ Nein (enger Wertebereich, normalverteilt)
        4. ✅ Ja (exponentielles Wachstum)
        5. ❌ Nein (Zufallszahlen in festem Bereich)

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_crisp = mo.ui.radio(
        options={
            "correct": "Business Understanding → Data Understanding → Data Preparation → Modeling → Evaluation → Deployment",
            "wrong1": "Data Understanding → Data Preparation → Business Understanding → Modeling → Evaluation → Deployment",
            "wrong2": "Business Understanding → Modeling → Data Preparation → Evaluation → Data Understanding → Deployment",
            "wrong3": "Data Preparation → Data Understanding → Modeling → Business Understanding → Deployment → Evaluation"
        },
        label="**Quiz:** In welcher Reihenfolge werden die CRISP-DM Phasen typischerweise durchlaufen?"
    )
    quiz_crisp
    return (quiz_crisp,)


@app.cell(hide_code=True)
def _(quiz_crisp, mo):
    if quiz_crisp.value == "correct":
        mo.output.replace(mo.md("✅ **Richtig!** CRISP-DM beginnt immer mit dem **Business Understanding** — erst das Problem verstehen, dann die Daten. In der Praxis ist der Prozess allerdings iterativ: Man springt oft zwischen Phasen zurück."))
    elif quiz_crisp.value:
        mo.output.replace(mo.md("❌ Nicht ganz. CRISP-DM beginnt immer mit **Business Understanding** — man muss zuerst das Problem verstehen, bevor man die Daten analysiert."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Freie Exploration

        Probiere eigene Analysen:

        ### Shipman-Daten:
        - Berechne den Prozentsatz weiblicher Opfer pro Arzt
        - Finde heraus, ob bestimmte Uhrzeiten besonders auffällig sind
        - Erstelle eine Altersverteilung als Histogramm

        ### Benford-Daten:
        - Vergleiche die zweite Ziffer (auch die hat eine erwartete Verteilung!)
        - Berechne den Chi-Quadrat-Abstand zur erwarteten Verteilung
        - Visualisiere die Abweichung
        """
    )
    return


@app.cell
def _(mo, rechnungen, todesfaelle):
    # Eigene Analyse hier:
    _df = mo.sql(
        f"""
        SELECT * FROM todesfaelle LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        ### CRISP-DM
        | Phase | Beschreibung |
        |-------|--------------|
        | Business Understanding | Problem definieren |
        | Data Understanding | Daten erkunden |
        | Data Preparation | Daten bereinigen |
        | Modeling | Analyse durchführen |
        | Evaluation | Ergebnisse prüfen |
        | Deployment | Lösung einsetzen |

        ### Anomalieerkennung (Shipman)
        - Vergleiche Kennzahlen zwischen Gruppen
        - Achte auf zeitliche Muster
        - Demografische Verteilungen prüfen

        ### Benford's Law
        - Erste Ziffer mit `SUBSTR(CAST(... AS TEXT), 1, 1)`
        - Erwartung: 30% beginnen mit 1
        - Abweichungen deuten auf Manipulation hin

        **Nächste Session:** Datenmodellierung – Von Anomalien zum ER-Modell
        """
    )
    return


if __name__ == "__main__":
    app.run()
