import marimo

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 2: SQL für Datenexploration",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 2: SQL für Datenexploration

        In dieser Session lernen Sie:

        - Ergebnisse **sortieren** mit `ORDER BY`
        - Ergebnisse **begrenzen** mit `LIMIT`
        - **Eindeutige Werte** finden mit `DISTINCT`
        - **Mustersuche** mit `LIKE`
        - Mit **NULL-Werten** umgehen

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
        ## Daten laden

        Wir arbeiten heute mit zwei Datensätzen:
        1. **Bundesliga-Tabelle** (wie letzte Woche)
        2. **Spieler-Daten** (mit fehlenden Werten für NULL-Übungen)
        """
    )
    return


@app.cell(hide_code=True)
def _():
    import pandas as pd
    import lxml  # Pre-load for pandas read_html parser

    # Configure pandas for plain text display
    pd.set_option('display.notebook_repr_html', False)

    def lade_bundesliga_tabelle(saison: str = "2026") -> pd.DataFrame:
        """Lädt die aktuelle Bundesliga-Tabelle von fussballdaten.de."""
        url = f"https://www.fussballdaten.de/bundesliga/{saison}/tabelle/"

        def get_fallback():
            return pd.DataFrame({
                "Mannschaft": ["Bayern München", "Borussia Dortmund", "VfB Stuttgart",
                              "RB Leipzig", "Bayer Leverkusen", "Eintracht Frankfurt",
                              "SC Freiburg", "TSG Hoffenheim", "Werder Bremen", "VfL Wolfsburg",
                              "1. FC Union Berlin", "FC Augsburg", "Borussia M'gladbach",
                              "1. FSV Mainz 05", "1. FC Heidenheim", "VfL Bochum",
                              "FC St. Pauli", "Holstein Kiel"],
                "Spiele": [19, 19, 19, 18, 18, 19, 18, 18, 19, 19, 18, 19, 18, 19, 19, 19, 18, 19],
                "Siege": [16, 12, 11, 11, 10, 9, 9, 11, 7, 6, 6, 6, 6, 5, 5, 3, 4, 3],
                "Unentschieden": [2, 6, 3, 2, 2, 6, 3, 3, 6, 7, 5, 5, 3, 6, 4, 5, 3, 3],
                "Niederlagen": [1, 1, 5, 5, 6, 4, 6, 4, 6, 6, 7, 8, 9, 8, 10, 11, 11, 13],
                "ToreGeschossen": [72, 38, 40, 32, 41, 35, 28, 38, 29, 31, 22, 21, 26, 24, 28, 17, 14, 18],
                "ToreKassiert": [16, 17, 30, 20, 31, 24, 26, 22, 32, 34, 24, 32, 33, 28, 40, 38, 25, 45],
                "Tordifferenz": [56, 21, 10, 12, 10, 11, 2, 16, -3, -3, -2, -11, -7, -4, -12, -21, -11, -27],
                "Punkte": [50, 42, 36, 35, 32, 33, 30, 36, 27, 25, 23, 23, 21, 21, 19, 14, 15, 12]
            }), "Offline-Beispieldaten (Saison 2024/25)"

        try:
            df = None
            for parser in ['html.parser', 'lxml', 'html5lib']:
                try:
                    tabellen = pd.read_html(url, flavor=parser)
                    df = tabellen[0]
                    break
                except:
                    continue

            if df is None:
                return get_fallback()

            spalten_mapping = {
                "Pts": "Punkte", "Pkt": "Punkte",
                "S": "Siege",
                "D": "Unentschieden", "U": "Unentschieden",
                "L": "Niederlagen", "V": "Niederlagen",
                "Sp.": "Spiele",
                "Goals": "Tore", "Tore": "Tore",
                "Diff.": "Tordifferenz"
            }
            df = df.rename(columns={k: v for k, v in spalten_mapping.items() if k in df.columns})

            if "Tordifferenz" not in df.columns and "Tore" in df.columns:
                df[["ToreGeschossen", "ToreKassiert"]] = df["Tore"].str.split(":", expand=True).astype(int)
                df["Tordifferenz"] = df["ToreGeschossen"] - df["ToreKassiert"]
            elif "Tordifferenz" in df.columns:
                df["Tordifferenz"] = pd.to_numeric(df["Tordifferenz"], errors="coerce").fillna(0).astype(int)
                if "Tore" in df.columns:
                    df[["ToreGeschossen", "ToreKassiert"]] = df["Tore"].str.split(":", expand=True).astype(int)

            gewuenschte_spalten = ["Mannschaft", "Spiele", "Siege", "Unentschieden", "Niederlagen",
                                   "ToreGeschossen", "ToreKassiert", "Tordifferenz", "Punkte"]
            df = df[[c for c in gewuenschte_spalten if c in df.columns]]
            quelle = f"Live von fussballdaten.de (Saison {saison})"

        except:
            return get_fallback()

        return df, quelle

    bundesliga, daten_quelle = lade_bundesliga_tabelle("2026")
    return bundesliga, daten_quelle, lade_bundesliga_tabelle, pd


@app.cell(hide_code=True)
def _(pd):
    # Spieler-Daten mit NULL-Werten für Übungen
    spieler = pd.DataFrame({
        "Name": ["Müller", "Neuer", "Kimmich", "Sané", "Musiala", "Gündogan",
                 "Havertz", "Wirtz", "Füllkrug", "Schlotterbeck", "Rüdiger", "Tah"],
        "Vorname": ["Thomas", "Manuel", "Joshua", "Leroy", "Jamal", "İlkay",
                    "Kai", "Florian", "Niclas", "Nico", "Antonio", "Jonathan"],
        "Position": ["Sturm", "Tor", "Mittelfeld", "Sturm", "Mittelfeld", "Mittelfeld",
                     "Sturm", "Mittelfeld", "Sturm", "Abwehr", "Abwehr", "Abwehr"],
        "Verein": ["Bayern München", "Bayern München", "Bayern München", "Bayern München",
                   "Bayern München", None, "Arsenal", "Bayer Leverkusen",
                   "West Ham", "Borussia Dortmund", "Real Madrid", "Bayer Leverkusen"],
        "Tore": [8, 0, 3, 5, 12, None, 9, 11, 6, 1, 2, None],
        "Vorlagen": [4, None, 8, 3, 7, 2, 5, 9, 2, None, 1, 0],
        "Spitzname": ["Mülli", None, "Jo", None, None, "Günni", None, "Flo", "Fülle", None, "Rüdi", None]
    })
    # Konvertiere zu nullable integer types
    spieler["Tore"] = spieler["Tore"].astype("Int64")
    spieler["Vorlagen"] = spieler["Vorlagen"].astype("Int64")
    spieler
    return (spieler,)


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle Bundesliga:** {daten_quelle}

        **Verfügbare Spalten Bundesliga:** Mannschaft, Spiele, Siege, Unentschieden, Niederlagen, ToreGeschossen, ToreKassiert, Tordifferenz, Punkte

        **Verfügbare Spalten Spieler:** Name, Vorname, Position, Verein, Tore, Vorlagen, Spitzname

        ---

        ## Phase 2: Daten sortieren mit ORDER BY (25 Minuten)

        ### 🟢 Aufgabe 2.1: Einfache Sortierung (geführt)

        Sortieren Sie die Bundesliga-Tabelle nach Punkten (absteigend):
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        ORDER BY Punkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 2.2: Aufsteigende Sortierung (geführt)

        Zeigen Sie die Teams mit der schlechtesten Tordifferenz zuerst:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Tordifferenz
        FROM bundesliga
        ORDER BY Tordifferenz ASC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 2.3: Mehrere Sortierkriterien (scaffolded)

        Sortieren Sie nach Punkten (absteigend), bei Gleichstand nach Tordifferenz.
        Ergänzen Sie das zweite Sortierkriterium:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ergänzen Sie: ORDER BY Punkte DESC, ??? DESC
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte, Tordifferenz
        FROM bundesliga
        ORDER BY Punkte DESC, Tordifferenz DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟣 Aufgabe 2.4: Vorhersage - Top 5

        **Bevor Sie ausführen:** Wie viele Zeilen wird das Ergebnis haben?

        ```sql
        SELECT Mannschaft, Punkte
        FROM bundesliga
        ORDER BY Punkte DESC
        LIMIT 5
        ```
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        ORDER BY Punkte DESC
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Antwort:** 5 Zeilen - LIMIT begrenzt auf die ersten 5 Ergebnisse.

        ---

        ### 🔵 Aufgabe 2.5: Selbstständig - Abstiegskandidaten

        Finden Sie die 3 Teams mit den wenigsten Punkten.
        Zeigen Sie Mannschaft und Punkte.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        ORDER BY Punkte ASC
        LIMIT 3
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.6: Selbstständig - Plätze 6-10

        Zeigen Sie die Teams auf den Plätzen 6-10 der Tabelle.

        (Hinweis: Verwenden Sie LIMIT und OFFSET)
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        ORDER BY Punkte DESC
        LIMIT 5 OFFSET 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 2.7: Debugging - Reihenfolge

        Diese Abfrage hat einen Fehler. Finden und beheben Sie ihn:

        ```sql
        SELECT Mannschaft, Punkte
        ORDER BY Punkte DESC
        FROM bundesliga
        LIMIT 5
        ```
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Korrigieren Sie die Reihenfolge der Klauseln:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        ORDER BY Punkte DESC
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 2.8: Debugging - ASC vs DESC

        Diese Abfrage soll die Top-Torjäger zeigen (meiste Tore zuerst).
        Aber sie zeigt das Gegenteil. Was ist falsch?

        ```sql
        SELECT Mannschaft, ToreGeschossen
        FROM bundesliga
        ORDER BY ToreGeschossen
        LIMIT 5
        ```
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Korrigieren Sie die Sortierrichtung:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, ToreGeschossen
        FROM bundesliga
        ORDER BY ToreGeschossen DESC
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: DISTINCT und LIKE (25 Minuten)

        ### 🟢 Aufgabe 4.1: Eindeutige Werte mit DISTINCT (geführt)

        Welche verschiedenen Spielstände (Anzahl Spiele) gibt es?
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT DISTINCT Spiele
        FROM bundesliga
        ORDER BY Spiele
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.2: DISTINCT mit Spielerdaten (geführt)

        Welche verschiedenen Positionen gibt es bei den Spielern?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT DISTINCT Position
        FROM spieler
        ORDER BY Position
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 4.3: Kombinationen finden (scaffolded)

        Finden Sie alle eindeutigen Kombinationen von Position und Verein.
        Ergänzen Sie die Spalten:
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ergänzen Sie die zweite Spalte nach Position:
    _df = mo.sql(
        f"""
        SELECT DISTINCT Position, Verein
        FROM spieler
        ORDER BY Position, Verein
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟣 Aufgabe 4.4: Vorhersage - DISTINCT Ergebnis

        **Bevor Sie ausführen:** Wie viele verschiedene Vereine gibt es in der Spieler-Tabelle?

        Zählen Sie die nicht-NULL Werte!
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT DISTINCT Verein
        FROM spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Antwort:** 6 Vereine (Bayern München, Borussia Dortmund, Arsenal, Bayer Leverkusen, West Ham, Real Madrid) + 1 NULL-Wert = 7 Zeilen.

        ---

        ### 🟢 Aufgabe 4.5: Mustersuche mit LIKE (geführt)

        Finden Sie alle Teams, deren Name mit 'B' beginnt:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft
        FROM bundesliga
        WHERE Mannschaft LIKE 'B%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.6: Selbstständig - LIKE mit Endung

        Finden Sie alle Spieler, deren Nachname auf 'er' endet:
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        SELECT Name, Vorname
        FROM spieler
        WHERE Name LIKE '%er'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.7: Selbstständig - LIKE mit Enthält

        Finden Sie alle Teams, die "FC" im Namen haben:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        SELECT Mannschaft
        FROM bundesliga
        WHERE Mannschaft LIKE '%FC%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 4.8: Debugging - LIKE Muster

        Diese Abfrage soll alle Teams finden, die mit "1." beginnen (also 1. FC etc.).
        Sie findet aber nichts. Was ist das Problem?

        ```sql
        SELECT Mannschaft
        FROM bundesliga
        WHERE Mannschaft LIKE '1.%'
        ```

        (Hinweis: Es funktioniert tatsächlich! Prüfen Sie, ob es solche Teams gibt.)
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Testen Sie die Abfrage - sie ist korrekt!
    _df = mo.sql(
        f"""
        SELECT Mannschaft
        FROM bundesliga
        WHERE Mannschaft LIKE '1.%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Umgang mit NULL-Werten (40 Minuten)

        NULL bedeutet "unbekannt" oder "nicht vorhanden" - es ist NICHT dasselbe wie 0 oder ein leerer String!

        ### 🟢 Aufgabe 6.1: NULL-Werte finden (geführt)

        Welche Spieler haben keinen Verein eingetragen (NULL)?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Name, Vorname, Verein
        FROM spieler
        WHERE Verein IS NULL
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.2: IS NOT NULL (geführt)

        Welche Spieler haben Tore eingetragen (nicht NULL)?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Name, Tore
        FROM spieler
        WHERE Tore IS NOT NULL
        ORDER BY Tore DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟣 Aufgabe 6.3: Vorhersage - NULL in Berechnungen

        **Bevor Sie ausführen:** Was passiert bei dieser Berechnung für Spieler mit NULL-Werten?

        ```sql
        SELECT Name, Tore, Vorlagen, Tore + Vorlagen AS Scorerpunkte
        FROM spieler
        ```
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Name, Tore, Vorlagen, Tore + Vorlagen AS Scorerpunkte
        FROM spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Antwort:** Wenn Tore ODER Vorlagen NULL ist, ist auch Scorerpunkte NULL!
        Jede Rechnung mit NULL ergibt NULL.

        ---

        ### 🟢 Aufgabe 6.4: COALESCE - NULL ersetzen (geführt)

        Zeigen Sie alle Spieler mit Toren, ersetzen Sie NULL durch 0:
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT
            Name,
            Tore AS Tore_Original,
            COALESCE(Tore, 0) AS Tore_Bereinigt
        FROM spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 6.5: COALESCE anwenden (scaffolded)

        Berechnen Sie Scorerpunkte (Tore + Vorlagen), aber ersetzen Sie NULL durch 0.
        Ergänzen Sie die COALESCE-Aufrufe:
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ergänzen Sie: COALESCE(???, 0) + COALESCE(???, 0)
    _df = mo.sql(
        f"""
        SELECT
            Name,
            COALESCE(Tore, 0) AS Tore,
            COALESCE(Vorlagen, 0) AS Vorlagen,
            COALESCE(Tore, 0) + COALESCE(Vorlagen, 0) AS Scorerpunkte
        FROM spieler
        ORDER BY Scorerpunkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.6: COALESCE mit mehreren Fallbacks (geführt)

        Erstellen Sie einen Anzeigenamen: Spitzname > Vorname > Name
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT
            Name,
            Spitzname,
            Vorname,
            COALESCE(Spitzname, Vorname, Name) AS Anzeigename
        FROM spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.7: Selbstständig - Spieler ohne Spitznamen

        Finden Sie alle Spieler, die keinen Spitznamen haben.
        Zeigen Sie Name, Vorname und Spitzname.
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        SELECT Name, Vorname, Spitzname
        FROM spieler
        WHERE Spitzname IS NULL
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.8: Selbstständig - Spieler mit vollständigen Daten

        Finden Sie alle Spieler, bei denen sowohl Tore ALS AUCH Vorlagen eingetragen sind (nicht NULL).
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        SELECT Name, Tore, Vorlagen
        FROM spieler
        WHERE Tore IS NOT NULL AND Vorlagen IS NOT NULL
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.9: Debugging - = NULL vs IS NULL

        Diese Abfrage soll Spieler ohne Verein finden, aber sie liefert keine Ergebnisse.
        Was ist falsch?

        ```sql
        SELECT Name, Verein
        FROM spieler
        WHERE Verein = NULL
        ```
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Korrigieren Sie den Vergleich mit NULL:
    _df = mo.sql(
        f"""
        SELECT Name, Verein
        FROM spieler
        WHERE Verein IS NULL
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.10: Debugging - NULL in Sortierung

        Schauen Sie sich die Sortierung an. Wo erscheinen die NULL-Werte?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Name, Tore
        FROM spieler
        ORDER BY Tore DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** NULL-Werte erscheinen am Ende bei DESC oder am Anfang bei ASC (datenbankabhängig).

        ---

        ### 🔵 Aufgabe 6.11: Selbstständig - Top-Torjäger mit COALESCE

        Erstellen Sie eine Rangliste der Spieler nach Scorerpunkten (Tore + Vorlagen).
        - Ersetzen Sie NULL-Werte durch 0
        - Sortieren Sie absteigend
        - Zeigen Sie nur die Top 5
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        SELECT
            Name,
            COALESCE(Tore, 0) AS Tore,
            COALESCE(Vorlagen, 0) AS Vorlagen,
            COALESCE(Tore, 0) + COALESCE(Vorlagen, 0) AS Scorerpunkte
        FROM spieler
        ORDER BY Scorerpunkte DESC
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.12: Kombination aller Konzepte

        Finden Sie alle Mittelfeldspieler, die mindestens 5 Scorerpunkte haben (Tore + Vorlagen).
        Behandeln Sie NULL-Werte als 0.
        Sortieren Sie nach Scorerpunkten absteigend.
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        SELECT
            Name,
            Position,
            COALESCE(Tore, 0) + COALESCE(Vorlagen, 0) AS Scorerpunkte
        FROM spieler
        WHERE Position = 'Mittelfeld'
          AND COALESCE(Tore, 0) + COALESCE(Vorlagen, 0) >= 5
        ORDER BY Scorerpunkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration

        Probieren Sie eigene Abfragen! Ideen:

        ### Bundesliga-Daten:
        - Top 3 Torjäger (nach ToreGeschossen)
        - Teams mit "burg" im Namen
        - Die 3 Teams mit den wenigsten Niederlagen

        ### Spieler-Daten:
        - Spieler ohne Spitznamen, sortiert nach Position
        - Vereine mit mehreren Spielern (DISTINCT hilft!)
        - Erstellen Sie eine vollständige Spielerliste mit allen Daten bereinigt
        """
    )
    return


@app.cell
def _(bundesliga, mo, spieler):
    # Ihre eigene Abfrage hier:
    _df = mo.sql(
        f"""
        SELECT *
        FROM spieler
        ORDER BY Name
        """
    )
    return


@app.cell
def _(bundesliga, mo, spieler):
    # Noch eine eigene Abfrage:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, ToreGeschossen
        FROM bundesliga
        ORDER BY ToreGeschossen DESC
        LIMIT 3
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | Syntax | Beispiel |
        |---------|--------|----------|
        | Aufsteigend sortieren | `ORDER BY spalte ASC` | `ORDER BY Punkte ASC` |
        | Absteigend sortieren | `ORDER BY spalte DESC` | `ORDER BY Punkte DESC` |
        | Begrenzen | `LIMIT n` | `LIMIT 5` |
        | Überspringen | `LIMIT n OFFSET m` | `LIMIT 5 OFFSET 5` |
        | Eindeutige Werte | `SELECT DISTINCT` | `SELECT DISTINCT Position` |
        | Muster (beginnt mit) | `LIKE 'X%'` | `WHERE Name LIKE 'M%'` |
        | Muster (enthält) | `LIKE '%X%'` | `WHERE Name LIKE '%er%'` |
        | NULL prüfen | `IS NULL` / `IS NOT NULL` | `WHERE Tore IS NULL` |
        | NULL ersetzen | `COALESCE(wert, ersatz)` | `COALESCE(Tore, 0)` |

        ### Häufige Fehler vermeiden:
        - ✅ `IS NULL` statt `= NULL`
        - ✅ Reihenfolge: SELECT → FROM → WHERE → ORDER BY → LIMIT
        - ✅ Bei Berechnungen: COALESCE verwenden, um NULL zu ersetzen
        - ✅ ASC ist Standard, DESC muss explizit angegeben werden

        **Nächste Session:** Aggregation & Gruppierung (COUNT, SUM, AVG, GROUP BY)
        """
    )
    return


if __name__ == "__main__":
    app.run()
