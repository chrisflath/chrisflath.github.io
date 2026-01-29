import marimo

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 9: JOINs - Tabellen verknuepfen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 9: JOINs - Tabellen verknuepfen

        In dieser Session lernen Sie:

        - **INNER JOIN**: Nur passende Zeilen aus beiden Tabellen
        - **LEFT JOIN**: Alle Zeilen der linken Tabelle + passende rechte
        - **RIGHT JOIN**: Alle Zeilen der rechten Tabelle + passende linke
        - **Self-Join**: Eine Tabelle mit sich selbst verknuepfen
        - **Bonus**: Graphen als Kantenlisten

        ---

        Nach der Normalisierung (Session 8) sind unsere Daten auf mehrere Tabellen verteilt.
        JOINs bringen sie wieder zusammen - ohne die Nachteile der Redundanz!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Datenmodell: Bundesliga-Szenario

        Wir arbeiten mit drei normalisierten Tabellen:

        - **Vereine**: Vereinsstammdaten
        - **Spieler**: Spielerdaten mit Verweis auf Verein (manche ohne Verein!)
        - **Spiele**: Begegnungen zwischen Vereinen

        ---
        """
    )
    return


@app.cell
def _():
    import pandas as pd

    # Vereine
    vereine = pd.DataFrame({
        "Verein_ID": [1, 2, 3, 4],
        "Name": ["Bayern Muenchen", "Bayer Leverkusen", "BVB Dortmund", "RB Leipzig"],
        "Stadt": ["Muenchen", "Leverkusen", "Dortmund", "Leipzig"],
        "Stadion": ["Allianz Arena", "BayArena", "Signal Iduna Park", "Red Bull Arena"]
    })

    vereine
    return pd, vereine


@app.cell
def _(pd):
    # Spieler - manche ohne Verein (NULL), um LEFT JOIN zu demonstrieren
    spieler = pd.DataFrame({
        "Spieler_ID": [1, 2, 3, 4, 5, 6, 7, 8],
        "Name": ["Mueller", "Neuer", "Wirtz", "Xhaka", "Hummels", "Sabitzer", "Reus", "Goetze"],
        "Position": ["Sturm", "Tor", "Mittelfeld", "Mittelfeld", "Abwehr", "Mittelfeld", "Mittelfeld", "Mittelfeld"],
        "Verein_ID": [1, 1, 2, 2, 3, None, None, None]  # Einige Spieler ohne Verein
    })

    spieler
    return (spieler,)


@app.cell
def _(pd):
    # Spiele - Heim vs Gast
    spiele = pd.DataFrame({
        "Spiel_ID": [1, 2, 3, 4],
        "Heim_ID": [1, 2, 3, 1],
        "Gast_ID": [2, 3, 4, 3],
        "Datum": ["2024-09-15", "2024-09-22", "2024-09-29", "2024-10-06"],
        "Heim_Tore": [2, 1, 3, 4],
        "Gast_Tore": [1, 1, 0, 2]
    })

    spiele
    return (spiele,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beachten Sie:**
        - Spieler 6-8 (Sabitzer, Reus, Goetze) haben **keine Verein_ID** (vereinslos)
        - Verein 4 (RB Leipzig) hat **keine Spieler** in unserer Tabelle
        - Die Spiele-Tabelle hat **zwei Fremdschluessel** (Heim_ID, Gast_ID)

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## INNER JOIN: Nur Treffer

        Der **INNER JOIN** gibt nur Zeilen zurueck, bei denen der JOIN-Schluessel
        in **beiden** Tabellen existiert.

        ```
        Tabelle A           Tabelle B
        +-------+           +-------+
        |   1   |----+  +---|   1   |
        |   2   |    +--+   |   3   |
        |   3   |----+  +---|   4   |
        +-------+    +------+-------+

        Ergebnis: Nur 1 und 3 (die Schnittmenge)
        ```

        ---

        ### Aufgabe 9.1: Spieler mit Vereinsnamen

        Zeigen Sie alle Spieler mit ihrem Vereinsnamen.
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
        -- INNER JOIN: Nur Spieler MIT Verein werden angezeigt
        SELECT
            s.Name AS Spieler,
            s.Position,
            v.Name AS Verein,
            v.Stadt
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
        **Beobachtung:** Nur **5 Spieler** werden angezeigt!

        - Sabitzer, Reus und Goetze fehlen (haben keine Verein_ID)
        - Der INNER JOIN filtert automatisch NULL-Werte heraus

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## LEFT JOIN: Alle aus der linken Tabelle

        Der **LEFT JOIN** behaelt alle Zeilen der **linken** Tabelle,
        auch wenn es keinen passenden Eintrag in der rechten gibt.

        ```
        Tabelle A           Tabelle B
        +-------+           +-------+
        |   1   |-----------|   1   |
        |   2   |---> NULL  |   3   |
        |   3   |-----------|   4   |
        +-------+           +-------+

        Ergebnis: 1, 2 (mit NULL), 3
        ```

        ---

        ### Aufgabe 9.2: Alle Spieler, auch ohne Verein

        Zeigen Sie **alle** Spieler - auch die vereinslosen.
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
        -- LEFT JOIN: Alle Spieler, egal ob mit oder ohne Verein
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
        **Beobachtung:** Jetzt sehen wir alle **8 Spieler**!

        - Sabitzer, Reus und Goetze haben NULL bei Verein und Stadt
        - Der LEFT JOIN behaelt alle Zeilen aus `spieler` (linke Tabelle)

        ---

        ### Aufgabe 9.2b: Nur Spieler ohne Verein finden

        **Wichtige Technik:** Mit `WHERE ... IS NULL` finden wir unverknuepfte Eintraege.
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
        -- LEFT JOIN + IS NULL: Finde Spieler OHNE Verein
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
        **Anwendungsfaelle fuer LEFT JOIN + IS NULL:**

        - Kunden ohne Bestellungen finden
        - Produkte ohne Verkaeufe identifizieren
        - Mitarbeiter ohne Projekte auflisten
        - Datensaetze mit fehlenden Referenzen aufspueren

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## RIGHT JOIN: Alle aus der rechten Tabelle

        Der **RIGHT JOIN** ist das Spiegelbild des LEFT JOIN:
        Er behaelt alle Zeilen der **rechten** Tabelle.

        ---

        ### Aufgabe 9.3: Alle Vereine, auch ohne Spieler

        Zeigen Sie alle Vereine - auch die ohne Spieler in unserer Tabelle.
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
        -- RIGHT JOIN: Alle Vereine, auch ohne Spieler
        SELECT
            v.Name AS Verein,
            v.Stadt,
            s.Name AS Spieler,
            s.Position
        FROM spieler s
        RIGHT JOIN vereine v ON s.Verein_ID = v.Verein_ID
        ORDER BY v.Name, s.Name NULLS LAST
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** RB Leipzig erscheint mit NULL-Werten fuer Spieler!

        **Praxis-Tipp:** Die meisten SQL-Entwickler bevorzugen LEFT JOIN und
        ordnen die Tabellen entsprechend an. RIGHT JOIN ist seltener.

        ```sql
        -- Diese beiden sind aequivalent:
        FROM spieler s RIGHT JOIN vereine v ON ...
        FROM vereine v LEFT JOIN spieler s ON ...
        ```

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Multiple JOINs: Mehrere Tabellen verknuepfen

        ---

        ### Aufgabe 9.3b: Spieler mit Verein und Stadt kombiniert

        Erstellen Sie eine vollstaendige Uebersicht aller Spieler mit Verein.
        """
    )
    return


@app.cell
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
        -- Kombination: Spieler mit allen Vereinsdetails
        SELECT
            s.Name AS Spieler,
            s.Position,
            v.Name AS Verein,
            v.Stadt,
            v.Stadion
        FROM spieler s
        INNER JOIN vereine v ON s.Verein_ID = v.Verein_ID
        ORDER BY v.Stadt, s.Name
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Self-Join: Tabelle mit sich selbst verknuepfen

        Ein **Self-Join** verknuepft eine Tabelle mit sich selbst.
        Das ist nuetzlich fuer hierarchische Daten oder Beziehungen
        innerhalb einer Tabelle.

        **Beispiel:** Finde Rueckspiele (Heim und Gast getauscht)

        ---

        ### Aufgabe 9.4: Rueckspiele finden

        Welche Spiele haben ein Rueckspiel in unseren Daten?
        (Heim und Gast sind vertauscht)
        """
    )
    return


@app.cell
def _(mo, spiele):
    _df = mo.sql(
        f"""
        -- Self-Join: Finde Hin- und Rueckspiele
        SELECT
            s1.Spiel_ID AS Hinspiel_ID,
            s1.Datum AS Hinspiel_Datum,
            s1.Heim_ID AS Heim,
            s1.Gast_ID AS Gast,
            s2.Spiel_ID AS Rueckspiel_ID,
            s2.Datum AS Rueckspiel_Datum
        FROM spiele s1
        INNER JOIN spiele s2
            ON s1.Heim_ID = s2.Gast_ID
            AND s1.Gast_ID = s2.Heim_ID
        WHERE s1.Datum < s2.Datum  -- Nur einmal zeigen (Hinspiel vor Rueckspiel)
        ORDER BY s1.Datum
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Erklaerung:**
        - Wir joinen `spiele` mit sich selbst (Alias s1 und s2)
        - Bedingung: Heim wird Gast und Gast wird Heim
        - `WHERE s1.Datum < s2.Datum` verhindert Duplikate

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Spiele mit Vereinsnamen (Multiple JOINs)

        Die Spiele-Tabelle hat zwei Fremdschluessel. Wir brauchen zwei JOINs
        zur Vereine-Tabelle, um beide Mannschaftsnamen anzuzeigen.
        """
    )
    return


@app.cell
def _(mo, spiele, vereine):
    _df = mo.sql(
        f"""
        -- Zwei JOINs auf dieselbe Tabelle mit verschiedenen Aliasen
        SELECT
            sp.Datum,
            vh.Name AS Heimmannschaft,
            vg.Name AS Gastmannschaft,
            sp.Heim_Tore,
            sp.Gast_Tore,
            CASE
                WHEN sp.Heim_Tore > sp.Gast_Tore THEN vh.Name
                WHEN sp.Heim_Tore < sp.Gast_Tore THEN vg.Name
                ELSE 'Unentschieden'
            END AS Ergebnis
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
        ---

        ## Sidebar: Graphen als Kantenlisten

        Soziale Netzwerke, Strassennetze und andere Graphen lassen sich
        elegant als **Kantenlisten** speichern und mit Self-Joins abfragen.

        ---
        """
    )
    return


@app.cell
def _(pd):
    # Freundschaftsnetzwerk als Kantenliste
    friendships = pd.DataFrame({
        "person_a": ["Alice", "Alice", "Bob", "Carol", "Dave", "Eve"],
        "person_b": ["Bob", "Carol", "Carol", "Dave", "Eve", "Alice"]
    })

    friendships
    return (friendships,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Graph-Darstellung:**
        ```
        Alice --- Bob
          |  \     |
          |   \    |
          |    \   |
        Eve --- Carol --- Dave
        ```

        ---

        ### Aufgabe 9.5 (Optional): Freunde von Freunden

        Wer sind die "Freunde von Freunden" von Alice?
        (Personen, die Alice ueber genau einen Zwischenschritt erreichen kann)
        """
    )
    return


@app.cell
def _(friendships, mo):
    _df = mo.sql(
        f"""
        -- Freunde von Freunden (2 Hops)
        SELECT DISTINCT
            f1.person_a AS Person,
            f1.person_b AS Direkter_Freund,
            f2.person_b AS Freund_des_Freundes
        FROM friendships f1
        INNER JOIN friendships f2 ON f1.person_b = f2.person_a
        WHERE f1.person_a = 'Alice'
          AND f2.person_b != f1.person_a  -- Nicht zurueck zur Ausgangsperson
        ORDER BY f1.person_b, f2.person_b
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Anwendungen von Graph-Abfragen:**

        - Soziale Netzwerke: "Personen, die du kennen koenntest"
        - Routenplanung: Verbindungen zwischen Staedten
        - Empfehlungssysteme: "Kunden kauften auch..."
        - Organisationshierarchien: Mitarbeiter → Manager → Director

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Freie Exploration

        Experimentieren Sie mit JOINs!

        **Ideen:**
        - Welcher Verein hat die meisten Spieler?
        - Welche Spieler haben noch nie gespielt (wenn wir eine Spielereinsatz-Tabelle haetten)?
        - Wie viele Tore wurden in jedem Stadion geschossen?
        """
    )
    return


@app.cell
def _(mo, spieler, spiele, vereine):
    # Ihre Abfrage hier:
    _df = mo.sql(
        f"""
        -- Beispiel: Spieler pro Verein zaehlen
        SELECT
            v.Name AS Verein,
            COUNT(s.Spieler_ID) AS Anzahl_Spieler
        FROM vereine v
        LEFT JOIN spieler s ON v.Verein_ID = s.Verein_ID
        GROUP BY v.Name
        ORDER BY Anzahl_Spieler DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | JOIN-Typ | Beschreibung | Typischer Anwendungsfall |
        |----------|--------------|--------------------------|
        | **INNER JOIN** | Nur passende Zeilen | Standardfall: Daten zusammenfuehren |
        | **LEFT JOIN** | Alle links + passende rechts | Fehlende Verknuepfungen finden |
        | **RIGHT JOIN** | Alle rechts + passende links | Selten, meist LEFT bevorzugt |
        | **Self-Join** | Tabelle mit sich selbst | Hierarchien, Graphen, Vergleiche |

        **Merksaetze:**
        - INNER = Schnittmenge
        - LEFT/RIGHT = Alles von einer Seite, passende von der anderen
        - Self-Join = Gleiche Tabelle, verschiedene Aliase

        **Naechste Session:** Subqueries und komplexe Abfragen
        """
    )
    return


if __name__ == "__main__":
    app.run()
