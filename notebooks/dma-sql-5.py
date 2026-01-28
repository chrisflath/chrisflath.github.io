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
    import pandas as pd

    # Die "schlechte" Mega-Tabelle mit Redundanzen
    spieler_schlecht = pd.DataFrame({
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
    return pd, spieler_schlecht


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
        ---

        ## Phase 3: Anomalien erleben

        ### Aufgabe 5.3: Änderungsanomalie provozieren

        **Szenario:** Bayern München baut ein neues Stadion namens "FC Bayern Arena".

        Führen wir ein UPDATE durch -- aber "vergessen" wir absichtlich eine Zeile:
        """
    )
    return


@app.cell
def _(pd, spieler_schlecht):
    # Kopie erstellen für die Demonstration
    spieler_nach_update = spieler_schlecht.copy()

    # "Fehlerhaftes" Update: Wir ändern nur 4 von 5 Bayern-Spielern
    maske = (spieler_nach_update["Verein"] == "Bayern München") & \
            (spieler_nach_update["Spieler"] != "Musiala")
    spieler_nach_update.loc[maske, "Stadion"] = "FC Bayern Arena"

    spieler_nach_update
    return maske, spieler_nach_update


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

        ### Aufgabe 5.4: Löschanomalie erleben

        **Szenario:** Wirtz, Tah und Frimpong wechseln alle ins Ausland.
        Wir löschen sie aus unserer Tabelle.
        """
    )
    return


@app.cell
def _(pd, spieler_schlecht):
    # Zurück zur Original-Tabelle
    spieler_vor_delete = spieler_schlecht.copy()

    # Alle Leverkusen-Spieler löschen
    spieler_nach_delete = spieler_vor_delete[
        spieler_vor_delete["Verein"] != "Bayer Leverkusen"
    ].copy()

    spieler_nach_delete
    return spieler_nach_delete, spieler_vor_delete


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Was ist passiert?** Wir haben alle Informationen über Bayer Leverkusen verloren!

        - Wo ist der Vereinssitz? Weg.
        - Wie heisst das Stadion? Weg.
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
def _(pd):
    # Tabelle 1: Vereine (jeder Verein nur EINMAL)
    vereine = pd.DataFrame({
        "Verein_ID": [1, 2, 3],
        "Verein": ["Bayern München", "Bayer Leverkusen", "West Ham United"],
        "Vereinsort": ["München", "Leverkusen", "London"],
        "Stadion": ["Allianz Arena", "BayArena", "London Stadium"],
        "Gründungsjahr": [1900, 1904, 1895]
    })
    vereine
    return (vereine,)


@app.cell
def _(pd):
    # Tabelle 2: Spieler (mit Verweis auf Verein)
    spieler_gut = pd.DataFrame({
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

        ---

        ### Aufgabe 5.6: Änderung testen (verbessertes Design)

        Jetzt ändern wir das Bayern-Stadion -- diesmal richtig:
        """
    )
    return


@app.cell
def _(pd, vereine):
    # Kopie für Update
    vereine_update = vereine.copy()

    # Stadion ändern -- nur EINE Zeile!
    vereine_update.loc[vereine_update["Verein"] == "Bayern München", "Stadion"] = "FC Bayern Arena"

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
def _(spieler_gut):
    # Leverkusen-Spieler löschen (Verein_ID = 2)
    spieler_nach_delete_gut = spieler_gut[spieler_gut["Verein_ID"] != 2].copy()
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
