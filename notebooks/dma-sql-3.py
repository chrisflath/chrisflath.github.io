# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "polars",
#     "pandas",
#     "plotly",
# ]
# ///

import marimo

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 3: Aggregation & Gruppierung — Übungen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 3: Aggregation & Gruppierung — Übungen

        Theorie und geführte Beispiele → **03-sql-aggregation-guide.py**

        **Aufgabentypen:**
        - 🟡 **Scaffolded**: Teillösung zum Ergänzen
        - 🔵 **Selbstständig**: Eigene Lösung schreiben
        - 🔴 **Debugging**: Fehler finden und beheben
        - ⭐ **Exploration**: Offene Herausforderungen

        > **Hinweis:** 🟡-Aufgaben enthalten `???` als Platzhalter. Die Zelle zeigt einen SQL-Fehler, bis Sie die `???` durch die richtige Lösung ersetzen — das ist Absicht!

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Daten laden
        """
    )
    return


@app.cell
def _():
    import polars as pl

    def lade_bundesliga_tabelle(saison: str = "2026"):
        """Lädt die aktuelle Bundesliga-Tabelle von fussballdaten.de."""
        import pandas as pd

        url = f"https://www.fussballdaten.de/bundesliga/{saison}/tabelle/"

        try:
            for parser in ['html.parser', 'lxml', 'html5lib']:
                try:
                    tabellen = pd.read_html(url, flavor=parser)
                    df = tabellen[0]
                    break
                except Exception:
                    continue
            else:
                raise ImportError("No HTML parser available")

            spalten_mapping = {
                "Pts": "Punkte", "Pkt": "Punkte",
                "S": "Siege",
                "D": "Unentschieden", "U": "Unentschieden",
                "L": "Niederlagen", "V": "Niederlagen",
                "Sp.": "Spiele",
                "Goals": "Tore_roh", "Tore": "Tore_roh",
                "Diff.": "Tordifferenz"
            }
            df = df.rename(columns={k: v for k, v in spalten_mapping.items() if k in df.columns})

            if "Tordifferenz" not in df.columns and "Tore_roh" in df.columns:
                df[["Tore", "Gegentore"]] = df["Tore_roh"].str.split(":", expand=True).astype(int)
                df["Tordifferenz"] = df["Tore"] - df["Gegentore"]
            elif "Tordifferenz" in df.columns:
                df["Tordifferenz"] = pd.to_numeric(df["Tordifferenz"], errors="coerce").fillna(0).astype(int)
                if "Tore_roh" in df.columns:
                    df[["Tore", "Gegentore"]] = df["Tore_roh"].str.split(":", expand=True).astype(int)

            gewünschte_spalten = ["Mannschaft", "Spiele", "Siege", "Unentschieden", "Niederlagen",
                                   "Tore", "Gegentore", "Tordifferenz", "Punkte"]
            df = df[[c for c in gewünschte_spalten if c in df.columns]]
            quelle = f"Live von fussballdaten.de (Saison {saison})"

        except Exception as e:
            df = pd.DataFrame({
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
                "Tore": [72, 38, 40, 32, 41, 35, 28, 38, 29, 31, 22, 21, 26, 24, 28, 17, 14, 18],
                "Gegentore": [16, 17, 30, 20, 31, 24, 26, 22, 32, 34, 24, 32, 33, 28, 40, 38, 25, 45],
                "Tordifferenz": [56, 21, 10, 12, 10, 11, 2, 16, -3, -3, -2, -11, -7, -4, -12, -21, -11, -27],
                "Punkte": [50, 42, 36, 35, 32, 33, 30, 36, 27, 25, 23, 23, 21, 21, 19, 14, 15, 12]
            })
            quelle = f"Offline-Beispieldaten"

        return pl.from_pandas(df), quelle

    bundesliga, daten_quelle = lade_bundesliga_tabelle("2026")
    return bundesliga, daten_quelle, lade_bundesliga_tabelle, pl


@app.cell
def _():
    import plotly.express as px
    return (px,)


@app.cell
def _(pl):
    # Erweiterte Spieler-Daten für Aggregationsübungen
    spieler = pl.DataFrame({
        "Name": ["Müller", "Neuer", "Kimmich", "Sané", "Musiala", "Gündogan",
                 "Havertz", "Wirtz", "Füllkrug", "Schlotterbeck", "Rüdiger", "Tah",
                 "Gnabry", "Goretzka", "ter Stegen", "Baumann"],
        "Vorname": ["Thomas", "Manuel", "Joshua", "Leroy", "Jamal", "İlkay",
                    "Kai", "Florian", "Niclas", "Nico", "Antonio", "Jonathan",
                    "Serge", "Leon", "Marc-André", "Oliver"],
        "Position": ["Sturm", "Tor", "Mittelfeld", "Sturm", "Mittelfeld", "Mittelfeld",
                     "Sturm", "Mittelfeld", "Sturm", "Abwehr", "Abwehr", "Abwehr",
                     "Sturm", "Mittelfeld", "Tor", "Tor"],
        "Verein": ["Bayern München", "Bayern München", "Bayern München", "Bayern München",
                   "Bayern München", "FC Barcelona", "Arsenal", "Bayer Leverkusen",
                   "West Ham", "Borussia Dortmund", "Real Madrid", "Bayer Leverkusen",
                   "Bayern München", "Bayern München", "FC Barcelona", "TSG Hoffenheim"],
        "Tore": [8, 0, 3, 5, 12, 4, 9, 11, 6, 1, 2, 0, 7, 2, 0, 0],
        "Vorlagen": [4, 0, 8, 3, 7, 2, 5, 9, 2, 0, 1, 0, 4, 3, 0, 0],
        "Alter": [35, 38, 29, 28, 21, 33, 25, 21, 31, 24, 31, 28, 28, 29, 32, 34],
        "Länderspiele": [131, 118, 91, 67, 35, 82, 47, 28, 20, 12, 70, 32, 42, 57, 40, 5]
    })
    spieler
    return (spieler,)


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle Bundesliga:** {daten_quelle}

        ---

        ## Phase 2: Aggregatfunktionen

        ### Aufgabe 2.1: Geführtes Beispiel — COUNT

        Wie viele Teams sind in der Bundesliga?
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS Anzahl_Teams
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 2.2: SUM und AVG

        Wie viele Tore wurden insgesamt geschossen? Wie viele im Durchschnitt?
        Ergänzen Sie die fehlenden Aggregatfunktionen:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT
            ???(Tore) AS Gesamttore,
            ???(Tore) AS Durchschnitt_Tore
        FROM bundesliga
        -- Tipp: SUM für die Gesamtsumme, AVG für den Durchschnitt
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    SUM(Tore) AS Gesamttore,
    AVG(Tore) AS Durchschnitt_Tore
FROM bundesliga
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.3: MIN und MAX

        Finden Sie die beste und schlechteste Tordifferenz. Berechnen Sie auch die Spannweite (Differenz zwischen Maximum und Minimum).
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        -- 🔵 Schreiben Sie Ihre Abfrage:
        SELECT 'Ihre Lösung hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    MIN(Tordifferenz) AS Schlechteste,
    MAX(Tordifferenz) AS Beste,
    MAX(Tordifferenz) - MIN(Tordifferenz) AS Spannweite
FROM bundesliga
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.4: Mehrere Aggregationen kombinieren

        Erstellen Sie eine Übersicht der Bundesliga mit: Anzahl Teams, Gesamtsiege, Durchschnittspunkte, niedrigste und höchste Punktzahl.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        -- 🔵 Schreiben Sie Ihre Abfrage:
        SELECT 'Ihre Lösung hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    COUNT(*) AS Teams,
    SUM(Siege) AS Gesamtsiege,
    AVG(Punkte) AS Schnitt_Punkte,
    MIN(Punkte) AS Min_Punkte,
    MAX(Punkte) AS Max_Punkte
FROM bundesliga
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: GROUP BY - Daten gruppieren

        ### Aufgabe 4.1: Geführtes Beispiel — Einfache Gruppierung

        Wie viele Spieler gibt es pro Position?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Position, COUNT(*) AS Anzahl
        FROM spieler
        GROUP BY Position
        ORDER BY Anzahl DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 4.2: Durchschnitt pro Gruppe

        Wie viele Tore schießen die verschiedenen Positionen im Durchschnitt?
        Ergänzen Sie die fehlenden Aggregatfunktionen:
        """
    )
    return


@app.cell
def _(mo, spieler):
    tore_by_position = mo.sql(
        f"""
        SELECT
            Position,
            COUNT(*) AS Spieler,
            ???(Tore) AS Schnitt_Tore,
            ???(Tore) AS Gesamt_Tore
        FROM spieler
        GROUP BY Position
        ORDER BY Schnitt_Tore DESC
        -- Tipp: AVG für Durchschnitt, SUM für Summe
        """
    )
    return (tore_by_position,)


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Position,
    COUNT(*) AS Spieler,
    AVG(Tore) AS Schnitt_Tore,
    SUM(Tore) AS Gesamt_Tore
FROM spieler
GROUP BY Position
ORDER BY Schnitt_Tore DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Visualisierung: Aggregierte Daten als Balkendiagramm
        """
    )
    return


@app.cell
def _(px, tore_by_position):
    px.bar(
        tore_by_position,
        x="Position",
        y="Schnitt_Tore",
        title="Durchschnittliche Tore nach Position",
        labels={"Position": "Position", "Schnitt_Tore": "Ø Tore"},
        labels={"Position": "Position", "Schnitt_Tore": "Ø Tore"}
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 4.3: Scaffolded — Gruppierung vervollständigen

        Welcher Verein hat die meisten Nationalspieler?
        Ergänzen Sie die `GROUP BY`-Spalte und die Sortierung:
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT
            Verein,
            COUNT(*) AS Nationalspieler
        FROM spieler
        -- Ergänzen Sie: Nach welcher Spalte gruppieren?
        GROUP BY ???
        -- Ergänzen Sie: Absteigend nach Anzahl sortieren
        ORDER BY ???
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Verein,
    COUNT(*) AS Nationalspieler
FROM spieler
GROUP BY Verein
ORDER BY Nationalspieler DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 4.4: Scaffolded — Mehrere Aggregatfunktionen

        Erweitern Sie die Abfrage: Zeigen Sie pro Verein die Anzahl Spieler,
        die Gesamttore und das Durchschnittsalter.
        Ergänzen Sie die fehlenden Aggregatfunktionen:
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT
            Verein,
            COUNT(*) AS Nationalspieler,
            ???(Tore) AS Tore_Gesamt,
            ???("Alter") AS Durchschnittsalter
        FROM spieler
        GROUP BY Verein
        ORDER BY Nationalspieler DESC
        -- Tipp: SUM für Gesamttore, AVG für Durchschnitt
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Verein,
    COUNT(*) AS Nationalspieler,
    SUM(Tore) AS Tore_Gesamt,
    AVG("Alter") AS Durchschnittsalter
FROM spieler
GROUP BY Verein
ORDER BY Nationalspieler DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.5: Bundesliga nach Spielanzahl

        Welche Teams haben wie viele Spiele absolviert? Zeigen Sie die Spieleanzahl, die Anzahl Teams und die Durchschnittspunkte pro Gruppe.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        -- 🔵 Schreiben Sie Ihre Abfrage:
        SELECT 'Ihre Lösung hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Spiele,
    COUNT(*) AS Anzahl_Teams,
    AVG(Punkte) AS Schnitt_Punkte
FROM bundesliga
GROUP BY Spiele
ORDER BY Spiele
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: HAVING - Filter auf Gruppen

        ### Aufgabe 6.1: Geführtes Beispiel — HAVING

        Welche Positionen haben mehr als 3 Spieler?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Position, COUNT(*) AS Anzahl
        FROM spieler
        GROUP BY Position
        HAVING COUNT(*) > 3
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 6.2: HAVING mit AVG

        Welche Positionen haben im Durchschnitt mehr als 5 Tore?
        Ergänzen Sie die HAVING-Bedingung:
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Position, AVG(Tore) AS Schnitt_Tore
        FROM spieler
        GROUP BY Position
        HAVING ???
        ORDER BY Schnitt_Tore DESC
        -- Tipp: Verwenden Sie AVG(Tore) > 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Position, AVG(Tore) AS Schnitt_Tore
FROM spieler
GROUP BY Position
HAVING AVG(Tore) > 5
ORDER BY Schnitt_Tore DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.3: WHERE und HAVING kombinieren

        Welche Vereine haben mehr als 2 Spieler unter 30 Jahren? Nutzen Sie WHERE für die Altersfilterung und HAVING für die Gruppenfilterung.
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        -- 🔵 Schreiben Sie Ihre Abfrage:
        -- Hinweis: WHERE filtert Zeilen VOR der Gruppierung
        --          HAVING filtert Gruppen NACH der Gruppierung
        SELECT 'Ihre Lösung hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Verein, COUNT(*) AS Junge_Spieler
FROM spieler
WHERE "Alter" < 30
GROUP BY Verein
HAVING COUNT(*) >= 2
ORDER BY Junge_Spieler DESC
```

**Erklärung:** `WHERE "Alter" < 30` filtert zuerst die Spieler unter 30. Dann gruppiert `GROUP BY Verein` die verbleibenden Spieler. `HAVING COUNT(*) >= 2` behält nur Vereine mit mindestens 2 jungen Spielern.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.4: Komplexe Analyse

        Finden Sie Vereine mit hoher Torbeteiligung: Zeigen Sie Verein, Summe Tore, Summe Vorlagen und Scorerpunkte (Tore + Vorlagen) — aber nur Vereine mit mehr als 20 Scorerpunkten.
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        -- 🔵 Schreiben Sie Ihre Abfrage:
        SELECT 'Ihre Lösung hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Verein,
    SUM(Tore) AS Tore,
    SUM(Vorlagen) AS Vorlagen,
    SUM(Tore) + SUM(Vorlagen) AS Scorerpunkte
FROM spieler
GROUP BY Verein
HAVING SUM(Tore) + SUM(Vorlagen) > 20
ORDER BY Scorerpunkte DESC
```

**Erklärung:** `HAVING` kann auch Ausdrücke mit mehreren Aggregatfunktionen enthalten. Hier filtern wir nach der Summe von Toren und Vorlagen.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.5: Bundesliga-Analyse mit CASE

        Klassifizieren Sie Teams in Punktebereiche (Top 40+, Oberes Mittelfeld 30-39, Unteres Mittelfeld 20-29, Abstiegskampf <20) und zeigen Sie nur Bereiche mit mehr als 3 Teams.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        -- 🔵 Schreiben Sie Ihre Abfrage:
        -- Hinweis: Verwenden Sie CASE WHEN ... THEN ... END
        SELECT 'Ihre Lösung hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    CASE
        WHEN Punkte >= 40 THEN 'Top (40+)'
        WHEN Punkte >= 30 THEN 'Oberes Mittelfeld (30-39)'
        WHEN Punkte >= 20 THEN 'Unteres Mittelfeld (20-29)'
        ELSE 'Abstiegskampf (<20)'
    END AS Punktebereich,
    COUNT(*) AS Teams
FROM bundesliga
GROUP BY Punktebereich
HAVING COUNT(*) > 3
ORDER BY MIN(Punkte) DESC
```

**Erklärung:** `CASE WHEN` erzeugt eine berechnete Spalte, nach der man gruppieren kann. `HAVING COUNT(*) > 3` filtert dann nur die Punktebereiche mit mehr als 3 Teams.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.6: Debugging — WHERE statt HAVING

        Diese Abfrage soll Positionen mit mehr als 3 Spielern finden.
        **Führen Sie sie aus** — was ist das Problem?
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Diese Abfrage enthält einen Fehler — finden und beheben Sie ihn!
    _df = mo.sql(
        f"""
        SELECT Position, COUNT(*) AS Anzahl
        FROM spieler
        WHERE COUNT(*) > 3
        GROUP BY Position
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** `COUNT(*)` kann nicht in `WHERE` stehen! WHERE wird **vor** GROUP BY ausgeführt — zu diesem Zeitpunkt gibt es noch keine Gruppen.

Aggregatfunktionen in Filterbedingungen gehören in `HAVING` (wird **nach** GROUP BY ausgeführt):

```sql
-- Korrektur:
SELECT Position, COUNT(*) AS Anzahl
FROM spieler
GROUP BY Position
HAVING COUNT(*) > 3
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.7: Debugging — Fehlende GROUP BY

        Diese Abfrage soll die Gesamttore pro Verein zeigen.
        **Führen Sie sie aus** — warum funktioniert sie nicht?
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Diese Abfrage enthält einen Fehler — finden und beheben Sie ihn!
    _df = mo.sql(
        f"""
        SELECT Verein, SUM(Tore) AS Gesamttore
        FROM spieler
        ORDER BY Gesamttore DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** `Verein` im SELECT ohne `GROUP BY`! SQL weiß nicht, welcher Verein zur Gesamtsumme gehört.

**Goldene Regel:** Im SELECT nur Spalten aus GROUP BY oder Aggregatfunktionen!

```sql
-- Korrektur:
SELECT Verein, SUM(Tore) AS Gesamttore
FROM spieler
GROUP BY Verein
ORDER BY Gesamttore DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Visualisierung: Referenzlinien
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    team_punkte = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        ORDER BY Punkte DESC
        """
    )
    return (team_punkte,)


@app.cell
def _(bundesliga, mo, px, team_punkte):
    # Durchschnitt berechnen
    avg_result = mo.sql(f"SELECT AVG(Punkte) AS avg FROM bundesliga")
    avg_punkte = avg_result.item(0, 0)

    # Balkendiagramm mit Referenzlinie
    fig = px.bar(
        team_punkte,
        x="Mannschaft",
        y="Punkte",
        title="Bundesliga: Punkte pro Team mit Liga-Durchschnitt",
        labels={"Mannschaft": "Team", "Punkte": "Punkte"}
    )

    fig.add_hline(
        y=avg_punkte,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Ø {avg_punkte:.1f}",
        annotation_position="right"
    )

    fig.update_layout(xaxis_tickangle=-45)
    fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration — Herausforderungen

        **Tipp:** Vergleichen Sie Ihre Lösungen mit Ihrem Nachbarn — es gibt oft mehrere Wege zum gleichen Ergebnis!

        ### ⭐ Herausforderung 1: Offensive vs. Defensive Vereine

        Welche Vereine haben insgesamt mehr Tore als Vorlagen? Zeigen Sie Verein, Summe Tore und Summe Vorlagen.
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- ⭐ Offensive vs. Defensive Vereine
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Verein,
    SUM(Tore) AS Tore_Gesamt,
    SUM(Vorlagen) AS Vorlagen_Gesamt
FROM spieler
GROUP BY Verein
HAVING SUM(Tore) > SUM(Vorlagen)
ORDER BY Tore_Gesamt DESC
```

**Erklärung:** `HAVING SUM(Tore) > SUM(Vorlagen)` vergleicht die aggregierten Werte pro Gruppe. Das ist ein gutes Beispiel für HAVING mit einem Vergleich zwischen zwei Aggregaten.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐ Herausforderung 2: Positionen mit hohem Durchschnittsalter

        Finde Positionen mit einem Durchschnittsalter über 28.

        (Hinweis: Verwenden Sie HAVING)
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- ⭐⭐ Positionen mit Ø Alter > 28
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Position, AVG("Alter") AS Durchschnittsalter
FROM spieler
GROUP BY Position
HAVING AVG("Alter") > 28
ORDER BY Durchschnittsalter DESC
```

**Erklärung:** `HAVING` filtert Gruppen nach der Aggregation. `WHERE` könnte einzelne Spieler filtern (z.B. `WHERE Alter > 28`), aber wir wollen den **Durchschnitt** der Gruppe prüfen — das geht nur mit `HAVING`.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐⭐ Herausforderung 3: Vereinsstatistiken

        Berechne für jeden Verein: Anzahl Spieler, Durchschnittsalter, Summe Tore, Durchschnitt Tore — aber nur Vereine mit mindestens 2 Spielern.
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- ⭐⭐⭐ Vereinsstatistiken (mind. 2 Spieler)
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Verein,
    COUNT(*) AS Anzahl_Spieler,
    ROUND(AVG("Alter"), 1) AS Durchschnittsalter,
    SUM(Tore) AS Tore_Gesamt,
    ROUND(AVG(Tore), 1) AS Tore_Durchschnitt
FROM spieler
GROUP BY Verein
HAVING COUNT(*) >= 2
ORDER BY Tore_Gesamt DESC
```

**Erklärung:** Hier kombinieren wir alles: `GROUP BY` für die Gruppierung, mehrere Aggregatfunktionen im `SELECT`, `HAVING` um kleine Vereine auszufiltern, und `ORDER BY` für die Sortierung. `ROUND(..., 1)` rundet auf eine Nachkommastelle.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | Syntax | Beispiel |
        |---------|--------|----------|
        | Zählen | `COUNT(*)` | `SELECT COUNT(*) FROM tabelle` |
        | Summe | `SUM(spalte)` | `SUM(Tore)` |
        | Durchschnitt | `AVG(spalte)` | `AVG(Punkte)` |
        | Minimum/Maximum | `MIN/MAX(spalte)` | `MIN(Alter), MAX(Alter)` |
        | Gruppieren | `GROUP BY spalte` | `GROUP BY Position` |
        | Gruppen filtern | `HAVING bedingung` | `HAVING COUNT(*) > 5` |

        **Goldene Regel:** Im SELECT nur GROUP BY-Spalten oder Aggregatfunktionen!

        **Nächste Session:** Strukturierte Datenanalyseprozesse (CRISP-DM, Fallstudie)
        """
    )
    return


if __name__ == "__main__":
    app.run()
