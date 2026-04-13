# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "polars",
#     "plotly",
# ]
# ///

import marimo

__generated_with = "0.19.7"
app = marimo.App(
    width="medium",
    app_title="DMA Session 1: SQL-Grundlagen — Übungen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Session 1: SQL-Grundlagen — Übungen

    Theorie und geführte Beispiele → **01-sql-grundlagen-guide.py**

    **Aufgabentypen:**
    - 🟡 **Scaffolded**: Teillösung zum Ergänzen
    - 🔵 **Selbstständig**: Eigene Lösung schreiben
    - 🔴 **Debugging**: Fehler finden und beheben
    - ⭐ **Exploration**: Offene Herausforderungen

    > **Hinweis:** 🟡-Aufgaben enthalten `???` als Platzhalter. Die Zelle zeigt einen SQL-Fehler, bis Sie die `???` durch die richtige Lösung ersetzen — das ist Absicht!

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    import polars as pl
    import re

    _BULIBOX_URL = "http://www.bulibox.de/abschlusstabellen/1-Bundesliga.html"
    _CORS_PROXY = "https://api.allorigins.win/get?url="

    def _fetch_html(url):
        """Fetch HTML — lokal via urllib, im Browser via pyodide + CORS-Proxy."""
        try:
            from urllib.request import urlopen
            return urlopen(url, timeout=5).read().decode("utf-8")
        except Exception:
            pass
        # WASM/Pyodide: nutze CORS-Proxy + pyodide.http
        import json
        from pyodide.http import open_url  # type: ignore[import-not-found]
        proxy_url = _CORS_PROXY + url
        response = json.loads(open_url(proxy_url).read())
        return response["contents"]

    def _parse_tabelle(html):
        """Parse bulibox.de HTML-Tabelle in ein Polars DataFrame."""
        tables = re.findall(
            r"<table[^>]*class='abschluss'[^>]*>(.*?)</table>", html, re.DOTALL
        )
        table_html = tables[-1] if tables else tables[0]
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, re.DOTALL)

        teams = []
        for row in rows[1:]:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
            if len(cells) < 6:
                continue
            mannschaft = re.sub(r"<[^>]+>|&nbsp;", "", cells[1]).strip()
            spiele = int(re.sub(r"\D", "", cells[2]))
            sun = re.sub(r"&nbsp;", "", cells[3]).strip()
            s, u, n = [int(x) for x in sun.split("-")]
            tore_raw = re.sub(r"&nbsp;", "", cells[4]).strip()
            m = re.match(r"(\d+):(\d+)\s*\(([+-]?\d+)\)", tore_raw)
            teams.append({
                "Mannschaft": mannschaft, "Spiele": spiele,
                "Siege": s, "Unentschieden": u, "Niederlagen": n,
                "Tore": int(m.group(1)), "Gegentore": int(m.group(2)),
                "Tordifferenz": int(m.group(3)), "Punkte": int(re.sub(r"\D", "", cells[5])),
            })
        return pl.DataFrame(teams)

    try:
        html = _fetch_html(_BULIBOX_URL)
        bundesliga = _parse_tabelle(html)
        daten_quelle = "Live-Daten von bulibox.de (Saison 2025/26)"
    except Exception:
        bundesliga = pl.DataFrame({
            "Mannschaft": ["Bayern München", "Bayer Leverkusen", "VfB Stuttgart",
                           "Borussia Dortmund", "RB Leipzig", "Eintracht Frankfurt",
                           "SC Freiburg", "1. FSV Mainz 05", "FC Augsburg",
                           "Werder Bremen", "VfL Wolfsburg", "Borussia Mönchengladbach",
                           "1. FC Union Berlin", "1. FC Köln", "Hamburger SV",
                           "TSG 1899 Hoffenheim", "FC St. Pauli", "1. FC Heidenheim"],
            "Spiele": [29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29],
            "Siege": [24, 15, 17, 19, 17, 12, 11, 12, 10, 7, 6, 8, 6, 8, 7, 10, 5, 4],
            "Unentschieden": [4, 7, 5, 7, 5, 7, 5, 6, 6, 7, 7, 5, 7, 4, 7, 5, 6, 5],
            "Niederlagen": [1, 7, 7, 3, 7, 10, 13, 11, 13, 15, 16, 16, 16, 17, 15, 14, 18, 20],
            "Tore": [105, 59, 60, 60, 56, 50, 34, 38, 33, 30, 30, 27, 23, 35, 30, 46, 22, 30],
            "Gegentore": [27, 39, 38, 29, 36, 42, 40, 37, 43, 43, 54, 46, 49, 50, 44, 51, 50, 62],
            "Tordifferenz": [78, 20, 22, 31, 20, 8, -6, 1, -10, -13, -24, -19, -26, -15, -14, -5, -28, -32],
            "Punkte": [76, 52, 56, 64, 56, 43, 38, 42, 36, 28, 25, 29, 25, 28, 28, 35, 21, 17],
        })
        daten_quelle = "Offline-Daten (Stand: Spieltag 29, Saison 2025/26)"
        mo.callout(
            mo.md("**Hinweis:** Live-Daten konnten nicht geladen werden. Es werden Offline-Daten verwendet."),
            kind="warn",
        )
    return bundesliga, daten_quelle


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(f"""
    **Datenquelle:** {daten_quelle}

    **Verfügbare Spalten:** Mannschaft, Spiele, Siege, Unentschieden, Niederlagen, Tore, Gegentore, Tordifferenz, Punkte

    ---

    ## Phase 2: Erste SELECT-Abfragen
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Aufgabe 2.1: Geführtes Beispiel — Alle Daten anzeigen

    Führen Sie die folgende Abfrage aus und schauen Sie sich das Ergebnis an:
    """)
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT
            *
        FROM
            bundesliga
        LIMIT
            5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🟡 Aufgabe 2.2: Drei Spalten auswählen (scaffolded)

    Ergänzen Sie den folgenden Befehl, um Mannschaft, Siege und Niederlagen anzuzeigen:
    """)
    return


@app.cell
def _(bundesliga, mo):
    # Ergänzen Sie die fehlende Spalte
    _df = mo.sql(
        f"""
        SELECT Siege
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
    ```sql
    SELECT Mannschaft, Siege, Niederlagen
    FROM bundesliga
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔵 Aufgabe 2.3: Selbstständig - Torstatistik

    Schreiben Sie eine Abfrage, die zeigt:
    - Mannschaft
    - Tore
    - Gegentore
    """)
    return


@app.cell
def _(mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: SELECT mit drei Spalten aus bundesliga
        -- Erwartete Spalten: Mannschaft, Tore, Gegentore
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
    ```sql
    SELECT Mannschaft, Tore, Gegentore
    FROM bundesliga
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔵 Aufgabe 2.4: Selbstständig - Spielstatistik

    Zeigen Sie für jedes Team:
    - Mannschaft
    - Spiele
    - Siege
    - Unentschieden
    - Niederlagen
    """)
    return


@app.cell
def _(mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: SELECT mit fünf Spalten aus bundesliga
        -- Erwartete Spalten: Mannschaft, Spiele, Siege, Unentschieden, Niederlagen
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
    ```sql
    SELECT Mannschaft, Spiele, Siege, Unentschieden, Niederlagen
    FROM bundesliga
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔴 Aufgabe 2.5: Debugging - Finden Sie den Fehler!

    Diese Abfrage hat einen Syntaxfehler. **Führen Sie sie aus** und beheben Sie ihn:
    """)
    return


@app.cell
def _(bundesliga, mo):
    # Diese Abfrage enthält einen Fehler — finden und beheben Sie ihn!
    _df = mo.sql(
        f"""
        SELECT Mannschaft Punkte
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
    **Fehler:** Fehlendes Komma zwischen den Spaltennamen.

    Ohne Komma interpretiert SQL `Punkte` als Alias für `Mannschaft`.

    ```sql
    -- Korrektur:
    SELECT Mannschaft, Punkte
    FROM bundesliga
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔴 Aufgabe 2.6: Debugging - Spaltenname

    Diese Abfrage hat einen Fehler. **Führen Sie sie aus** — was stimmt nicht?
    """)
    return


@app.cell
def _(bundesliga, mo):
    # Diese Abfrage enthält einen Fehler — finden und beheben Sie ihn!
    _df = mo.sql(
        f"""
        SELECT Manschaft, Punkte
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
    **Fehler:** Tippfehler im Spaltennamen — `Manschaft` statt `Mannschaft` (doppeltes n).

    SQL-Spaltennamen müssen exakt stimmen!

    ```sql
    -- Korrektur:
    SELECT Mannschaft, Punkte
    FROM bundesliga
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quiz: SELECT-Grundlagen

    Testen Sie Ihr Verständnis der bisherigen Konzepte:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_select = mo.ui.radio(
        options={
            "a": "Alle Spalten der Tabelle bundesliga",
            "b": "Nur die Spalte Mannschaft für alle Teams",
            "c": "Nur Teams, die 'Mannschaft' heißen",
            "d": "Eine Fehlermeldung",
        },
        label="Was liefert `SELECT Mannschaft FROM bundesliga`?",
    )
    quiz_select
    return (quiz_select,)


@app.cell(hide_code=True)
def _(mo, quiz_select):
    if quiz_select.value == "b":
        mo.callout(mo.md("**Richtig!** `SELECT Mannschaft` wählt genau eine Spalte aus — für alle Zeilen der Tabelle."), kind="success")
    elif quiz_select.value is not None:
        mo.callout(mo.md("**Nicht ganz.** `SELECT spalte` wählt eine bestimmte Spalte aus. `*` wäre nötig für alle Spalten."), kind="warn")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Phase 4: Filtern mit WHERE
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Aufgabe 4.1: Geführtes Beispiel — Teams mit vielen Punkten

    Führen Sie die folgende Abfrage aus. Wie viele Teams haben mehr als 50 Punkte?
    """)
    return


@app.cell
def _(bundesliga, mo):
    mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Punkte > 50
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔵 Aufgabe 4.2: Selbstständig - Wenig Niederlagen

    Finden Sie alle Teams mit weniger als 5 Niederlagen.
    Zeigen Sie Mannschaft und Niederlagen.
    """)
    return


@app.cell
def _(mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: WHERE mit Vergleichsoperator < auf Niederlagen
        -- Erwartete Spalten: Mannschaft, Niederlagen
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
    ```sql
    SELECT Mannschaft, Niederlagen
    FROM bundesliga
    WHERE Niederlagen < 5
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔵 Aufgabe 4.3: Selbstständig - Tore

    Finden Sie alle Teams, die mehr als 35 Tore geschossen haben.
    """)
    return


@app.cell
def _(mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: WHERE mit Vergleichsoperator > auf Tore
        -- Erwartete Spalten: Mannschaft, Tore
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
    ```sql
    SELECT Mannschaft, Tore
    FROM bundesliga
    WHERE Tore > 35
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔴 Aufgabe 4.4: Debugging - Textvergleich

    Diese Abfrage soll Bayern München finden. **Führen Sie sie aus** — was fehlt?
    """)
    return


@app.cell
def _(mo):
    # Diese Abfrage enthält einen Fehler — finden und beheben Sie ihn!
    _df = mo.sql(
        f"""
        SELECT *
        FROM bundesliga
        WHERE Mannschaft = Bayern München
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
    **Fehler:** Text muss in einfache Anführungszeichen gesetzt werden.

    Ohne Anführungszeichen denkt SQL, `Bayern` und `München` seien Spaltennamen.

    ```sql
    -- Korrektur:
    SELECT *
    FROM bundesliga
    WHERE Mannschaft = 'Bayern München'
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔴 Aufgabe 4.5: Debugging - Operator

    Diese Abfrage soll Teams mit **mindestens 25 Punkten** finden.
    **Führen Sie sie aus** — liefert sie das richtige Ergebnis?
    """)
    return


@app.cell
def _(bundesliga, mo):
    # Prüfen Sie: Findet diese Abfrage wirklich "mindestens 25"?
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Punkte > 25
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
    **Fehler:** `>` bedeutet "größer als", nicht "mindestens". Ein Team mit genau 25 Punkten wird nicht gefunden!

    "Mindestens" bedeutet "größer oder gleich" → `>=`

    ```sql
    -- Korrektur:
    SELECT Mannschaft, Punkte
    FROM bundesliga
    WHERE Punkte >= 25
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quiz: WHERE-Klausel
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_where = mo.ui.radio(
        options={
            "a": "`WHERE Siege > 10 OR Niederlagen < 5`",
            "b": "`WHERE Siege > 10 AND Niederlagen < 5`",
            "c": "`WHERE Siege >= 10 AND Niederlagen <= 5`",
            "d": "`WHERE Siege >= 10 OR Niederlagen <= 5`",
        },
        label="Welche Abfrage findet Teams mit **mindestens 10 Siegen** UND **höchstens 5 Niederlagen**?",
    )
    quiz_where
    return (quiz_where,)


@app.cell(hide_code=True)
def _(mo, quiz_where):
    if quiz_where.value == "c":
        mo.callout(mo.md("**Richtig!** 'Mindestens' = `>=`, 'höchstens' = `<=`, und beide Bedingungen müssen gelten = `AND`."), kind="success")
    elif quiz_where.value is not None:
        mo.callout(mo.md("**Nicht ganz.** Achten Sie auf: 'mindestens 10' bedeutet `>= 10` (nicht `> 10`), und 'UND' erfordert `AND` (nicht `OR`)."), kind="warn")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Phase 6: Komplexe Abfragen mit AND, OR, NOT
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Aufgabe 6.1: Geführtes Beispiel — AND-Verknüpfung

    Führen Sie die Abfrage aus. Welche Teams erfüllen beide Bedingungen gleichzeitig?
    """)
    return


@app.cell
def _(bundesliga, mo):
    mo.sql(
        f"""
        SELECT Mannschaft, Siege, Niederlagen
        FROM bundesliga
        WHERE Siege > 15 AND Niederlagen < 10
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔵 Aufgabe 6.2: Selbstständig - Kombinierte Bedingung

    Finden Sie Teams, die:
    - Mehr als 30 Tore geschossen haben UND
    - Weniger als 25 Tore kassiert haben

    Zeigen Sie Mannschaft, Tore, Gegentore.
    """)
    return


@app.cell
def _(mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: Verwenden Sie AND um zwei WHERE-Bedingungen zu kombinieren
        -- Erwartete Spalten: Mannschaft, Tore, Gegentore
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
    ```sql
    SELECT Mannschaft, Tore, Gegentore
    FROM bundesliga
    WHERE Tore > 30 AND Gegentore < 25
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔵 Aufgabe 6.3: Selbstständig - Abstiegskandidaten

    Finden Sie potenzielle Abstiegskandidaten:
    - Weniger als 20 Punkte ODER
    - Mehr als 10 Niederlagen

    Zeigen Sie Mannschaft, Punkte, Niederlagen.
    """)
    return


@app.cell
def _(mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: Verwenden Sie OR für "mindestens eine Bedingung"
        -- Erwartete Spalten: Mannschaft, Punkte, Niederlagen
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
    ```sql
    SELECT Mannschaft, Punkte, Niederlagen
    FROM bundesliga
    WHERE Punkte < 20 OR Niederlagen > 10
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔵 Aufgabe 6.4: Selbstständig - LIKE

    Finden Sie alle Teams mit "Borussia" im Namen.

    (Hinweis: Verwenden Sie `%` vor und nach dem Suchbegriff)
    """)
    return


@app.cell
def _(mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: LIKE mit % vor und nach dem Suchbegriff
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
    WHERE Mannschaft LIKE '%Borussia%'
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔴 Aufgabe 6.5: Debugging - Klammern

    Diese Abfrage soll Teams finden, die ENTWEDER viele Punkte (>35) ODER viele Tore (>40) haben, UND dabei weniger als 5 Niederlagen haben.

    **Führen Sie sie aus** — die Abfrage ist syntaktisch korrekt, liefert aber falsche Ergebnisse. Warum?
    """)
    return


@app.cell
def _(bundesliga, mo):
    # Diese Abfrage liefert falsche Ergebnisse — finden Sie den logischen Fehler!
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte, Tore, Niederlagen
        FROM bundesliga
        WHERE Punkte > 35 OR Tore > 40 AND Niederlagen < 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
    **Fehler:** AND bindet stärker als OR! Die Abfrage wird gelesen als:

    ```sql
    WHERE Punkte > 35 OR (Tore > 40 AND Niederlagen < 5)
    ```

    Das bedeutet: ALLE Teams mit >35 Punkten werden angezeigt, unabhängig von Niederlagen.

    **Korrektur mit Klammern:**

    ```sql
    SELECT Mannschaft, Punkte, Tore, Niederlagen
    FROM bundesliga
    WHERE (Punkte > 35 OR Tore > 40) AND Niederlagen < 5
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔴 Aufgabe 6.6: Debugging - LIKE

    Diese Abfrage soll alle Teams finden, die "FC" im Namen haben.
    **Führen Sie sie aus** — findet sie alle FC-Teams?
    """)
    return


@app.cell
def _(bundesliga, mo):
    # Diese Abfrage findet nicht alle Teams mit FC — warum?
    _df = mo.sql(
        f"""
        SELECT Mannschaft
        FROM bundesliga
        WHERE Mannschaft LIKE 'FC%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
    **Fehler:** `'FC%'` findet nur Teams, die mit "FC" **beginnen** (z.B. "FC Augsburg").

    Aber "1. FC Union Berlin" oder "1. FC Heidenheim" haben "FC" **mitten im Namen**.

    ```sql
    -- Korrektur: % auch vor FC setzen
    SELECT Mannschaft
    FROM bundesliga
    WHERE Mannschaft LIKE '%FC%'
    ```
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quiz: Logische Operatoren
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_logic = mo.ui.radio(
        options={
            "a": "AND — weil beide einschränkend wirken",
            "b": "OR — weil nur eine Bedingung erfüllt sein muss",
            "c": "Beide liefern gleich viele Ergebnisse",
            "d": "Kommt auf die Daten an, man kann es nicht allgemein sagen",
        },
        label="Welcher Operator liefert in der Regel **mehr** Ergebnisse: `WHERE A AND B` oder `WHERE A OR B`?",
    )
    quiz_logic
    return (quiz_logic,)


@app.cell(hide_code=True)
def _(mo, quiz_logic):
    if quiz_logic.value == "b":
        mo.callout(mo.md("**Richtig!** `OR` ist *permissiv* — es reicht, wenn eine Bedingung zutrifft. `AND` ist *restriktiv* — beide müssen gelten."), kind="success")
    elif quiz_logic.value is not None:
        mo.callout(mo.md("**Nicht ganz.** Merkregel: `AND` = restriktiv (weniger Ergebnisse), `OR` = permissiv (mehr Ergebnisse)."), kind="warn")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Phase 7: Visualisierung
    """)
    return


@app.cell
def _():
    import plotly.express as px
    return (px,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔵 Aufgabe 7.1: Eigene Visualisierung

    Erstellen Sie ein Diagramm Ihrer Wahl:
    - Balkendiagramm: Welche Teams kassieren die meisten Gegentore?
    - Liniendiagramm: Wie entwickelte sich Dortmund über die Saison?
    """)
    return


@app.cell
def _(bundesliga, mo):
    # Ihre SQL-Abfrage hier:
    mo.sql(
        f"""
        SELECT Mannschaft, Gegentore
        FROM bundesliga
        ORDER BY Gegentore DESC
        """
    )
    return


@app.cell
def _(bundesliga, mo, px):
    # Ihre Visualisierung:
    meine_daten = mo.sql(
        f"""
        SELECT Mannschaft, Gegentore
        FROM bundesliga
        ORDER BY Gegentore DESC
        """
    )

    fig_own = px.bar(meine_daten, x="Mannschaft", y="Gegentore",
                     title="Gegentore pro Team")
    fig_own
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Freie Exploration — Herausforderungen

    **Tipp:** Vergleichen Sie Ihre Lösungen mit Ihrem Nachbarn — es gibt oft mehrere Wege zum gleichen Ergebnis!

    ### ⭐ Herausforderung 1: Siegreiche Teams

    Welche Teams haben mehr Siege als Unentschieden und Niederlagen **zusammen**?
    """)
    return


@app.cell
def _(mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- ⭐ Siege > Unentschieden + Niederlagen
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
    ```sql
    SELECT Mannschaft, Siege, Unentschieden, Niederlagen
    FROM bundesliga
    WHERE Siege > Unentschieden + Niederlagen
    ```

    **Erklärung:** In SQL kann man Spalten in WHERE direkt verrechnen. Die rechte Seite `Unentschieden + Niederlagen` wird pro Zeile berechnet.
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ⭐⭐ Herausforderung 2: Punkte pro Spiel

    Erstelle ein Ranking: Punkte pro Spiel (`Punkte / Spiele`) für jedes Team, absteigend sortiert.

    (Hinweis: SQL kann berechnete Spalten erstellen — `SELECT spalte1, spalte2, ausdruck AS alias`)
    """)
    return


@app.cell
def _(mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- ⭐⭐ Punkte pro Spiel berechnen
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
    ```sql
    SELECT
    Mannschaft,
    Punkte,
    Spiele,
    ROUND(CAST(Punkte AS FLOAT) / Spiele, 2) AS Punkte_pro_Spiel
    FROM bundesliga
    ORDER BY Punkte_pro_Spiel DESC
    ```

    **Erklärung:** `CAST(... AS FLOAT)` sorgt dafür, dass die Division ein Dezimalergebnis liefert (nicht ganzzahlig). `ROUND(..., 2)` rundet auf 2 Nachkommastellen.
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ⭐⭐⭐ Herausforderung 3: Kombination von LIKE, AND, OR

    Finde Teams mit "Borussia" oder "Bayern" im Namen, die eine **positive Tordifferenz** haben.
    """)
    return


@app.cell
def _(mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- ⭐⭐⭐ LIKE + AND + OR kombinieren
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
    ```sql
    SELECT Mannschaft, Tordifferenz
    FROM bundesliga
    WHERE (Mannschaft LIKE '%Borussia%' OR Mannschaft LIKE '%Bayern%')
      AND Tordifferenz > 0
    ```

    **Erklärung:** Die Klammern um die OR-Bedingung sind entscheidend! Ohne Klammern würde AND nur auf die zweite LIKE-Bedingung wirken (Operatorvorrang). Außerdem braucht jeder LIKE-Vergleich ein eigenes `Mannschaft LIKE ...`.
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Zusammenfassung

    | Konzept | Syntax | Beispiel |
    |---------|--------|----------|
    | Alle Spalten | `SELECT *` | `SELECT * FROM tabelle` |
    | Bestimmte Spalten | `SELECT spalte1, spalte2` | `SELECT Mannschaft, Punkte` |
    | Filtern | `WHERE bedingung` | `WHERE Punkte > 30` |
    | Und-Verknüpfung | `AND` | `WHERE Siege > 10 AND Niederlagen < 5` |
    | Oder-Verknüpfung | `OR` | `WHERE Punkte > 30 OR Tordifferenz > 10` |
    | Negation | `NOT` | `WHERE NOT Mannschaft = 'Bayern'` |
    | Wertebereich | `BETWEEN` | `WHERE Punkte BETWEEN 20 AND 30` |
    | Werteliste | `IN` | `WHERE Mannschaft IN ('A', 'B', 'C')` |
    | Mustersuche | `LIKE` | `WHERE Mannschaft LIKE 'B%'` |

    ### Visualisierung
    | Charttyp | Funktion | Verwendung |
    |----------|----------|------------|
    | Balkendiagramm | `px.bar()` | Querschnitt (Kategorien vergleichen) |
    | Liniendiagramm | `px.line()` | Zeitreihe (Entwicklung zeigen) |

    **Nächste Session:** Sortieren, DISTINCT, NULL-Werte, mehr Visualisierung
    """)
    return


if __name__ == "__main__":
    app.run()
