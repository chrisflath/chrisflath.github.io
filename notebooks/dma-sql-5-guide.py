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
    app_title="DMA Session 5: Datenmodellierung — Guide",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 5: Datenmodellierung — Guide

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · **▸ II: Datenmodellierung (S5–7)** · III: Fortgeschrittenes SQL (S8–9) · IV: Datenanalyse (S10–13)

        ### Lernziele

        Nach dieser Session können Sie:

        - **Redundanz-Probleme** in Datenbanken erkennen
        - Daten auf **mehrere Tabellen** aufteilen
        - **ER-Diagramme** modellieren (Entitäten, Attribute, Beziehungen)
        - **Kardinalitäten** (1:1, 1:N, M:N) bestimmen

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _():
    import polars as pl

    # Die "schlechte" Mega-Tabelle mit Redundanzen
    spieler_schlecht = pl.DataFrame({
        "Spieler": ["Müller", "Neuer", "Kimmich", "Sané", "Musiala",
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

    # Normalisierte Tabellen
    vereine = pl.DataFrame({
        "Verein_ID": [1, 2, 3],
        "Verein": ["Bayern München", "Bayer Leverkusen", "West Ham United"],
        "Vereinsort": ["München", "Leverkusen", "London"],
        "Stadion": ["Allianz Arena", "BayArena", "London Stadium"],
        "Gründungsjahr": [1900, 1904, 1895]
    })

    spieler_gut = pl.DataFrame({
        "Spieler_ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Spieler": ["Müller", "Neuer", "Kimmich", "Sané", "Musiala",
                    "Wirtz", "Tah", "Frimpong", "Füllkrug", "Nmecha"],
        "Position": ["Sturm", "Tor", "Mittelfeld", "Sturm", "Mittelfeld",
                     "Mittelfeld", "Abwehr", "Abwehr", "Sturm", "Sturm"],
        "Verein_ID": [1, 1, 1, 1, 1, 2, 2, 2, 3, 3]
    })
    return pl, spieler_gut, spieler_schlecht, vereine


# ============================================================
# Phase 1: Redundanz erkennen
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 1: Redundanz erkennen

        ### Die "Mega-Tabelle": Ein problematisches Design

        Stellen Sie sich vor, wir verwalten Spieler und ihre Vereine in **einer** Tabelle.
        Das scheint zunächst praktisch -- alles an einem Ort!
        """
    )
    return


@app.cell(hide_code=True)
def _(spieler_schlecht):
    spieler_schlecht
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ### Geführtes Beispiel 5.1: Wie oft wird jede Vereinsinformation gespeichert?

        Zählen Sie, wie oft jeder Verein in der Tabelle vorkommt:
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, spieler_schlecht):
    _df = mo.sql(
        f"""
        SELECT
            Verein,
            COUNT(*) AS Anzahl_Einträge
        FROM spieler_schlecht
        GROUP BY Verein
        ORDER BY Anzahl_Einträge DESC
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


@app.cell(hide_code=True)
def _():
    import plotly.express as px
    return (px,)


@app.cell(hide_code=True)
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
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_redundanz = mo.ui.radio(
        options={
            "1": "1 Zeile",
            "5": "5 Zeilen",
            "10": "10 Zeilen",
        },
        label="**Vorhersage:** Bayern hat 5 Spieler. In wie vielen Zeilen müsste das Stadion geändert werden?"
    )
    pred_redundanz
    return (pred_redundanz,)


@app.cell(hide_code=True)
def _(mo, pred_redundanz):
    if pred_redundanz.value == "5":
        mo.output.replace(
            mo.md(
                "Richtig! Da jede Spielerzeile die Vereinsinformation wiederholt, "
                "müsste das Stadion in **allen 5 Zeilen** geändert werden. "
                "Vergisst man eine Zeile, entsteht eine Inkonsistenz -- "
                "das ist die **Änderungsanomalie**."
            )
        )
    elif pred_redundanz.value == "1":
        mo.output.replace(
            mo.md(
                "Nicht ganz. In der Mega-Tabelle wird die Vereinsinformation "
                "**in jeder Spielerzeile** wiederholt. Bayern hat 5 Spieler, "
                "also steht das Stadion in **5 Zeilen**. "
                "Eine Zeile wäre nur im normalisierten Design nötig."
            )
        )
    elif pred_redundanz.value == "10":
        mo.output.replace(
            mo.md(
                "Nicht ganz. 10 Zeilen ist die Gesamtanzahl aller Spieler in der Tabelle. "
                "Aber nur **5 Zeilen** gehören zu Bayern München -- "
                "in diesen 5 Zeilen müsste das Stadion geändert werden."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 2.x**

        ---
        """
    )
    return


# ============================================================
# Phase 3: Anomalien
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 3: Anomalien erleben

        ### Änderungsanomalie provozieren

        **Szenario:** Bayern München baut ein neues Stadion namens "FC Bayern Arena".

        Führen wir ein UPDATE durch -- aber "vergessen" wir absichtlich eine Zeile:
        """
    )
    return


@app.cell(hide_code=True)
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

        Prüfen wir die Inkonsistenz mit einer Abfrage:
        """
    )
    return


@app.cell(hide_code=True)
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

        ### Einfügeanomalie erleben

        **Szenario:** Was, wenn wir einen neuen Verein aufnehmen wollen,
        aber noch keinen Spieler für diesen Verein haben?
        """
    )
    return


@app.cell(hide_code=True)
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
        **Problem erkannt?** Wir mussten `NULL`-Werte für `Spieler` und `Position` eintragen.
        Das ist die **Einfügeanomalie**: Neue Informationen können nicht hinzugefügt werden,
        ohne gleichzeitig **andere, zusammenhanglose** Daten angeben zu müssen.

        ---

        ### Löschanomalie erleben

        **Szenario:** Wirtz, Tah und Frimpong wechseln alle ins Ausland.
        Wir löschen sie aus unserer Tabelle:
        """
    )
    return


@app.cell(hide_code=True)
def _(pl, spieler_schlecht):
    # Alle Leverkusen-Spieler löschen
    spieler_nach_delete = spieler_schlecht.filter(
        pl.col("Verein") != "Bayer Leverkusen"
    )

    spieler_nach_delete
    return (spieler_nach_delete,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Alle Informationen über Bayer Leverkusen sind verloren!**
        Vereinssitz, Stadion, Gründungsjahr -- alles weg.

        Prüfen wir, welche Vereine wir noch kennen:
        """
    )
    return


@app.cell(hide_code=True)
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

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_anomalie = mo.ui.radio(
        options={
            "correct": "Löschanomalie -- Vereinsinformationen gingen verloren",
            "aenderung": "Änderungsanomalie -- ein Verein ist nicht kohärent aktualisiert",
            "einfuege": "Einfügeanomalie -- wir konnten nicht alle Infos speichern",
            "normal": "Normalisierungsanomalie -- die Tabelle ist nicht in 3NF",
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
        mo.output.replace(mo.md("Nicht ganz. Beim **Löschen** von Daten gehen *andere* Informationen verloren -- das ist die Löschanomalie. Tipp: Der Name der Anomalie beschreibt die Aktion, die das Problem verursacht."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_einfuege = mo.ui.radio(
        options={
            "null": "Wir müssen NULL-Werte für Spieler eintragen (Einfügeanomalie)",
            "normal": "Der Verein wird ganz normal eingefügt",
            "fehler": "Die Datenbank gibt einen Fehler aus",
        },
        label="**Vorhersage:** Neuen Verein ohne Spieler einfügen -- was passiert in der Mega-Tabelle?"
    )
    pred_einfuege
    return (pred_einfuege,)


@app.cell(hide_code=True)
def _(mo, pred_einfuege):
    if pred_einfuege.value == "null":
        mo.output.replace(
            mo.md(
                "Richtig! In der Mega-Tabelle kann ein Verein nur als Teil einer "
                "**Spielerzeile** existieren. Ohne Spieler müssen wir `NULL`-Werte "
                "für Spielername und Position eintragen -- das ist die **Einfügeanomalie**. "
                "Im normalisierten Design existiert die Vereinstabelle unabhängig von Spielern."
            )
        )
    elif pred_einfuege.value == "normal":
        mo.output.replace(
            mo.md(
                "Nicht ganz. In der Mega-Tabelle sind Spieler- und Vereinsdaten "
                "in derselben Zeile verknüpft. Ohne Spieler müssen Sie `NULL`-Werte "
                "für die Spieler-Spalten eintragen -- das ist die **Einfügeanomalie**."
            )
        )
    elif pred_einfuege.value == "fehler":
        mo.output.replace(
            mo.md(
                "Nicht ganz. Die Datenbank gibt keinen Fehler aus, aber das Ergebnis ist "
                "unbefriedigend: Sie müssen `NULL`-Werte für Spieler und Position eintragen, "
                "um den Verein speichern zu können -- das ist die **Einfügeanomalie**."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 4.x**

        ---
        """
    )
    return


# ============================================================
# Phase 5: ER-Modellierung
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 5: Die Lösung -- Daten aufteilen & ER-Modellierung

        ### Normalisierte Tabellen

        Die Lösung ist einfach: **Jedes "Ding" bekommt seine eigene Tabelle!**

        - Spieler sind ein "Ding" (Entität)
        - Vereine sind ein anderes "Ding" (Entität)
        """
    )
    return


@app.cell(hide_code=True)
def _(vereine):
    vereine
    return


@app.cell(hide_code=True)
def _(spieler_gut):
    spieler_gut
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beachten Sie:**
        - Die Vereinsinformationen stehen nur **einmal** in der `vereine`-Tabelle
        - Die `spieler_gut`-Tabelle hat nur eine `Verein_ID`, die auf die Vereine-Tabelle **verweist**
        - Diese `Verein_ID` ist ein **Fremdschlüssel**

        ---

        ### ER-Modellierung: Kernkonzepte

        Wie wissen wir, *welche* Tabellen wir brauchen?
        Die **Entity-Relationship-Modellierung (ER)** gibt uns eine systematische Methode!

        | Element | Symbol | Beschreibung |
        |---------|--------|--------------|
        | **Entität** | Rechteck | Ein "Ding" der realen Welt (Spieler, Verein) |
        | **Attribut** | Ellipse | Eigenschaft einer Entität (Name, Alter) |
        | **Schlüssel** | Unterstrichen | Eindeutige Identifikation |
        | **Beziehung** | Raute | Verbindung zwischen Entitäten |

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ER-Diagramme visualisieren (Mermaid-Notation)

        In den folgenden Beispielen verwenden wir **Mermaid-Diagramme**, die ER-Modelle
        kompakt darstellen. Die Symbole an den Verbindungslinien zeigen die Kardinalitäten:

        | Symbol | Bedeutung |
        |--------|-----------|
        | `\|\|` | Genau eins |
        | `o\|` | Null oder eins |
        | `\|{` | Eins oder mehr |
        | `o{` | Null oder mehr |

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Kardinalitäten

        Beziehungen zwischen Entitäten haben unterschiedliche **Kardinalitäten** --
        sie beschreiben, wie viele Instanzen auf jeder Seite beteiligt sein können:

        | Kardinalität | Beispiel | Erklärung |
        |--------------|----------|-----------|
        | **1:1** | Person -- Personalausweis | Jede Person hat genau einen Ausweis |
        | **1:N** | Verein -- Spieler | Ein Verein hat viele Spieler |
        | **M:N** | Student -- Kurs | Studierende besuchen mehrere Kurse |

        **Faustregel:** Die meisten Beziehungen in der Praxis sind **1:N**!

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quiz: Kardinalitäten bestimmen
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    quiz1 = mo.ui.radio(
        options={
            "1:1": "1:1 (Eins zu Eins)",
            "1:N": "1:N (Eins zu Viele)",
            "M:N": "M:N (Viele zu Viele)"
        },
        label="**Frage 1:** Verein <-> Spieler (ein Spieler spielt für einen Verein)"
    )
    quiz1
    return (quiz1,)


@app.cell(hide_code=True)
def _(mo, quiz1):
    if quiz1.value == "1:N":
        mo.output.replace(mo.md("Richtig! Ein Verein hat viele Spieler, aber jeder Spieler gehört zu einem Verein."))
    elif quiz1.value:
        mo.output.replace(mo.md("Nicht ganz. Denken Sie daran: Ein Verein kann *viele* Spieler haben."))
    return


@app.cell(hide_code=True)
def _(mo):
    quiz2 = mo.ui.radio(
        options={
            "1:1": "1:1 (Eins zu Eins)",
            "1:N": "1:N (Eins zu Viele)",
            "M:N": "M:N (Viele zu Viele)"
        },
        label="**Frage 2:** Student <-> Kurs (Studierende können mehrere Kurse besuchen, Kurse haben mehrere Studierende)"
    )
    quiz2
    return (quiz2,)


@app.cell(hide_code=True)
def _(mo, quiz2):
    if quiz2.value == "M:N":
        mo.output.replace(mo.md("Richtig! Beide Seiten können mit vielen auf der anderen verbunden sein."))
    elif quiz2.value:
        mo.output.replace(mo.md("Nicht ganz. Auf *beiden* Seiten sind mehrere möglich."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 3
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_kardinalitaet = mo.ui.radio(
        options={
            "0": "0",
            "2": "2",
            "3": "3",
            "5": "5",
        },
        label="**Vorhersage:** Von diesen 5 Beziehungen (Abt-Mitarbeiter, Student-Kurs, Person-Ausweis, Autor-Buch, Verein-Spieler) -- wie viele sind 1:N?"
    )
    pred_kardinalitaet
    return (pred_kardinalitaet,)


@app.cell(hide_code=True)
def _(mo, pred_kardinalitaet):
    if pred_kardinalitaet.value == "2":
        mo.output.replace(
            mo.md(
                "Richtig! Genau **2** der 5 Beziehungen sind 1:N:\n\n"
                "- **Abteilung -- Mitarbeiter:** 1:N (eine Abteilung hat viele Mitarbeiter)\n"
                "- **Verein -- Spieler:** 1:N (ein Verein hat viele Spieler)\n\n"
                "Die anderen:\n"
                "- Person -- Ausweis: **1:1**\n"
                "- Student -- Kurs: **M:N**\n"
                "- Autor -- Buch: **M:N** (Co-Autoren!)"
            )
        )
    elif pred_kardinalitaet.value == "0":
        mo.output.replace(
            mo.md(
                "Nicht ganz. Es gibt durchaus 1:N-Beziehungen in der Liste! "
                "Denken Sie an Abteilung -- Mitarbeiter: Eine Abteilung hat *viele* Mitarbeiter, "
                "aber jeder Mitarbeiter gehört zu *einer* Abteilung."
            )
        )
    elif pred_kardinalitaet.value == "3":
        mo.output.replace(
            mo.md(
                "Nicht ganz. Prüfen Sie nochmal genau: Student -- Kurs und Autor -- Buch "
                "sind **M:N** (auf *beiden* Seiten mehrere möglich). "
                "Person -- Ausweis ist **1:1**. Nur 2 der 5 sind tatsächlich 1:N."
            )
        )
    elif pred_kardinalitaet.value == "5":
        mo.output.replace(
            mo.md(
                "Nicht ganz. Nicht alle Beziehungen sind 1:N! "
                "Person -- Ausweis ist **1:1** (jede Person hat genau einen). "
                "Student -- Kurs und Autor -- Buch sind **M:N** (beide Seiten können mehrere haben). "
                "Nur **2** der 5 sind 1:N."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ### (Min,Max)-Notation

        Für präzisere Kardinalitätsangaben gibt es die (Min,Max)-Notation:

        | Notation | Bedeutung |
        |----------|-----------|
        | **(0,1)** | Optional, höchstens einer |
        | **(1,1)** | Genau einer (Pflicht) |
        | **(0,N)** | Optional, beliebig viele |
        | **(1,N)** | Mindestens einer, beliebig viele |
        | **(15,30)** | Zwischen 15 und 30 |

        **Beispiel Bundesliga:** Ein Verein hat **(15,30)** Spieler im Kader --
        mindestens 15 und höchstens 30 gemäß den Regularien.

        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 6.x**

        ---
        """
    )
    return


# ============================================================
# Phase 7: Visualisierung
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 7: Visualisierung -- Redundanz sichtbar machen
        """
    )
    return


@app.cell(hide_code=True)
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

        ### Attribute pro Entität (Bibliotheks-Modell)

        Wie komplex sind die einzelnen Entitäten in einem typischen Bibliotheks-Datenmodell?
        """
    )
    return


@app.cell(hide_code=True)
def _(px):
    _entitaeten = ["Verlag", "Buch", "Autor", "Exemplar", "Student", "Ausleihe"]
    _attribute = [3, 4, 2, 3, 2, 5]  # inkl. PK und FK
    _typen = ["Entität", "Entität", "Entität",
              "Abhängige Entität", "Entität", "Beziehungstabelle"]

    _fig = px.bar(
        x=_entitaeten,
        y=_attribute,
        color=_typen,
        title="Attribute pro Entität (Bibliotheks-Modell)",
        labels={"x": "Entität", "y": "Anzahl Attribute", "color": "Typ"},
        color_discrete_map={
            "Entität": "#003560",
            "Abhängige Entität": "#E87722",
            "Beziehungstabelle": "#5B9BD5",
        },
    )
    _fig.update_layout(xaxis_title="", yaxis_title="Anzahl Attribute")
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Die **Ausleihe** als Beziehungstabelle hat die meisten Attribute
        (inkl. Fremdschlüssel und Beziehungsattribute). **Exemplar** braucht den Schlüssel
        des Buches (ISBN) als Teil seines eigenen Schlüssels.

        ---

        ### Viz-Choice: Den richtigen Charttyp wählen
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    viz_choice_5 = mo.ui.radio(
        options={
            "grouped_bar": "Gruppiertes Balkendiagramm",
            "pie": "Kreisdiagramm",
            "line": "Liniendiagramm",
            "scatter": "Streudiagramm",
        },
        label="Redundanz zeigen: 10 Zeilen gespeichert vs. nur 3 eindeutige Fakten?"
    )
    viz_choice_5
    return (viz_choice_5,)


@app.cell(hide_code=True)
def _(mo, viz_choice_5):
    if viz_choice_5.value == "grouped_bar":
        mo.output.replace(
            mo.md(
                "Richtig! Ein **gruppiertes Balkendiagramm** eignet sich ideal, um "
                "zwei Kennzahlen (Gespeicherte Zeilen vs. Eindeutige Fakten) für die gleichen "
                "Kategorien (Mega-Tabelle, Normalisiert) nebeneinander zu vergleichen. "
                "Die Diskrepanz bei der Mega-Tabelle springt sofort ins Auge."
            )
        )
    elif viz_choice_5.value == "pie":
        mo.output.replace(
            mo.md(
                "Nicht ganz. Ein Kreisdiagramm zeigt Anteile am Ganzen, aber hier wollen wir "
                "**zwei verschiedene Kennzahlen** für zwei Designs vergleichen. "
                "Ein **gruppiertes Balkendiagramm** macht die Diskrepanz deutlicher sichtbar."
            )
        )
    elif viz_choice_5.value == "line":
        mo.output.replace(
            mo.md(
                "Nicht ganz. Ein Liniendiagramm suggeriert eine zeitliche Entwicklung oder "
                "Reihenfolge. Hier vergleichen wir **zwei Designs** nebeneinander -- "
                "ein **gruppiertes Balkendiagramm** ist dafür besser geeignet."
            )
        )
    elif viz_choice_5.value == "scatter":
        mo.output.replace(
            mo.md(
                "Nicht ganz. Ein Streudiagramm zeigt den Zusammenhang zweier numerischer "
                "Variablen. Hier haben wir Kategorien (Designs) und wollen Kennzahlen vergleichen -- "
                "ein **gruppiertes Balkendiagramm** ist die bessere Wahl."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Selbsttest
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    selbsttest_5 = mo.ui.radio(
        options={
            "redundanz": "Redundanz (mehrfach gespeicherte Daten)",
            "geschwindigkeit": "Langsamere Abfragen",
            "speicher": "Höherer Speicherverbrauch",
        },
        label="Welches Problem löst die Aufteilung auf mehrere Tabellen primär?"
    )
    selbsttest_5
    return (selbsttest_5,)


@app.cell(hide_code=True)
def _(mo, selbsttest_5):
    if selbsttest_5.value == "redundanz":
        mo.output.replace(
            mo.md(
                "Richtig! Die Aufteilung auf mehrere Tabellen löst primär das "
                "**Redundanz-Problem**: Jede Information wird nur **einmal** gespeichert. "
                "Dadurch verschwinden auch die drei Anomalien (Änderungs-, Einfüge-, Löschanomalie). "
                "Speicherverbrauch und Geschwindigkeit sind zwar auch betroffen, aber "
                "die Vermeidung von Inkonsistenzen ist das Hauptziel."
            )
        )
    elif selbsttest_5.value == "geschwindigkeit":
        mo.output.replace(
            mo.md(
                "Nicht ganz. Normalisierung kann Abfragen sogar *langsamer* machen (wegen JOINs). "
                "Das Hauptproblem, das gelöst wird, ist **Redundanz**: mehrfach gespeicherte Daten "
                "führen zu Inkonsistenzen und Anomalien."
            )
        )
    elif selbsttest_5.value == "speicher":
        mo.output.replace(
            mo.md(
                "Nicht ganz. Normalisierung spart zwar etwas Speicher, aber das ist ein "
                "Nebeneffekt. Das Hauptproblem ist **Redundanz**: Wenn dieselbe Information "
                "an mehreren Stellen steht, entstehen Inkonsistenzen bei Änderungen."
            )
        )
    return


# ============================================================
# Probieren Sie selbst
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Probieren Sie selbst

        Experimentieren Sie mit den normalisierten Tabellen:
        """
    )
    return


@app.cell
def _(mo, spieler_gut, vereine):
    # Ihre eigene Abfrage hier:
    _df = mo.sql(
        f"""
        -- Beispiel: Spieler mit Vereinsnamen zusammenführen
        SELECT s.Spieler, s.Position, v.Verein, v.Stadion
        FROM spieler_gut s
        JOIN vereine v ON s.Verein_ID = v.Verein_ID
        ORDER BY v.Verein, s.Spieler
        """
    )
    return


# ============================================================
# Zusammenfassung
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        ### Teil 1: Redundanz & Anomalien

        | Problem | Ursache | Lösung |
        |---------|---------|--------|
        | **Redundanz** | Alles in einer Tabelle | Daten aufteilen |
        | **Änderungsanomalie** | Gleiche Daten mehrfach | Primärschlüssel |
        | **Einfügeanomalie** | Abhängige Daten | Separate Tabellen |
        | **Löschanomalie** | Vermischte Konzepte | Fremdschlüssel |

        ### Teil 2: ER-Modellierung

        | Schritt | Frage |
        |---------|-------|
        | 1. Entitäten | Was sind die "Dinge"? |
        | 2. Attribute | Welche Eigenschaften haben sie? |
        | 3. Schlüssel | Was macht sie eindeutig? |
        | 4. Beziehungen | Wie hängen sie zusammen? |
        | 5. Kardinalitäten | Wie viele auf jeder Seite? |

        **Kernkonzepte:**

        - **Entität:** Ein "Ding" der realen Welt (Spieler, Verein)
        - **Primärschlüssel (PK):** Eindeutige ID für jede Zeile
        - **Fremdschlüssel (FK):** Verweis auf einen PK in anderer Tabelle
        - **Kardinalitäten:** 1:1, 1:N, M:N
        - **Werkzeuge:** Papier, Whiteboard, draw.io, Lucidchart

        ### Ausblick Session 6: ER → SQL (CREATE TABLE)

        Nächste Session überführen wir ER-Diagramme in SQL-Tabellen mit
        `CREATE TABLE`, `PRIMARY KEY` und `FOREIGN KEY`.
        """
    )
    return


if __name__ == "__main__":
    app.run()
