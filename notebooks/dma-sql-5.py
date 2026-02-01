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
    app_title="DMA Session 5: Warum mehrere Tabellen?",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 5: Warum mehrere Tabellen?

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · **▸ II: Datenmodellierung (S5–8)** · III: Fortgeschrittenes SQL (S9–10) · IV: Datenanalyse (S11–14)

        In dieser Session lernen Sie:

        - Probleme der **Redundanz** in Datenbanken
        - Die drei **Anomalien**: Änderungs-, Einfüge-, Löschanomalie
        - Warum wir Daten auf **mehrere Tabellen** aufteilen
        - Grundkonzepte: **Primärschlüssel** und **Fremdschlüssel**

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Die "Mega-Tabelle": Ein problematisches Design

        Stellen wir uns vor, wir verwalten Spieler und ihre Vereine in **einer** Tabelle.
        Das scheint zunächst praktisch -- alles an einem Ort!
        """
    )
    return


@app.cell
def _():
    import polars as pl
    import plotly.express as px

    # Die "schlechte" Mega-Tabelle mit Redundanzen
    spieler_schlecht = pl.DataFrame({
        "Spieler": ["Müller", "Neuer", "Kimmich", "Sane", "Musiala",
                    "Wirtz", "Tah", "Frimpong",
                    "Füllkrug", "Nmecha"],
        "Position": ["Sturm", "Tor", "Mittelfeld", "Sturm", "Mittelfeld",
                     "Mittelfeld", "Abwehr", "Abwehr",
                     "Sturm", "Sturm"],
        "Verein": ["Bayern München", "Bayern München", "Bayern München",
                   "Bayern München", "Bayern München",
                   "Bayer Leverkusen", "Bayer Leverkusen", "Bayer Leverkusen",
                   "West Ham United", "West Ham United"],
        "Vereinsort": ["München", "München", "München", "München", "München",
                       "Leverkusen", "Leverkusen", "Leverkusen",
                       "London", "London"],
        "Stadion": ["Allianz Arena", "Allianz Arena", "Allianz Arena",
                    "Allianz Arena", "Allianz Arena",
                    "BayArena", "BayArena", "BayArena",
                    "London Stadium", "London Stadium"],
        "Gründungsjahr": [1900, 1900, 1900, 1900, 1900,
                          1904, 1904, 1904,
                          1895, 1895]
    })
    spieler_schlecht
    return pl, px, spieler_schlecht


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 2: Redundanz identifizieren

        ### Aufgabe 5.1: Wie oft wird jede Vereinsinformation gespeichert?

        Zählen Sie, wie oft jeder Verein in der Tabelle vorkommt.
        """
    )
    return


@app.cell
def _(mo, spieler_schlecht):
    _df = mo.sql(
        f"""
        SELECT
            Verein,
            Vereinsort,
            Stadion,
            COUNT(*) AS Anzahl_Wiederholungen
        FROM spieler_schlecht
        GROUP BY Verein, Vereinsort, Stadion
        ORDER BY Anzahl_Wiederholungen DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Sichtbar gemacht:** Das folgende Diagramm zeigt, wie oft jede Vereinsinformation
        in der Mega-Tabelle wiederholt wird. Jede Wiederholung über 1 ist reine Redundanz.
        """
    )
    return


@app.cell
def _(pl, px, spieler_schlecht):
    _redundanz = (
        spieler_schlecht
        .group_by("Verein")
        .len()
        .rename({"len": "Anzahl_Einträge"})
        .sort("Anzahl_Einträge")
    )
    px.bar(
        _redundanz,
        x="Anzahl_Einträge",
        y="Verein",
        color="Verein",
        orientation="h",
        title="Wie oft wird jeder Verein in der Mega-Tabelle gespeichert?",
        labels={"Anzahl_Einträge": "Anzahl Wiederholungen", "Verein": ""},
        color_discrete_sequence=["#003560", "#E87722", "#5B9BD5"],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Die Vereinsinformationen (Ort, Stadion, Gründungsjahr)
        werden für jeden Spieler wiederholt -- das ist **Redundanz**!

        Bayern München hat 5 Spieler, also werden "München" und "Allianz Arena"
        **5 Mal** gespeichert, obwohl es nur **ein** Verein ist.

        ---

        ### Aufgabe 5.2: Wie viel Speicherplatz "verschwenden" wir?

        Berechnen Sie die theoretische Redundanz:
        """
    )
    return


@app.cell
def _(mo, spieler_schlecht):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*) AS Gesamtzeilen,
            COUNT(DISTINCT Verein) AS Verschiedene_Vereine,
            COUNT(*) - COUNT(DISTINCT Verein) AS Redundante_Vereinseinträge
        FROM spieler_schlecht
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 5.2a: Redundanz pro Verein (scaffolded)

        Wie oft werden die Daten jedes Vereins wiederholt?
        Ergänze die fehlende Berechnung:
        """
    )
    return


@app.cell
def _(mo, spieler_schlecht):
    # Ergänze: COUNT(*) - 1 berechnet die redundanten Zeilen; GROUP BY Verein
    _df = mo.sql(
        f"""
        SELECT
            Verein,
            COUNT(*) AS Gesamt_Zeilen,
            ??? AS Redundante_Zeilen
        FROM spieler_schlecht
        GROUP BY ???
        ORDER BY Redundante_Zeilen DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        > **Vorhersage:** Stellen Sie sich vor, Bayern München benennt sein Stadion um. In wie vielen Zeilen der Mega-Tabelle müssten wir den Namen ändern? Was passiert, wenn wir eine Zeile vergessen?

        ---

        ## Phase 3: Anomalien erleben

        ### Aufgabe 5.3: Änderungsanomalie provozieren

        **Szenario:** Bayern München baut ein neues Stadion namens "FC Bayern Arena".

        Führen wir ein UPDATE durch -- aber "vergessen" wir absichtlich eine Zeile:
        """
    )
    return


@app.cell
def _(pl, spieler_schlecht):
    # "Fehlerhaftes" Update: Wir ändern nur 4 von 5 Bayern-Spielern
    spieler_nach_update = spieler_schlecht.with_columns(
        pl.when(
            (pl.col("Verein") == "Bayern München") & (pl.col("Spieler") != "Musiala")
        )
        .then(pl.lit("FC Bayern Arena"))
        .otherwise(pl.col("Stadion"))
        .alias("Stadion")
    )

    spieler_nach_update
    return (spieler_nach_update,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Problem erkannt?** Musiala spielt noch in der "Allianz Arena",
        während alle anderen Bayern-Spieler in der "FC Bayern Arena" sind!

        Das ist eine **Inkonsistenz** -- die Daten widersprechen sich.

        Prüfen wir das mit einer Abfrage:
        """
    )
    return


@app.cell
def _(mo, spieler_nach_update):
    _df = mo.sql(
        f"""
        SELECT DISTINCT Verein, Stadion
        FROM spieler_nach_update
        WHERE Verein = 'Bayern München'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Änderungsanomalie:** Bei redundanten Daten müssen Änderungen an
        **allen** Stellen durchgeführt werden. Vergisst man eine, entstehen
        Inkonsistenzen.

        ---

        ### Aufgabe 5.2b: Einfügeanomalie erleben

        **Szenario:** Was, wenn wir einen neuen Verein in unsere Datenbank aufnehmen wollen,
        aber noch keinen Spieler für diesen Verein haben?

        In der Mega-Tabelle geht das nicht -- jede Zeile **muss** einen Spieler enthalten,
        weil Spieler- und Vereinsdaten in derselben Tabelle stecken.
        """
    )
    return


@app.cell
def _(mo, spieler_schlecht):
    # Versuch: "1. FC Köln" ohne Spieler einfügen
    _df = mo.sql(
        f"""
        SELECT * FROM (
            SELECT * FROM spieler_schlecht
            UNION ALL
            SELECT
                NULL AS Spieler,
                NULL AS Position,
                '1. FC Köln' AS Verein,
                'Köln' AS Vereinsort,
                'RheinEnergieStadion' AS Stadion,
                1948 AS Gründungsjahr
        )
        ORDER BY Verein, Spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Problem erkannt?** Wir mussten `NULL`-Werte für `Spieler` und `Position` eintragen,
        weil die Tabelle diese Spalten in jeder Zeile erwartet. Das ist die **Einfügeanomalie**:

        - Wir können **keine Vereinsinformationen** speichern, solange kein Spieler existiert
        - Die `NULL`-Werte erzeugen unvollständige, schwer auswertbare Datensätze
        - Bei Abfragen wie `COUNT(Spieler)` oder `WHERE Position = 'Sturm'` führen die `NULL`-Einträge zu unerwartetem Verhalten

        > **Einfügeanomalie:** Neue Informationen können nicht hinzugefügt werden,
        > ohne gleichzeitig **andere, zusammenhanglose** Daten angeben zu müssen.

        ---

        ### Aufgabe 5.4: Löschanomalie erleben

        **Szenario:** Wirtz, Tah und Frimpong wechseln alle ins Ausland.
        Wir löschen sie aus unserer Tabelle.
        """
    )
    return


@app.cell
def _(pl, spieler_schlecht):
    # Zurück zur Original-Tabelle
    spieler_vor_delete = spieler_schlecht.clone()

    # Alle Leverkusen-Spieler löschen
    spieler_nach_delete = spieler_vor_delete.filter(
        pl.col("Verein") != "Bayer Leverkusen"
    )

    spieler_nach_delete
    return spieler_nach_delete, spieler_vor_delete


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Was ist passiert?** Wir haben alle Informationen über Bayer Leverkusen verloren!

        - Wo ist der Vereinssitz? Weg.
        - Wie heißt das Stadion? Weg.
        - Wann wurde der Verein gegründet? Weg.

        Prüfen wir, welche Vereine wir noch kennen:
        """
    )
    return


@app.cell
def _(mo, spieler_nach_delete):
    _df = mo.sql(
        f"""
        SELECT DISTINCT Verein, Vereinsort, Stadion
        FROM spieler_nach_delete
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Löschanomalie:** Beim Löschen von Daten gehen ungewollt
        **andere Informationen** verloren, die wir eigentlich behalten wollten.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_anomalie = mo.ui.radio(
        options={
            "correct": "Löschanomalie — Vereinsinformationen gingen verloren",
            "aenderung": "Änderungsanomalie — ein Verein ist nicht kohärent aktualisiert",
            "einfuege": "Einfügeanomalie — wir konnten nicht alle Infos auf einmal speichern",
            "normal": "Normalisierungsanomalie — die Tabelle ist nicht in 3NF",
        },
        label="**Quiz:** Wir haben alle Leverkusen-Spieler gelöscht. Jetzt wissen wir nicht mehr, wo Leverkusen liegt oder wie das Stadion heißt. Welche Anomalie ist das?"
    )
    quiz_anomalie
    return (quiz_anomalie,)


@app.cell(hide_code=True)
def _(quiz_anomalie, mo):
    if quiz_anomalie.value == "correct":
        mo.output.replace(mo.md("Richtig! Das ist die **Löschanomalie**: Beim Löschen von Spielerdaten gehen ungewollt auch die Vereinsinformationen verloren, weil beides in derselben Tabelle gespeichert ist."))
    elif quiz_anomalie.value:
        mo.output.replace(mo.md("Nicht ganz. Beim **Löschen** von Daten gehen *andere* Informationen verloren — das ist die Löschanomalie. Tipp: Der Name der Anomalie beschreibt die Aktion, die das Problem verursacht."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Pause: Zeit für Reflexion

        Bevor wir zur Lösung kommen, überlegen Sie:

        1. Warum passieren diese Probleme?
        2. Was haben Spieler und Vereine gemeinsam, das getrennt werden könnte?

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 5: Die Lösung -- Daten aufteilen

        Die Lösung ist einfach: **Jedes "Ding" bekommt seine eigene Tabelle!**

        - Spieler sind ein "Ding" (Entität)
        - Vereine sind ein anderes "Ding" (Entität)

        Erstellen wir zwei separate Tabellen:
        """
    )
    return


@app.cell
def _(pl):
    # Tabelle 1: Vereine (jeder Verein nur EINMAL)
    vereine = pl.DataFrame({
        "Verein_ID": [1, 2, 3],
        "Verein": ["Bayern München", "Bayer Leverkusen", "West Ham United"],
        "Vereinsort": ["München", "Leverkusen", "London"],
        "Stadion": ["Allianz Arena", "BayArena", "London Stadium"],
        "Gründungsjahr": [1900, 1904, 1895]
    })
    vereine
    return (vereine,)


@app.cell
def _(pl):
    # Tabelle 2: Spieler (mit Verweis auf Verein)
    spieler_gut = pl.DataFrame({
        "Spieler_ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Spieler": ["Müller", "Neuer", "Kimmich", "Sane", "Musiala",
                    "Wirtz", "Tah", "Frimpong",
                    "Füllkrug", "Nmecha"],
        "Position": ["Sturm", "Tor", "Mittelfeld", "Sturm", "Mittelfeld",
                     "Mittelfeld", "Abwehr", "Abwehr",
                     "Sturm", "Sturm"],
        "Verein_ID": [1, 1, 1, 1, 1, 2, 2, 2, 3, 3]  # Verweis auf vereine-Tabelle
    })
    spieler_gut
    return (spieler_gut,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beachten Sie:**
        - Die Vereinsinformationen stehen nur **einmal** in der `vereine`-Tabelle
        - Die `spieler_gut`-Tabelle hat nur eine `Verein_ID`, die auf die Vereine-Tabelle **verweist**
        - Diese `Verein_ID` ist ein **Fremdschlüssel**

        ---

        ### Aufgabe 5.5: Redundanz prüfen (verbessertes Design)

        Wie viel Redundanz haben wir jetzt noch?
        """
    )
    return


@app.cell
def _(mo, vereine):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*) AS Vereine_Gesamt,
            COUNT(DISTINCT Verein) AS Verschiedene_Vereine
        FROM vereine
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Perfekt!** Keine Redundanz mehr -- jeder Verein existiert genau einmal.

        Vergleichen wir die beiden Designs quantitativ:
        """
    )
    return


@app.cell
def _(pl, px):
    _vergleich = pl.DataFrame({
        "Design": ["Mega-Tabelle", "Mega-Tabelle", "Normalisiert", "Normalisiert"],
        "Kategorie": ["Gespeicherte Zeilen", "Eindeutige Fakten",
                       "Gespeicherte Zeilen", "Eindeutige Fakten"],
        "Anzahl": [10, 3, 13, 13]  # Mega: 10 Zeilen, 3 Vereine; Normal: 3+10=13, alle eindeutig
    })
    px.bar(
        _vergleich,
        x="Design",
        y="Anzahl",
        color="Kategorie",
        barmode="group",
        title="Mega-Tabelle vs. normalisiertes Design",
        labels={"Anzahl": "Anzahl", "Design": ""},
        color_discrete_map={
            "Gespeicherte Zeilen": "#003560",
            "Eindeutige Fakten": "#E87722"
        },
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        In der Mega-Tabelle werden 10 Zeilen gespeichert, aber nur 3 Vereins-Fakten sind
        tatsächlich verschieden. Im normalisierten Design entspricht jede Zeile einem
        eindeutigen Fakt -- keine verschwendete Redundanz.

        ---

        ### Aufgabe 5.6: Änderung testen (verbessertes Design)

        Jetzt ändern wir das Bayern-Stadion -- diesmal richtig:
        """
    )
    return


@app.cell
def _(pl, vereine):
    # Stadion ändern -- nur EINE Zeile!
    vereine_update = vereine.with_columns(
        pl.when(pl.col("Verein") == "Bayern München")
        .then(pl.lit("FC Bayern Arena"))
        .otherwise(pl.col("Stadion"))
        .alias("Stadion")
    )

    vereine_update
    return (vereine_update,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Eine Zeile, eine Änderung, keine Inkonsistenz möglich!**

        ---

        ### Aufgabe 5.7: Löschung testen (verbessertes Design)

        Was passiert, wenn wir jetzt alle Leverkusen-Spieler löschen?
        """
    )
    return


@app.cell
def _(pl, spieler_gut):
    # Leverkusen-Spieler löschen (Verein_ID = 2)
    spieler_nach_delete_gut = spieler_gut.filter(pl.col("Verein_ID") != 2)
    spieler_nach_delete_gut
    return (spieler_nach_delete_gut,)


@app.cell
def _(vereine):
    # Aber die Vereine-Tabelle ist unverändert!
    vereine
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Kein Informationsverlust!** Die Vereinsdaten bleiben erhalten,
        auch wenn wir keine Spieler mehr haben.

        ---

        ## Phase 6: Daten kombinieren (Vorschau auf JOINs)

        Natürlich wollen wir manchmal alle Informationen zusammen sehen.
        Dafür gibt es den **JOIN** -- aber das ist Thema von Session 9.

        Hier ein kleiner Vorgeschmack:
        """
    )
    return


@app.cell
def _(mo, spieler_gut, vereine):
    _df = mo.sql(
        f"""
        SELECT
            s.Spieler,
            s.Position,
            v.Verein,
            v.Stadion
        FROM spieler_gut s
        JOIN vereine v ON s.Verein_ID = v.Verein_ID
        ORDER BY v.Verein, s.Spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Der JOIN kombiniert die beiden Tabellen wieder -- aber die Daten sind
        **getrennt gespeichert** und damit anomaliefrei!

        ---

        ## Freie Exploration

        Experimentieren Sie selbst:

        - Fügen Sie einen neuen Verein hinzu (ohne Spieler)
        - Ändern Sie einen Vereinsort
        - Löschen Sie einen Spieler

        Beobachten Sie, wie das verbesserte Design diese Operationen vereinfacht.
        """
    )
    return


@app.cell
def _(mo, spieler_gut, vereine):
    # Ihre eigene Abfrage hier:
    _df = mo.sql(
        f"""
        -- Beispiel: Neuen Verein hinzufügen geht jetzt einfach
        -- (In echtem SQL wäre das ein INSERT)

        -- Hier zeigen wir, welche Vereine keine Spieler (mehr) haben könnten:
        SELECT v.Verein, COUNT(s.Spieler_ID) AS Anzahl_Spieler
        FROM vereine v
        LEFT JOIN spieler_gut s ON v.Verein_ID = s.Verein_ID
        GROUP BY v.Verein
        ORDER BY Anzahl_Spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Problem | Ursache | Lösung |
        |---------|---------|---------|
        | **Redundanz** | Alles in einer Tabelle | Daten aufteilen |
        | **Änderungsanomalie** | Gleiche Daten mehrfach | Primärschlüssel |
        | **Einfügeanomalie** | Abhängige Daten | Separate Tabellen |
        | **Löschanomalie** | Vermischte Konzepte | Fremdschlüssel |

        **Kernkonzepte:**
        - **Entität:** Ein "Ding" der realen Welt (Spieler, Verein)
        - **Primärschlüssel (PK):** Eindeutige ID für jede Zeile
        - **Fremdschlüssel (FK):** Verweis auf einen PK in anderer Tabelle

        **Nächste Session:** Entity-Relationship-Modellierung (ER-Diagramme)
        """
    )
    return


if __name__ == "__main__":
    app.run()
