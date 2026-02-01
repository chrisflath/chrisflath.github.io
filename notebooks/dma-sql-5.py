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
    app_title="DMA Session 5: Datenmodellierung",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 5: Datenmodellierung -- Von Anomalien zum ER-Modell

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · **▸ II: Datenmodellierung (S5–7)** · III: Fortgeschrittenes SQL (S8–9) · IV: Datenanalyse (S10–13)

        In dieser Session lernen Sie:

        - Probleme der **Redundanz** in Datenbanken
        - Die drei **Anomalien**: Änderungs-, Einfüge-, Löschanomalie
        - Warum wir Daten auf **mehrere Tabellen** aufteilen
        - **Entitäten**, **Attribute** und **Beziehungen** modellieren
        - **Kardinalitäten** (1:1, 1:N, M:N) bestimmen
        - Die **Crow's Foot Notation** für ER-Diagramme

        ---
        """
    )
    return


# ============================================================
# Teil 1: Redundanz und Anomalien
# ============================================================


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
        ### Aufgabe 5.2a: Redundanz pro Verein (scaffolded)

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
    mo.accordion({"Musterlösung": mo.md("""
```sql
SELECT
    Verein,
    COUNT(*) AS Gesamt_Zeilen,
    COUNT(*) - 1 AS Redundante_Zeilen
FROM spieler_schlecht
GROUP BY Verein
ORDER BY Redundante_Zeilen DESC
```
""")})
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

        ### Aufgabe 5.4: Einfügeanomalie erleben

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

        ### Aufgabe 5.5: Löschanomalie erleben

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
            "correct": "Löschanomalie -- Vereinsinformationen gingen verloren",
            "aenderung": "Änderungsanomalie -- ein Verein ist nicht kohärent aktualisiert",
            "einfuege": "Einfügeanomalie -- wir konnten nicht alle Infos auf einmal speichern",
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


# ============================================================
# Teil 2: Die Lösung -- Daten aufteilen
# ============================================================


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

        ### Aufgabe 5.6: Redundanz prüfen (verbessertes Design)

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

        ### Aufgabe 5.7: Änderung testen (verbessertes Design)

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

        ### Aufgabe 5.8: Löschung testen (verbessertes Design)

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
        Dafür gibt es den **JOIN** -- aber das ist Thema einer späteren Session.

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
        """
    )
    return


# ============================================================
# Teil 3: ER-Modellierung
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Von der Lösung zur Methode: ER-Modellierung

        Wir haben gesehen: Die Lösung für Redundanz ist, Daten auf **mehrere Tabellen** aufzuteilen.

        **Die Frage:** Wie wissen wir, *welche* Tabellen wir brauchen?

        Die **Entity-Relationship-Modellierung (ER)** gibt uns eine systematische Methode!

        ---

        ## Kernkonzepte

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
    mo.md(r"""
## Crow's Foot Notation (Kardinalitäten)

In ER-Diagrammen verwenden wir oft die **Crow's Foot Notation**:

| Symbol | Bedeutung |
|--------|-----------|
| `\|\|` (Strich) | Genau eins |
| `o\|` (Kreis + Strich) | Null oder eins |
| `\|{` (Strich + Gabel) | Eins oder mehr |
| `o{` (Kreis + Gabel) | Null oder mehr |

**Beispiel:** `VEREIN \|\|--\|{ SPIELER` bedeutet: Ein Verein hat *eins oder mehr* Spieler.

---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Quiz: Kardinalitäten bestimmen

        > **Vorhersage:** Von den 7 Szenarien unten -- wie viele sind 1:1, wie viele 1:N und wie viele M:N? Schätzen Sie die Verteilung, bevor Sie die Quizfragen beantworten.

        Bestimmen Sie für jedes Beispiel die richtige Kardinalität!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    # Quiz 1
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
    # Quiz 2
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
    # Quiz 3
    quiz3 = mo.ui.radio(
        options={
            "1:1": "1:1 (Eins zu Eins)",
            "1:N": "1:N (Eins zu Viele)",
            "M:N": "M:N (Viele zu Viele)"
        },
        label="**Frage 3:** Person <-> Personalausweis (jede Person hat genau einen Ausweis)"
    )
    quiz3
    return (quiz3,)


@app.cell(hide_code=True)
def _(mo, quiz3):
    if quiz3.value == "1:1":
        mo.output.replace(mo.md("Richtig! Jede Person hat genau einen Ausweis, und jeder Ausweis gehört zu genau einer Person."))
    elif quiz3.value:
        mo.output.replace(mo.md("Nicht ganz. Eine Person hat *genau einen* Ausweis (nicht mehrere)."))
    return


@app.cell(hide_code=True)
def _(mo):
    # Quiz 4
    quiz4 = mo.ui.radio(
        options={
            "1:1": "1:1 (Eins zu Eins)",
            "1:N": "1:N (Eins zu Viele)",
            "M:N": "M:N (Viele zu Viele)"
        },
        label="**Frage 4:** Autor <-> Buch (ein Buch kann mehrere Autoren haben, Autoren schreiben mehrere Bücher)"
    )
    quiz4
    return (quiz4,)


@app.cell(hide_code=True)
def _(mo, quiz4):
    if quiz4.value == "M:N":
        mo.output.replace(mo.md("Richtig! Co-Autoren und Vielschreiber -- M:N!"))
    elif quiz4.value:
        mo.output.replace(mo.md("Nicht ganz. Denken Sie an Co-Autoren: Ein Buch kann *mehrere* Autoren haben."))
    return


@app.cell(hide_code=True)
def _(mo):
    # Quiz 5
    quiz5 = mo.ui.radio(
        options={
            "1:1": "1:1 (Eins zu Eins)",
            "1:N": "1:N (Eins zu Viele)",
            "M:N": "M:N (Viele zu Viele)"
        },
        label="**Frage 5:** Abteilung <-> Mitarbeiter (jeder Mitarbeiter gehört zu einer Abteilung)"
    )
    quiz5
    return (quiz5,)


@app.cell(hide_code=True)
def _(mo, quiz5):
    if quiz5.value == "1:N":
        mo.output.replace(mo.md("Richtig! Eine Abteilung hat viele Mitarbeiter, aber jeder Mitarbeiter ist in einer Abteilung."))
    elif quiz5.value:
        mo.output.replace(mo.md("Nicht ganz. Eine Abteilung hat *viele* Mitarbeiter."))
    return


@app.cell(hide_code=True)
def _(mo):
    # Quiz 6
    quiz6 = mo.ui.radio(
        options={
            "attribut": "Attribut (Eigenschaft einer Entität)",
            "entitaet": "Entität (eigenständiges Objekt)",
            "beziehung": "Beziehung (Verbindung zwischen Entitäten)"
        },
        label="**Frage 6:** Ist 'Raumnummer' in einem Universitätssystem ein Attribut oder eine Entität?"
    )
    quiz6
    return (quiz6,)


@app.cell(hide_code=True)
def _(mo, quiz6):
    if quiz6.value == "attribut":
        mo.output.replace(mo.md("Richtig! Raumnummer ist typischerweise ein Attribut von z.B. einer Veranstaltung. *Aber:* Wenn Räume eigene Eigenschaften haben (Kapazität, Gebäude, Beamer), könnte 'Raum' auch eine eigene Entität sein!"))
    elif quiz6.value == "entitaet":
        mo.output.replace(mo.md("Möglich! Wenn Räume eigene Eigenschaften haben (Kapazität, Ausstattung), kann 'Raum' eine Entität sein. Die einfache 'Raumnummer' allein ist aber eher ein Attribut."))
    elif quiz6.value:
        mo.output.replace(mo.md("Nicht ganz. Eine Raumnummer ist eine Eigenschaft, keine Verbindung zwischen Objekten."))
    return


@app.cell(hide_code=True)
def _(mo):
    # Quiz 7
    quiz7 = mo.ui.radio(
        options={
            "weak": "Schwache Entität (existiert nicht ohne Buch)",
            "strong": "Starke Entität (existiert unabhängig)",
            "beziehung": "Beziehung (Verbindung zwischen Buch und Regal)",
            "attribut": "Attribut von Buch"
        },
        label="**Frage 7:** Ein Bibliotheks-Exemplar hat nur zusammen mit dem Buchtitel eine eindeutige ID (Buch-ISBN + Exemplar-Nr). Was ist es?"
    )
    quiz7
    return (quiz7,)


@app.cell(hide_code=True)
def _(mo, quiz7):
    if quiz7.value == "weak":
        mo.output.replace(mo.md("Richtig! Ein Exemplar kann ohne das zugehörige Buch nicht existieren und hat keinen eigenständigen Schlüssel. Das ist eine **schwache Entität** mit einer **identifizierenden Beziehung** zum Buch."))
    elif quiz7.value:
        mo.output.replace(mo.md("Nicht ganz. Das Exemplar braucht den Schlüssel des Buches, um eindeutig identifiziert zu werden. Es ist existenzabhängig vom Buch."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Häufige Kardinalitäten

        | Kardinalität | Beispiele | Häufigkeit |
        |--------------|-----------|------------|
        | **1:1** | Person-Ausweis, Land-Hauptstadt | Selten |
        | **1:N** | Abteilung-Mitarbeiter, Verein-Spieler, Kunde-Bestellung | **Sehr häufig** |
        | **M:N** | Student-Kurs, Autor-Buch, Schauspieler-Film | Häufig |

        **Faustregel:** Die meisten Beziehungen sind 1:N!

        ---
        """
    )
    return


# ============================================================
# Teil 4: ER-Diagramme in der Praxis
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Übung: Entitäten und Beziehungen identifizieren

        Lesen Sie die folgende Beschreibung und identifizieren Sie:
        1. Welche **Entitäten** gibt es?
        2. Welche **Beziehungen** bestehen?
        3. Welche **Kardinalitäten** haben diese?
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Szenario: Fußball-Liga

        *"In einer Fußball-Liga spielen mehrere Vereine. Jeder Verein hat einen Namen,
        einen Ort und ein Gründungsjahr. Spieler gehören zu einem Verein und haben
        einen Namen, eine Position und ein Geburtsdatum. Vereine spielen Spiele
        gegeneinander, wobei jedes Spiel an einem bestimmten Datum stattfindet
        und ein Ergebnis (Tore Heim, Tore Gast) hat."*

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Lösung anzeigen": mo.md(r"""
**Entitäten:**
- **Verein** (Name, Ort, Gründungsjahr)
- **Spieler** (Name, Position, Geburtsdatum)
- **Spiel** (Datum, Tore_Heim, Tore_Gast)

**Beziehungen:**
1. Spieler **spielt für** Verein -> **1:N** (ein Verein hat viele Spieler)
2. Verein **spielt** Spiel -> **2:N** (jedes Spiel hat 2 Vereine; Heim und Gast)

**Alternativ:** Spiel als Beziehung zwischen zwei Vereinen modellieren (mit Attributen für Datum und Ergebnis)
        """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
### ER-Diagramm: Fußball-Liga (Mermaid)

Das folgende Diagramm zeigt die Lösung in der **Crow's Foot Notation**:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
        erDiagram
            VEREIN ||--|{ SPIELER : hat
            VEREIN ||--|{ SPIEL : "spielt (Heim)"
            VEREIN ||--|{ SPIEL : "spielt (Gast)"

            VEREIN {
                int ID PK
                string Name
                string Ort
                int Gruendungsjahr
            }

            SPIELER {
                int ID PK
                string Name
                string Position
                date Geburtsdatum
                int Verein_ID FK
            }

            SPIEL {
                int ID PK
                date Datum
                int Tore_Heim
                int Tore_Gast
                int Heim_ID FK
                int Gast_ID FK
            }
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
---

## Beispiel: Online-Shop (M:N-Beziehung)

Ein Online-Shop mit Kunden, Bestellungen und Produkten:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
        erDiagram
            KUNDE ||--o{ BESTELLUNG : "gibt auf"
            BESTELLUNG ||--|{ BESTELLPOSITION : enthaelt
            PRODUKT ||--o{ BESTELLPOSITION : "ist in"
            KATEGORIE ||--o{ PRODUKT : beinhaltet

            KUNDE {
                int ID PK
                string Name
                string Email UK
            }

            BESTELLUNG {
                int ID PK
                date Datum
                int Kunde_ID FK
            }

            BESTELLPOSITION {
                int Bestellung_ID PK,FK
                int Produkt_ID PK,FK
                int Menge
            }

            PRODUKT {
                int ID PK
                string Name
                decimal Preis
                int Kategorie_ID FK
            }

            KATEGORIE {
                int ID PK
                string Name
            }
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
**Beobachtungen:**

- **1:N:** Kunde -> Bestellung, Kategorie -> Produkt
- **M:N:** Bestellung <-> Produkt (aufgelöst durch Bestellposition)
- Die **Bestellposition** ist eine Beziehungstabelle mit zusammengesetztem Primärschlüssel

*In Session 6 werden wir dieses Modell in SQL CREATE TABLE umsetzen!*

---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Übung: Bibliotheks-Szenario

        Identifizieren Sie die Entitäten, Beziehungen und Kardinalitäten:
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Szenario: Universitätsbibliothek

        *"Eine Bibliothek verwaltet Bücher und deren Exemplare. Jedes Buch hat eine ISBN,
        einen Titel und ein Erscheinungsjahr. Ein Buch kann mehrere Autoren haben, und
        Autoren können mehrere Bücher geschrieben haben. Jedes Buch gehört zu genau einem
        Verlag (Name, Ort). Von jedem Buch existieren ein oder mehrere physische Exemplare,
        die durch eine Exemplar-Nummer (innerhalb des Buches) unterschieden werden.
        Studierende können Exemplare ausleihen, wobei Ausleihdatum und Rückgabedatum
        gespeichert werden."*

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Lösung anzeigen": mo.md(r"""
**Entitäten:**
- **Buch** (ISBN, Titel, Erscheinungsjahr)
- **Autor** (AutorID, Name)
- **Verlag** (VerlagID, Name, Ort)
- **Exemplar** (ExemplarNr) -- *schwache Entität*, abhängig von Buch
- **Student** (MatrikelNr, Name)

**Beziehungen:**
1. Autor **schreibt** Buch -> **M:N** (Co-Autoren, Vielschreiber)
2. Verlag **veröffentlicht** Buch -> **1:N** (ein Verlag, viele Bücher)
3. Buch **hat** Exemplar -> **1:N** (identifizierende Beziehung, schwache Entität)
4. Student **leiht aus** Exemplar -> **M:N** mit Attributen (Ausleihdatum, Rückgabedatum)

**Besonderheiten:**
- Exemplar ist eine **schwache Entität**: ExemplarNr allein ist nicht eindeutig, erst ISBN + ExemplarNr
- Die Ausleihe ist eine M:N-Beziehung mit **Beziehungsattributen** (Datum)
        """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
### ER-Diagramm: Bibliothek (Mermaid)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
        erDiagram
            VERLAG ||--o{ BUCH : veroeffentlicht
            BUCH ||--|{ EXEMPLAR : hat
            AUTOR }|--|{ BUCH : schreibt
            STUDENT }|--o{ AUSLEIHE : leiht
            EXEMPLAR ||--o{ AUSLEIHE : "wird ausgeliehen"

            VERLAG {
                int ID PK
                string Name
                string Ort
            }

            BUCH {
                string ISBN PK
                string Titel
                int Erscheinungsjahr
                int Verlag_ID FK
            }

            AUTOR {
                int ID PK
                string Name
            }

            EXEMPLAR {
                string ISBN PK,FK
                int ExemplarNr PK
                string Standort
            }

            STUDENT {
                int MatrikelNr PK
                string Name
            }

            AUSLEIHE {
                int ID PK
                string ISBN FK
                int ExemplarNr FK
                int MatrikelNr FK
                date Ausleihdatum
                date Rueckgabedatum
            }
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
**Beobachtungen:**

- **Schwache Entität:** Exemplar hat einen zusammengesetzten Schlüssel (ISBN + ExemplarNr)
- **M:N mit Attributen:** Die Ausleihe speichert neben den Verweisen auch Datumsangaben
- **1:N:** Verlag -> Buch (jedes Buch hat genau einen Verlag)
- **M:N:** Autor <-> Buch (aufgelöst durch implizite Beziehungstabelle)

*Dieses Szenario kombiniert alle Beziehungstypen, die wir kennengelernt haben!*

---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
### Visualisierung: Attribute pro Entität

Wie komplex sind die einzelnen Entitäten in unserem Bibliotheks-Modell?
    """)
    return


@app.cell(hide_code=True)
def _(px):
    _entitaeten = ["Verlag", "Buch", "Autor", "Exemplar", "Student", "Ausleihe"]
    _attribute = [3, 4, 2, 3, 2, 5]  # inkl. PK und FK
    _typen = ["Starke Entität", "Starke Entität", "Starke Entität",
              "Schwache Entität", "Starke Entität", "Beziehungstabelle"]

    _fig = px.bar(
        x=_entitaeten,
        y=_attribute,
        color=_typen,
        title="Attribute pro Entität (Bibliotheks-Modell)",
        labels={"x": "Entität", "y": "Anzahl Attribute", "color": "Typ"},
        color_discrete_map={
            "Starke Entität": "#003560",
            "Schwache Entität": "#E87722",
            "Beziehungstabelle": "#5B9BD5",
        },
    )
    _fig.update_layout(xaxis_title="", yaxis_title="Anzahl Attribute")
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
**Beobachtung:** Die **Ausleihe** als Beziehungstabelle hat die meisten Attribute (inkl. Fremdschlüssel und Beziehungsattribute). Schwache Entitäten wie **Exemplar** brauchen den Schlüssel der übergeordneten Entität.

---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## (Min,Max)-Notation

        Genauere Kardinalitätsangabe:

        | Notation | Bedeutung |
        |----------|-----------|
        | **(0,1)** | Optional, höchstens einer |
        | **(1,1)** | Genau einer (Pflicht) |
        | **(0,N)** | Optional, beliebig viele |
        | **(1,N)** | Mindestens einer, beliebig viele |
        | **(15,30)** | Zwischen 15 und 30 |

        **Beispiel:** Ein Bundesliga-Verein hat **(15,30)** Spieler im Kader.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Selbstständig: Eigenes ER-Modell entwerfen

        **Szenario:** Eine Universitätsbibliothek möchte ihre Ausleihe digitalisieren.

        - Es gibt **Bücher** (ISBN, Titel, Erscheinungsjahr) und **Autoren** (Name, Nationalität)
        - **Studierende** (Matrikelnummer, Name, Studiengang) können Bücher **ausleihen** (Datum, Rückgabedatum)
        - Ein Buch kann von mehreren Autoren geschrieben sein
        - Ein Studierender kann mehrere Bücher gleichzeitig ausleihen

        **Aufgabe:** Zeichnen Sie ein ER-Diagramm auf Papier oder in [draw.io](https://draw.io):

        1. Welche **Entitäten** gibt es? (Tipp: 3 Stück)
        2. Welche **Attribute** hat jede Entität? Was ist der Primärschlüssel?
        3. Welche **Beziehungen** bestehen? (Tipp: 2 Stück)
        4. Was sind die **Kardinalitäten**? (1:1, 1:N, oder M:N?)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Musterlösung": mo.md("""
**Entitäten:**

1. **Buch** (Primärschlüssel: ISBN)
   - Attribute: ISBN, Titel, Erscheinungsjahr
2. **Autor** (Primärschlüssel: AutorID)
   - Attribute: AutorID, Name, Nationalität
3. **Studierender** (Primärschlüssel: Matrikelnummer)
   - Attribute: Matrikelnummer, Name, Studiengang

**Beziehungen:**

1. **Autor** *schreibt* **Buch** -> **M:N**
   - Ein Buch kann mehrere Autoren haben (Co-Autoren)
   - Ein Autor kann mehrere Bücher schreiben
   - -> Wird als Beziehungstabelle aufgelöst (z.B. `Autor_Buch`)
2. **Studierender** *leiht aus* **Buch** -> **M:N** (mit Beziehungsattributen)
   - Ein Studierender kann mehrere Bücher ausleihen
   - Ein Buch kann von verschiedenen Studierenden ausgeliehen werden
   - Beziehungsattribute: Datum, Rückgabedatum
   - -> Wird als Beziehungstabelle aufgelöst (z.B. `Ausleihe`)
""")})
    return


# ============================================================
# Freie Exploration & Zusammenfassung
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration

        Experimentieren Sie selbst:

        - Fügen Sie einen neuen Verein hinzu (ohne Spieler)
        - Ändern Sie einen Vereinsort
        - Löschen Sie einen Spieler
        - Entwerfen Sie ein eigenes ER-Diagramm für ein Szenario Ihrer Wahl

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

        ### Teil 1: Redundanz und Anomalien

        | Problem | Ursache | Lösung |
        |---------|---------|---------|
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

        **Nächste Session:** Session 6 -- Relationales Modell & Transformation (ER -> SQL CREATE TABLE)
        """
    )
    return


if __name__ == "__main__":
    app.run()
