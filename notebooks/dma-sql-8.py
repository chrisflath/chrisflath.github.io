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
    app_title="DMA Session 8: JOINs — Übungen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 8: JOINs — Übungen

        Theorie und geführte Beispiele → **08-joins-guide.py**

        **Aufgabentypen:**
        - 🟡 **Scaffolded**: Teillösung zum Ergänzen
        - 🔵 **Selbstständig**: Eigene Lösung schreiben
        - 🔴 **Debugging**: Fehler finden und beheben
        - ⭐ **Exploration**: Offene Herausforderungen

        ---
        """
    )
    return


@app.cell
def _():
    import polars as pl
    import plotly.express as px

    # Vereine
    vereine = pl.DataFrame({
        "Verein_ID": [1, 2, 3, 4],
        "Name": ["Bayern München", "Bayer Leverkusen", "BVB Dortmund", "RB Leipzig"],
        "Stadt": ["München", "Leverkusen", "Dortmund", "Leipzig"],
        "Stadion": ["Allianz Arena", "BayArena", "Signal Iduna Park", "Red Bull Arena"]
    })

    # Spieler — manche ohne Verein (NULL), um LEFT JOIN zu demonstrieren
    spieler = pl.DataFrame({
        "Spieler_ID": [1, 2, 3, 4, 5, 6, 7, 8],
        "Name": ["Müller", "Neuer", "Wirtz", "Xhaka", "Hummels", "Sabitzer", "Reus", "Götze"],
        "Position": ["Sturm", "Tor", "Mittelfeld", "Mittelfeld", "Abwehr", "Mittelfeld", "Mittelfeld", "Mittelfeld"],
        "Verein_ID": [1, 1, 2, 2, 3, None, None, None]
    })

    # Spiele — Heim vs. Gast
    spiele = pl.DataFrame({
        "Spiel_ID": [1, 2, 3, 4],
        "Heim_ID": [1, 2, 3, 1],
        "Gast_ID": [2, 3, 4, 3],
        "Datum": ["2024-09-15", "2024-09-22", "2024-09-29", "2024-10-06"],
        "Heim_Tore": [2, 1, 3, 4],
        "Gast_Tore": [1, 1, 0, 2]
    })

    # Freundschaftsnetzwerk als Kantenliste
    friendships = pl.DataFrame({
        "person_a": ["Alice", "Alice", "Bob", "Carol", "Dave", "Eve"],
        "person_b": ["Bob", "Carol", "Carol", "Dave", "Eve", "Alice"]
    })

    return friendships, pl, px, spieler, spiele, vereine


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 2: INNER JOIN

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 2.1: Spieler mit Vereinsnamen

        Zeigen Sie alle Spieler mit ihrem Vereinsnamen und der Stadt.
        Der INNER JOIN liefert nur Spieler, die einem Verein zugeordnet sind.
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
        SELECT s.Name AS Spieler, s.Position, v.Name AS Verein, v.Stadt
        FROM spieler s
        INNER JOIN vereine v ON s.Verein_ID = v.Verein_ID
        ORDER BY v.Name, s.Name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 2.2: Spieler und Stadien

        Zeigen Sie alle Spieler mit ihrem Verein und dem zugehörigen Stadion.
        Ergänzen Sie die fehlenden Teile:
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
        SELECT s.Name AS Spieler, v.Name AS Verein, v.Stadion
        FROM spieler s
        ??? vereine v ON s.??? = v.???
        ORDER BY v.Name
        -- Tipp: INNER JOIN, Verein_ID
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT s.Name AS Spieler, v.Name AS Verein, v.Stadion
FROM spieler s
INNER JOIN vereine v ON s.Verein_ID = v.Verein_ID
ORDER BY v.Name
```

**Erklärung:** Der INNER JOIN verbindet `spieler` und `vereine` über die gemeinsame Spalte `Verein_ID`. Nur Spieler mit einem gültigen Verein werden angezeigt.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.3: Spieler in Städten mit 'ü'

        Finden Sie alle Spieler, deren Verein in einer Stadt mit dem Buchstaben 'ü' im Namen liegt.

        Hinweis: Verwenden Sie INNER JOIN + WHERE Stadt LIKE '%ü%'
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
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
SELECT s.Name AS Spieler, s.Position, v.Name AS Verein, v.Stadt
FROM spieler s
INNER JOIN vereine v ON s.Verein_ID = v.Verein_ID
WHERE v.Stadt LIKE '%ü%'
ORDER BY s.Name
```

**Erklärung:** Der INNER JOIN verknüpft Spieler mit Vereinen. `WHERE v.Stadt LIKE '%ü%'` filtert anschließend nach Städten, die ein 'ü' enthalten (hier: München).
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 2.4: Falscher JOIN-Schlüssel

        Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT s.Name AS Spieler, v.Name AS Verein
        FROM spieler s
        INNER JOIN vereine v ON s.Spieler_ID = v.Verein_ID
        ORDER BY v.Name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** Falscher JOIN-Schlüssel! `s.Spieler_ID = v.Verein_ID` verknüpft die Spieler-ID mit der Vereins-ID — das ist inhaltlich falsch und liefert zufällige Ergebnisse.

```sql
-- Korrektur:
SELECT s.Name AS Spieler, v.Name AS Verein
FROM spieler s
INNER JOIN vereine v ON s.Verein_ID = v.Verein_ID
ORDER BY v.Name
```

**Erklärung:** Der Fremdschlüssel `Verein_ID` in der Spieler-Tabelle verweist auf `Verein_ID` in der Vereine-Tabelle. Nur diese Spalten gehören in die ON-Bedingung.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: LEFT JOIN

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.1: Alle Spieler mit LEFT JOIN

        Zeigen Sie **alle** Spieler — auch die vereinslosen. Der LEFT JOIN behält alle Zeilen der linken Tabelle.
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
        SELECT
            s.Name AS Spieler,
            s.Position,
            v.Name AS Verein,
            v.Stadt
        FROM spieler s
        LEFT JOIN vereine v ON s.Verein_ID = v.Verein_ID
        ORDER BY v.Name NULLS LAST, s.Name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.2: Vereinslose Spieler finden

        Nutzen Sie LEFT JOIN + WHERE ... IS NULL, um nur die Spieler **ohne** Verein zu finden.
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
        SELECT
            s.Name AS Spieler,
            s.Position
        FROM spieler s
        LEFT JOIN vereine v ON s.Verein_ID = v.Verein_ID
        WHERE v.Verein_ID IS NULL
        ORDER BY s.Name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 4.3: Spieler pro Verein zählen

        Zeigen Sie alle Vereine mit der Anzahl ihrer Spieler — auch Vereine ohne Spieler (mit 0).
        Ergänzen Sie die fehlenden Teile:
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
        SELECT v.Name AS Verein, COUNT(???) AS Anzahl_Spieler
        FROM vereine v
        ??? JOIN spieler s ON v.Verein_ID = s.Verein_ID
        GROUP BY ???
        ORDER BY Anzahl_Spieler DESC
        -- Tipp: LEFT JOIN, COUNT(s.Spieler_ID), GROUP BY v.Name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT v.Name AS Verein, COUNT(s.Spieler_ID) AS Anzahl_Spieler
FROM vereine v
LEFT JOIN spieler s ON v.Verein_ID = s.Verein_ID
GROUP BY v.Name
ORDER BY Anzahl_Spieler DESC
```

**Erklärung:**
- `COUNT(s.Spieler_ID)` zählt nur Nicht-NULL-Werte, d.h. nur tatsächlich vorhandene Spieler
- `LEFT JOIN` stellt sicher, dass auch Vereine ohne Spieler (z.B. RB Leipzig) erscheinen
- `GROUP BY v.Name` gruppiert nach Vereinsname
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.4: Vereine ohne Spieler

        Finden Sie alle Vereine, die **keine** Spieler in unserer Tabelle haben.

        Hinweis: LEFT JOIN von Vereine auf Spieler + WHERE ... IS NULL
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
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
SELECT v.Name AS Verein, v.Stadt
FROM vereine v
LEFT JOIN spieler s ON v.Verein_ID = s.Verein_ID
WHERE s.Spieler_ID IS NULL
ORDER BY v.Name
```

**Erklärung:** Aus der Perspektive der Vereine-Tabelle: Der LEFT JOIN behält alle Vereine. `WHERE s.Spieler_ID IS NULL` filtert diejenigen heraus, bei denen kein Spieler gefunden wurde — also Vereine ohne Spieler.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.5: Vereine mit Anzahl Heimspiele

        Zeigen Sie alle Vereine mit der Anzahl ihrer Heimspiele.

        Hinweis: LEFT JOIN vereine v auf spiele sp mit `v.Verein_ID = sp.Heim_ID`
        """
    )
    return


@app.cell
def _(mo, spiele, vereine):
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
SELECT v.Name AS Verein, COUNT(sp.Spiel_ID) AS Heimspiele
FROM vereine v
LEFT JOIN spiele sp ON v.Verein_ID = sp.Heim_ID
GROUP BY v.Name
ORDER BY Heimspiele DESC
```

**Erklärung:** Der LEFT JOIN über `Heim_ID` verknüpft jeden Verein mit seinen Heimspielen. `COUNT(sp.Spiel_ID)` zählt nur tatsächliche Spiele (NULL wird nicht gezählt). So erscheinen auch Vereine ohne Heimspiel mit 0.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 4.6: INNER statt LEFT JOIN

        Diese Abfrage soll **alle** Spieler zeigen, auch vereinslose. Aber es fehlen Spieler! Finden Sie den Fehler.
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage soll ALLE Spieler zeigen, auch vereinslose.
        -- Aber es fehlen Spieler! Finden Sie den Fehler.
        SELECT s.Name AS Spieler, v.Name AS Verein
        FROM spieler s
        INNER JOIN vereine v ON s.Verein_ID = v.Verein_ID
        ORDER BY s.Name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** `INNER JOIN` filtert automatisch alle Spieler heraus, deren `Verein_ID` NULL ist! Sabitzer, Reus und Götze verschwinden.

```sql
-- Korrektur:
SELECT s.Name AS Spieler, v.Name AS Verein
FROM spieler s
LEFT JOIN vereine v ON s.Verein_ID = v.Verein_ID
ORDER BY s.Name
```

**Erklärung:** Wenn Sie **alle** Zeilen der linken Tabelle behalten möchten (auch ohne passenden Partner rechts), brauchen Sie einen `LEFT JOIN` statt `INNER JOIN`.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Self-Joins & Multiple JOINs

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.1: Rückspiele finden (Self-Join)

        Ein Self-Join verknüpft eine Tabelle mit sich selbst. Finden Sie Hin- und Rückspiele (Heim und Gast vertauscht).
        """
    )
    return


@app.cell
def _(mo, spiele):
    _df = mo.sql(
        f"""
        SELECT
            s1.Spiel_ID AS Hinspiel_ID,
            s1.Datum AS Hinspiel_Datum,
            s1.Heim_ID AS Heim,
            s1.Gast_ID AS Gast,
            s2.Spiel_ID AS Rückspiel_ID,
            s2.Datum AS Rückspiel_Datum
        FROM spiele s1
        INNER JOIN spiele s2
            ON s1.Heim_ID = s2.Gast_ID
            AND s1.Gast_ID = s2.Heim_ID
        WHERE s1.Datum < s2.Datum
        ORDER BY s1.Datum
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.2: Spiele mit Vereinsnamen (Multiple JOINs)

        Die Spiele-Tabelle hat zwei Fremdschlüssel (Heim_ID, Gast_ID). Wir brauchen zwei JOINs zur Vereine-Tabelle, um beide Mannschaftsnamen anzuzeigen.
        """
    )
    return


@app.cell
def _(mo, spiele, vereine):
    _df = mo.sql(
        f"""
        SELECT
            sp.Datum,
            vh.Name AS Heimmannschaft,
            vg.Name AS Gastmannschaft,
            sp.Heim_Tore,
            sp.Gast_Tore
        FROM spiele sp
        INNER JOIN vereine vh ON sp.Heim_ID = vh.Verein_ID
        INNER JOIN vereine vg ON sp.Gast_ID = vg.Verein_ID
        ORDER BY sp.Datum
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 6.3: Sieger per CASE WHEN bestimmen

        Erweitern Sie die Spielübersicht um eine Ergebnis- und eine Sieger-Spalte.
        Ergänzen Sie die fehlenden Teile im CASE WHEN:
        """
    )
    return


@app.cell
def _(mo, spiele, vereine):
    _df = mo.sql(
        f"""
        SELECT
            sp.Datum,
            vh.Name AS Heim,
            vg.Name AS Gast,
            sp.Heim_Tore || ':' || sp.Gast_Tore AS Ergebnis,
            CASE
                WHEN sp.Heim_Tore > sp.Gast_Tore THEN ???
                WHEN sp.Heim_Tore < sp.Gast_Tore THEN ???
                ELSE 'Unentschieden'
            END AS Sieger
        FROM spiele sp
        INNER JOIN vereine vh ON sp.Heim_ID = vh.Verein_ID
        INNER JOIN vereine vg ON sp.Gast_ID = vg.Verein_ID
        ORDER BY sp.Datum
        -- Tipp: vh.Name für Heimsieg, vg.Name für Gastsieg
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sp.Datum,
    vh.Name AS Heim,
    vg.Name AS Gast,
    sp.Heim_Tore || ':' || sp.Gast_Tore AS Ergebnis,
    CASE
        WHEN sp.Heim_Tore > sp.Gast_Tore THEN vh.Name
        WHEN sp.Heim_Tore < sp.Gast_Tore THEN vg.Name
        ELSE 'Unentschieden'
    END AS Sieger
FROM spiele sp
INNER JOIN vereine vh ON sp.Heim_ID = vh.Verein_ID
INNER JOIN vereine vg ON sp.Gast_ID = vg.Verein_ID
ORDER BY sp.Datum
```

**Erklärung:** Durch die zwei JOINs stehen `vh.Name` (Heimverein) und `vg.Name` (Gastverein) zur Verfügung. Im `CASE WHEN` können wir so den Sieger namentlich ausgeben.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.4: Gesamttore pro Verein (heim + gast)

        Berechnen Sie die Gesamttore jedes Vereins — sowohl als Heim- als auch als Gastmannschaft.

        Hinweis: Sie können zwei JOINs oder einen UNION-Ansatz verwenden.
        """
    )
    return


@app.cell
def _(mo, spiele, vereine):
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
WITH alle_tore AS (
    SELECT Heim_ID AS Verein_ID, Heim_Tore AS Tore FROM spiele
    UNION ALL
    SELECT Gast_ID AS Verein_ID, Gast_Tore AS Tore FROM spiele
)
SELECT v.Name AS Verein, SUM(a.Tore) AS Gesamttore
FROM alle_tore a
INNER JOIN vereine v ON a.Verein_ID = v.Verein_ID
GROUP BY v.Name
ORDER BY Gesamttore DESC
```

**Erklärung:** Mit `UNION ALL` kombinieren wir Heim- und Gasttore in eine einheitliche Struktur. Dann gruppieren wir nach Verein und summieren alle Tore. Der JOIN auf `vereine` liefert den lesbaren Namen.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.5: Freunde von Freunden von Bob

        Finden Sie alle Personen, die Bob über genau **zwei Schritte** im Freundschaftsnetzwerk erreichen kann (Freunde von Freunden).

        Hinweis: Zwei-Hop-JOIN auf `friendships`, startend bei `person_a = 'Bob'`
        """
    )
    return


@app.cell
def _(friendships, mo):
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
SELECT DISTINCT
    f1.person_a AS Person,
    f1.person_b AS Direkter_Freund,
    f2.person_b AS Freund_des_Freundes
FROM friendships f1
INNER JOIN friendships f2 ON f1.person_b = f2.person_a
WHERE f1.person_a = 'Bob'
  AND f2.person_b != 'Bob'
ORDER BY f1.person_b, f2.person_b
```

**Erklärung:** Der Self-Join verbindet die erste Kante (Bob → Freund) mit der zweiten Kante (Freund → Freund-des-Freundes). `WHERE f2.person_b != 'Bob'` schließt den Rückweg zu Bob selbst aus.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.6: Doppelte Spielpaare

        Diese Abfrage zeigt Hin-/Rückspielpaare — aber jedes Paar erscheint doppelt. Beheben Sie das Problem!
        """
    )
    return


@app.cell
def _(mo, spiele):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage zeigt Spielpaare doppelt. Beheben Sie das Problem!
        SELECT
            s1.Spiel_ID AS Spiel_1,
            s2.Spiel_ID AS Spiel_2,
            s1.Heim_ID, s1.Gast_ID
        FROM spiele s1
        INNER JOIN spiele s2
            ON s1.Heim_ID = s2.Gast_ID
            AND s1.Gast_ID = s2.Heim_ID
        ORDER BY s1.Spiel_ID
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** Ohne Einschränkung liefert der Self-Join jedes Paar zweimal: einmal als (Spiel_1, Spiel_2) und einmal als (Spiel_2, Spiel_1).

```sql
-- Korrektur:
SELECT
    s1.Spiel_ID AS Spiel_1,
    s2.Spiel_ID AS Spiel_2,
    s1.Heim_ID, s1.Gast_ID
FROM spiele s1
INNER JOIN spiele s2
    ON s1.Heim_ID = s2.Gast_ID
    AND s1.Gast_ID = s2.Heim_ID
WHERE s1.Spiel_ID < s2.Spiel_ID
ORDER BY s1.Spiel_ID
```

**Erklärung:** `WHERE s1.Spiel_ID < s2.Spiel_ID` sorgt dafür, dass jedes Paar nur einmal erscheint — das Spiel mit der kleineren ID steht immer links.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration — Herausforderungen

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Herausforderung 1: Torverhältnis pro Spiel als Balkendiagramm

        Erstellen Sie ein Balkendiagramm, das für jedes Spiel die Heim- und Gasttore zeigt. Nutzen Sie die Vereinsnamen (nicht IDs) auf der x-Achse.
        """
    )
    return


@app.cell
def _(mo, spiele, vereine):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- ⭐ Torverhältnis pro Spiel
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```python
spiel_daten = mo.sql(f\"\"\"
    SELECT
        vh.Name || ' vs. ' || vg.Name AS Spiel,
        sp.Heim_Tore,
        sp.Gast_Tore
    FROM spiele sp
    INNER JOIN vereine vh ON sp.Heim_ID = vh.Verein_ID
    INNER JOIN vereine vg ON sp.Gast_ID = vg.Verein_ID
    ORDER BY sp.Datum
\"\"\")

px.bar(
    spiel_daten.to_pandas().melt(id_vars="Spiel", var_name="Typ", value_name="Tore"),
    x="Spiel",
    y="Tore",
    color="Typ",
    barmode="group",
    title="Torverhältnis pro Spiel",
    labels={"Typ": ""},
)
```

**Erklärung:** Zwei JOINs liefern die Vereinsnamen. `melt()` wandelt Heim_Tore und Gast_Tore in ein Langformat um, das Plotly als gruppiertes Balkendiagramm darstellen kann.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐ Herausforderung 2: Punktetabelle aus Spiele-Tabelle

        Erstellen Sie eine Punktetabelle direkt aus der `spiele`-Tabelle. Vergeben Sie: 3 Punkte für einen Sieg, 1 Punkt für ein Unentschieden, 0 Punkte für eine Niederlage.
        """
    )
    return


@app.cell
def _(mo, spiele, vereine):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- ⭐⭐ Punktetabelle berechnen
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH ergebnisse AS (
    SELECT Heim_ID AS Verein_ID,
           CASE WHEN Heim_Tore > Gast_Tore THEN 3
                WHEN Heim_Tore = Gast_Tore THEN 1
                ELSE 0 END AS Punkte,
           Heim_Tore AS Tore, Gast_Tore AS Gegentore
    FROM spiele
    UNION ALL
    SELECT Gast_ID AS Verein_ID,
           CASE WHEN Gast_Tore > Heim_Tore THEN 3
                WHEN Gast_Tore = Heim_Tore THEN 1
                ELSE 0 END AS Punkte,
           Gast_Tore AS Tore, Heim_Tore AS Gegentore
    FROM spiele
)
SELECT v.Name AS Verein,
       COUNT(*) AS Spiele,
       SUM(CASE WHEN e.Punkte = 3 THEN 1 ELSE 0 END) AS Siege,
       SUM(CASE WHEN e.Punkte = 1 THEN 1 ELSE 0 END) AS Unentschieden,
       SUM(CASE WHEN e.Punkte = 0 THEN 1 ELSE 0 END) AS Niederlagen,
       SUM(e.Tore) AS Tore,
       SUM(e.Gegentore) AS Gegentore,
       SUM(e.Tore) - SUM(e.Gegentore) AS Tordifferenz,
       SUM(e.Punkte) AS Punkte
FROM ergebnisse e
INNER JOIN vereine v ON e.Verein_ID = v.Verein_ID
GROUP BY v.Name
ORDER BY Punkte DESC, Tordifferenz DESC
```

**Erklärung:** Ein CTE (WITH) kombiniert per UNION ALL die Heim- und Gastergebnisse. CASE WHEN berechnet die Punkte. Dann wird nach Verein gruppiert und aggregiert — eine vollständige Tabelle entsteht!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐⭐ Herausforderung 3: 3-Hop-Pfade im Freundschaftsnetzwerk

        Finden Sie alle Pfade der Länge 3 im Freundschaftsnetzwerk (z.B. Alice → Bob → Carol → Dave). Vermeiden Sie Zyklen (keine Person darf im Pfad doppelt vorkommen).
        """
    )
    return


@app.cell
def _(friendships, mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        -- ⭐⭐⭐ 3-Hop-Pfade
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT DISTINCT
    f1.person_a AS Schritt_0,
    f1.person_b AS Schritt_1,
    f2.person_b AS Schritt_2,
    f3.person_b AS Schritt_3
FROM friendships f1
INNER JOIN friendships f2 ON f1.person_b = f2.person_a
INNER JOIN friendships f3 ON f2.person_b = f3.person_a
WHERE f1.person_a != f2.person_b
  AND f1.person_a != f3.person_b
  AND f1.person_b != f3.person_b
ORDER BY Schritt_0, Schritt_1, Schritt_2, Schritt_3
```

**Erklärung:** Drei Self-Joins auf die Kantenliste bilden 3-Hop-Pfade. Die WHERE-Bedingungen verhindern Zyklen: Keine Person darf an zwei verschiedenen Stellen im Pfad auftauchen. Das ist die Grundidee von Graphtraversierung in SQL!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | JOIN-Typ | Beschreibung | Typischer Anwendungsfall |
        |----------|--------------|--------------------------|
        | **INNER JOIN** | Nur passende Zeilen aus beiden Tabellen | Standardfall: Daten zusammenführen |
        | **LEFT JOIN** | Alle links + passende rechts (NULL wenn kein Treffer) | Fehlende Verknüpfungen finden |
        | **RIGHT JOIN** | Alle rechts + passende links (NULL wenn kein Treffer) | Selten, meist LEFT bevorzugt |
        | **Self-Join** | Tabelle mit sich selbst verknüpfen | Hierarchien, Graphen, Vergleiche |
        | **Multiple JOINs** | Mehrere Tabellen in einer Abfrage | Zwei Fremdschlüssel (z.B. Heim/Gast) |

        **Merksätze:**
        - INNER = Schnittmenge (nur Treffer)
        - LEFT/RIGHT = Alles von einer Seite, passende von der anderen
        - Self-Join = Gleiche Tabelle, verschiedene Aliase
        - `LEFT JOIN` + `WHERE ... IS NULL` = Finde unverknüpfte Einträge

        **Nächste Session:** Subqueries, Views & Transaktionen
        """
    )
    return


if __name__ == "__main__":
    app.run()
