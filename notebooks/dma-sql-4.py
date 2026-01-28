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
def _():
    import polars as pl

    # Echte Shipman-Daten von der Website laden
    url = "https://chrisflath.github.io/notebooks/public/todesfaelle.csv"
    todesfaelle = pl.read_csv(url)
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
        SELECT
            Arzt,
            ROUND(AVG(Alter), 1) AS Durchschnittsalter,
            MIN(Alter) AS Jüngster,
            MAX(Alter) AS Ältester
        FROM todesfaelle
        GROUP BY Arzt
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
        ref_long.to_pandas(),
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
        hourly.to_pandas(),
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
        benford_analyse.to_pandas(),
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
        SELECT
            CAST(SUBSTR(CAST(CAST(betrag AS INT) AS TEXT), 1, 1) AS INT)
                AS erste_ziffer,
            COUNT(*) AS anzahl,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rechnungen_verdächtig WHERE betrag >= 10), 1) AS prozent
        FROM rechnungen_verdächtig
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
        ---

        ### 🔴 2.5 Debugging: Fehlerhafte Benford-Analyse

        Diese Abfrage hat mehrere Probleme. Finde und erkläre sie:
        """
    )
    return


@app.cell
def _(mo, rechnungen):
    # Was ist hier falsch?
    _df = mo.sql(
        f"""
        SELECT
            SUBSTR(betrag, 1, 1) AS erste_ziffer,
            COUNT(*)
        FROM rechnungen
        GROUP BY erste_ziffer
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
def _(deaths, mo, rechnungen):
    # Eigene Analyse hier:
    _df = mo.sql(
        f"""
        SELECT * FROM deaths LIMIT 5
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

        **Nächste Session:** JOINs – Mehrere Tabellen verknüpfen
        """
    )
    return


if __name__ == "__main__":
    app.run()
