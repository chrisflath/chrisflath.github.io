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
    app_title="DMA Session 2: SQL für Datenexploration — Übungen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 2: SQL für Datenexploration — Übungen

        Theorie und geführte Beispiele → **02-sql-exploration-guide.py**

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
    import polars as pl

    try:
        csv_path = mo.notebook_location() / "public" / "bundesliga.csv"
        bundesliga = pl.read_csv(str(csv_path))
        daten_quelle = "Beispieldaten Bundesliga Saison 2024/25"
    except Exception:
        bundesliga = pl.DataFrame({
            "Mannschaft": ["Bayern München", "Bayer Leverkusen", "VfB Stuttgart", "Borussia Dortmund", "RB Leipzig"],
            "Spiele": [34, 34, 34, 34, 34],
            "Siege": [23, 21, 17, 16, 15],
            "Unentschieden": [5, 7, 6, 7, 8],
            "Niederlagen": [6, 6, 11, 11, 11],
            "Tore": [82, 68, 58, 62, 55],
            "Gegentore": [32, 29, 44, 42, 38],
            "Tordifferenz": [50, 39, 14, 20, 17],
            "Punkte": [74, 70, 57, 55, 53],
        })
        daten_quelle = "Offline-Daten (Fallback)"
        mo.callout(mo.md("**Hinweis:** CSV konnte nicht geladen werden. Es werden Beispieldaten verwendet."), kind="warn")

    return bundesliga, daten_quelle, pl


@app.cell(hide_code=True)
def _(mo, pl):
    try:
        spieler_path = mo.notebook_location() / "public" / "spieler.csv"
        spieler = pl.read_csv(str(spieler_path))

        spieltage_path = mo.notebook_location() / "public" / "bundesliga_spieltage.csv"
        bundesliga_spieltage = pl.read_csv(str(spieltage_path))
    except Exception:
        spieler = pl.DataFrame({
            "Name": ["Müller", "Neuer", "Kimmich", "Wirtz", "Musiala"],
            "Vorname": ["Thomas", "Manuel", "Joshua", "Florian", "Jamal"],
            "Position": ["Sturm", "Tor", "Mittelfeld", "Mittelfeld", "Mittelfeld"],
            "Verein": ["Bayern München", "Bayern München", "Bayern München", "Bayer Leverkusen", None],
            "Tore": [8, 0, 3, 11, None],
            "Vorlagen": [4, 0, 8, 9, 7],
            "Alter": [35, 38, 29, 21, 21],
            "Länderspiele": [131, 118, 91, 28, 35],
            "Spitzname": [None, None, None, None, "Bambi"],
        })
        bundesliga_spieltage = pl.DataFrame({
            "Mannschaft": ["Bayern München"] * 5,
            "Spieltag": [1, 2, 3, 4, 5],
            "Punkte_Kumuliert": [3, 6, 9, 10, 13],
        })
        mo.callout(mo.md("**Hinweis:** CSVs konnten nicht geladen werden. Es werden Beispieldaten verwendet."), kind="warn")

    return bundesliga_spieltage, spieler


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle Bundesliga:** {daten_quelle}

        **Datensätze:**
        - `bundesliga` – Finale Tabelle (18 Teams, 1 Zeitpunkt)
        - `bundesliga_spieltage` – Verlauf (18 Teams × 34 Spieltage)
        - `spieler` – Spielerdaten (mit NULL-Werten)

        ---

        ## Phase 2: Daten sortieren mit ORDER BY
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 2.1: Geführtes Beispiel — Top 5 sortieren

        Führen Sie die Abfrage aus. Welches Team steht an der Spitze?
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
        ### 🟡 Aufgabe 2.2: Mehrere Sortierkriterien (scaffolded)

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
        ORDER BY Punkte DESC, ???
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Mannschaft, Punkte, Tordifferenz
FROM bundesliga
ORDER BY Punkte DESC, Tordifferenz DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.3: Selbstständig - Abstiegskandidaten

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
        -- Ihre Lösung hier
        -- Tipp: ORDER BY ... ASC für aufsteigende Sortierung, LIMIT für Begrenzung
        -- Erwartete Spalten: Mannschaft, Punkte
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Mannschaft, Punkte
FROM bundesliga
ORDER BY Punkte ASC
LIMIT 3
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.4: Selbstständig - Plätze 6-10

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
        -- Ihre Lösung hier
        -- Tipp: LIMIT und OFFSET kombinieren — OFFSET überspringt die ersten N Zeilen
        -- Erwartete Spalten: Mannschaft, Punkte
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Mannschaft, Punkte
FROM bundesliga
ORDER BY Punkte DESC
LIMIT 5 OFFSET 5
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 2.5: Debugging - Reihenfolge

        Diese Abfrage hat einen Fehler. **Führen Sie sie aus** und beheben Sie ihn:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Diese Abfrage enthält einen Fehler — finden und beheben Sie ihn!
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        ORDER BY Punkte DESC
        FROM bundesliga
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** Falsche Reihenfolge der Klauseln! `FROM` muss vor `ORDER BY` stehen.

Die richtige Reihenfolge: `SELECT → FROM → WHERE → ORDER BY → LIMIT`

```sql
-- Korrektur:
SELECT Mannschaft, Punkte
FROM bundesliga
ORDER BY Punkte DESC
LIMIT 5
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 2.6: Debugging - ASC vs DESC

        Diese Abfrage soll die Top-Torjäger zeigen (meiste Tore zuerst).
        **Führen Sie sie aus** — zeigt sie wirklich die Top-Teams?
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Diese Abfrage soll die MEISTEN Tore zuerst zeigen — stimmt das?
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Tore
        FROM bundesliga
        ORDER BY Tore
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** Ohne explizite Angabe sortiert `ORDER BY` **aufsteigend** (ASC). Die wenigsten Tore kommen zuerst!

Für "meiste Tore zuerst" brauchen wir `DESC`:

```sql
-- Korrektur:
SELECT Mannschaft, Tore
FROM bundesliga
ORDER BY Tore DESC
LIMIT 5
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Quiz: ORDER BY
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_order = mo.ui.radio(
        options={
            "Aufsteigend (kleinster Wert zuerst)": "a",
            "Absteigend (größter Wert zuerst)": "b",
            "Alphabetisch": "c",
            "Zufällig": "d",
        },
        label="Wie sortiert `ORDER BY Punkte` **ohne** ASC/DESC?",
    )
    return (quiz_order,)


@app.cell(hide_code=True)
def _(mo, quiz_order):
    if quiz_order.value == "a":
        mo.callout(mo.md("**Richtig!** Ohne explizite Angabe sortiert `ORDER BY` aufsteigend (ASC). Für absteigend muss `DESC` angegeben werden."), kind="success")
    elif quiz_order.value is not None:
        mo.callout(mo.md("**Nicht ganz.** Standard ist aufsteigend (`ASC`). Merke: Man muss nur `DESC` explizit angeben — ASC ist der Default."), kind="warn")
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([quiz_order, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: DISTINCT und LIKE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 4.1: Geführtes Beispiel — Eindeutige Positionen

        Führen Sie die Abfrage aus. Wie viele verschiedene Positionen gibt es?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT DISTINCT Position
        FROM spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 4.2: Kombinationen finden (scaffolded)

        Finden Sie alle eindeutigen Kombinationen von Position und Verein.
        Ergänzen Sie die zweite Spalte:
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ergänzen Sie die zweite Spalte
    _df = mo.sql(
        f"""
        SELECT DISTINCT Position, ???
        FROM spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT DISTINCT Position, Verein
FROM spieler
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.3: Selbstständig - LIKE mit Endung

        Finden Sie alle Spieler, deren Nachname auf 'er' endet:
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: LIKE mit '%' vor dem Suchbegriff für "endet mit"
        -- Erwartete Spalten: Name, Vorname
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Name, Vorname
FROM spieler
WHERE Name LIKE '%er'
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.4: Selbstständig - LIKE mit Enthält

        Finden Sie alle Teams, die "FC" im Namen haben:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: LIKE mit '%' vor UND nach dem Suchbegriff für "enthält"
        -- Erwartete Spalten: Mannschaft
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Mannschaft
FROM bundesliga
WHERE Mannschaft LIKE '%FC%'
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Quiz: DISTINCT und LIKE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_distinct = mo.ui.radio(
        options={
            "Nur Zeilen, bei denen Name genau 'M' ist": "a",
            "Alle Spieler, deren Name mit 'M' beginnt": "b",
            "Alle Spieler, deren Name 'M' enthält": "c",
            "Alle Spieler, deren Name mit 'M' endet": "d",
        },
        label="Was findet `WHERE Name LIKE 'M%'`?",
    )
    return (quiz_distinct,)


@app.cell(hide_code=True)
def _(mo, quiz_distinct):
    if quiz_distinct.value == "b":
        mo.callout(mo.md("**Richtig!** `'M%'` bedeutet: beginnt mit 'M', danach beliebig viele Zeichen. Für 'enthält' bräuchte man `'%M%'`."), kind="success")
    elif quiz_distinct.value is not None:
        mo.callout(mo.md("**Nicht ganz.** `%` steht für 'beliebig viele Zeichen'. `'M%'` = beginnt mit M. `'%M%'` = enthält M. `'%M'` = endet mit M."), kind="warn")
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([quiz_distinct, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Umgang mit NULL-Werten
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 6.1: Geführtes Beispiel — NULL-Werte finden

        Führen Sie die Abfrage aus. Welche Spieler haben keinen Verein?
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
        ### 🟡 Aufgabe 6.2: COALESCE anwenden (scaffolded)

        Berechnen Sie Scorerpunkte (Tore + Vorlagen), aber ersetzen Sie NULL durch 0.
        Ergänze die COALESCE-Aufrufe:
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
            COALESCE(???, 0) + COALESCE(???, 0) AS Scorerpunkte
        FROM spieler
        ORDER BY Scorerpunkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Name,
    COALESCE(Tore, 0) + COALESCE(Vorlagen, 0) AS Scorerpunkte
FROM spieler
ORDER BY Scorerpunkte DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.3: Selbstständig - Spieler ohne Spitznamen

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
        -- Ihre Lösung hier
        -- Tipp: IS NULL prüft auf fehlende Werte
        -- Erwartete Spalten: Name, Vorname, Spitzname
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Name, Vorname, Spitzname
FROM spieler
WHERE Spitzname IS NULL
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.4: Selbstständig - Spieler mit vollständigen Daten

        Finden Sie alle Spieler, bei denen sowohl Tore ALS AUCH Vorlagen eingetragen sind (nicht NULL).
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: IS NOT NULL mit AND kombinieren
        -- Erwartete Spalten: Name, Tore, Vorlagen
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Name, Tore, Vorlagen
FROM spieler
WHERE Tore IS NOT NULL
  AND Vorlagen IS NOT NULL
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.5: Debugging - = NULL vs IS NULL

        Diese Abfrage soll Spieler ohne Verein finden.
        **Führen Sie sie aus** — liefert sie Ergebnisse?
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Diese Abfrage enthält einen Fehler — finden und beheben Sie ihn!
    _df = mo.sql(
        f"""
        SELECT Name, Verein
        FROM spieler
        WHERE Verein = NULL
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** `= NULL` funktioniert nicht in SQL! Der Vergleich `Verein = NULL` ergibt immer NULL (nicht TRUE), daher werden keine Zeilen gefunden.

NULL ist "unbekannt" — man kann es nicht mit `=` vergleichen. Verwenden Sie stattdessen `IS NULL`:

```sql
-- Korrektur:
SELECT Name, Verein
FROM spieler
WHERE Verein IS NULL
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.6: Selbstständig - Top-Torjäger mit COALESCE

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
        -- Ihre Lösung hier
        -- Tipp: COALESCE(Tore, 0) + COALESCE(Vorlagen, 0) AS Scorerpunkte
        -- Dann ORDER BY Scorerpunkte DESC und LIMIT 5
        -- Erwartete Spalten: Name, Tore, Vorlagen, Scorerpunkte
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Name,
    Tore,
    Vorlagen,
    COALESCE(Tore, 0) + COALESCE(Vorlagen, 0) AS Scorerpunkte
FROM spieler
ORDER BY Scorerpunkte DESC
LIMIT 5
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.7: Kombination aller Konzepte

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
        -- Ihre Lösung hier
        -- Tipp: WHERE für Position + COALESCE für NULL-Behandlung + WHERE für Minimum
        -- Erwartete Spalten: Name, Position, Scorerpunkte
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Name,
    Position,
    COALESCE(Tore, 0) + COALESCE(Vorlagen, 0) AS Scorerpunkte
FROM spieler
WHERE Position = 'Mittelfeld'
  AND COALESCE(Tore, 0) + COALESCE(Vorlagen, 0) >= 5
ORDER BY Scorerpunkte DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Quiz: NULL-Werte
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_null = mo.ui.radio(
        options={
            "Alle Zeilen, bei denen Verein NULL ist": "a",
            "Keine Zeilen — der Vergleich ergibt immer NULL (UNKNOWN)": "b",
            "Alle Zeilen — NULL ist gleich NULL": "c",
            "Eine Fehlermeldung": "d",
        },
        label="Was liefert `WHERE Verein = NULL`?",
    )
    return (quiz_null,)


@app.cell(hide_code=True)
def _(mo, quiz_null):
    if quiz_null.value == "b":
        mo.callout(mo.md("**Richtig!** `= NULL` ergibt immer UNKNOWN (nicht TRUE), daher werden keine Zeilen gefunden. Man muss `IS NULL` verwenden."), kind="success")
    elif quiz_null.value is not None:
        mo.callout(mo.md("**Nicht ganz.** NULL ist 'unbekannt' — jeder Vergleich mit `=` ergibt UNKNOWN. Verwenden Sie stattdessen `IS NULL`."), kind="warn")
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([quiz_null, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 7: Visualisierung
        """
    )
    return


@app.cell
def _():
    import plotly.express as px
    return (px,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 7.1: Siege vs. Niederlagen

        Erstellen Sie ein Streudiagramm, das Siege (x-Achse) gegen Niederlagen (y-Achse) zeigt.
        Fügen Sie den Teamnamen als hover_name hinzu.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre SQL-Abfrage hier:
    mo.sql(
        f"""
        SELECT Mannschaft, Siege, Niederlagen
        FROM bundesliga
        """
    )


@app.cell
def _(bundesliga, mo, px):
    # Ihre Visualisierung:
    siege_niederlagen = mo.sql(
        f"""
        SELECT Mannschaft, Siege, Niederlagen
        FROM bundesliga
        """
    )

    fig4 = px.scatter(
        siege_niederlagen,
        x="Siege",
        y="Niederlagen",
        hover_name="Mannschaft",
        title="Siege vs. Niederlagen"
    )
    fig4


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration — Herausforderungen

        **Tipp:** Vergleichen Sie Ihre Lösungen mit Ihrem Nachbarn — es gibt oft mehrere Wege zum gleichen Ergebnis!

        ### ⭐ Herausforderung 1: Paginierung

        Zeige Spieler sortiert nach Toren (absteigend), aber nur die Plätze 4-6 (mit OFFSET).
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- ⭐ Plätze 4-6 nach Toren
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Name, Vorname, Tore
FROM spieler
WHERE Tore IS NOT NULL
ORDER BY Tore DESC
LIMIT 3 OFFSET 3
```

**Erklärung:** `OFFSET 3` überspringt die ersten 3 Ergebnisse (Plätze 1-3), `LIMIT 3` zeigt dann die nächsten 3 (Plätze 4-6). Wir filtern `IS NOT NULL` um sinnvoll zu sortieren.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐ Herausforderung 2: NULL und Vokale

        Finde alle Spieler deren Verein NULL ist UND deren Name mit einem Vokal beginnt.

        (Hinweis: Mehrere `LIKE`-Bedingungen mit `OR` kombinieren)
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- ⭐⭐ Kein Verein + Name beginnt mit Vokal
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Name, Vorname, Verein
FROM spieler
WHERE Verein IS NULL
  AND (Name LIKE 'A%' OR Name LIKE 'E%' OR Name LIKE 'I%'
       OR Name LIKE 'O%' OR Name LIKE 'U%')
```

**Erklärung:** Die Klammern um die `OR`-Bedingungen sind wichtig, damit `AND` korrekt mit allen Vokal-Prüfungen verknüpft wird. Alternativ in DuckDB: `WHERE Verein IS NULL AND Name SIMILAR TO '[AEIOU]%'`
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐⭐ Herausforderung 3: Bereinigte Ansicht

        Erstelle eine "bereinigte" Ansicht: Alle Spieler mit `COALESCE(Tore, 0)` und `COALESCE(Verein, 'Vereinslos')`, sortiert nach bereinigten Toren DESC.
        """
    )
    return


@app.cell
def _(mo, spieler):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- ⭐⭐⭐ Bereinigte Spieler-Ansicht
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Name,
    Vorname,
    Position,
    COALESCE(Verein, 'Vereinslos') AS Verein,
    COALESCE(Tore, 0) AS Tore,
    COALESCE(Vorlagen, 0) AS Vorlagen,
    COALESCE(Tore, 0) + COALESCE(Vorlagen, 0) AS Scorerpunkte
FROM spieler
ORDER BY Tore DESC
```

**Erklärung:** `COALESCE` ersetzt NULL durch den angegebenen Wert. Hier machen wir die Tabelle "sauber" — kein NULL mehr sichtbar. Besonders nützlich für Berichte und Visualisierungen!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        ### SQL-Konzepte
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

        ### Visualisierung mit Plotly
        | Chart-Typ | Funktion | Verwendung |
        |-----------|----------|------------|
        | Balkendiagramm | `px.bar()` | Werte vergleichen |
        | Streudiagramm | `px.scatter()` | Zusammenhänge zeigen |
        | Farbe als Dimension | `color=` | Dritte Variable kodieren |

        **Nächste Session:** Aggregation & Gruppierung (COUNT, SUM, AVG, GROUP BY)
        """
    )
    return


if __name__ == "__main__":
    app.run()
