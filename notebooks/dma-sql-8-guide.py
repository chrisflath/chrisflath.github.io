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
    app_title="DMA Session 8: JOINs — Guide",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 8: JOINs — Guide

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · II: Datenmodellierung (S5–7) · **▸ III: Fortgeschrittenes SQL (S8–9)** · IV: Datenanalyse (S10–13)

        ### Lernziele

        Nach dieser Session können Sie:

        - **INNER JOIN** für passende Verknüpfungen anwenden
        - **LEFT JOIN** für fehlende Verknüpfungen nutzen
        - **Self-Joins** für Rückspiele und Hierarchien verstehen
        - Mehrere JOINs **kombinieren**
        - Den richtigen **JOIN-Typ** wählen

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Daten laden

        Wir arbeiten heute mit drei normalisierten Tabellen:

        1. **Vereine** — Vereinsstammdaten (4 Vereine)
        2. **Spieler** — Spielerdaten mit Verweis auf Verein (8 Spieler, davon 3 ohne Verein!)
        3. **Spiele** — Begegnungen zwischen Vereinen (zwei Fremdschlüssel)
        4. **Friendships** — Kantenliste für Graph-Abfragen
        """
    )
    return


@app.cell(hide_code=True)
def _():
    import polars as pl

    vereine = pl.DataFrame({
        "Verein_ID": [1, 2, 3, 4],
        "Name": ["Bayern München", "Bayer Leverkusen", "BVB Dortmund", "RB Leipzig"],
        "Stadt": ["München", "Leverkusen", "Dortmund", "Leipzig"],
        "Stadion": ["Allianz Arena", "BayArena", "Signal Iduna Park", "Red Bull Arena"]
    })

    spieler = pl.DataFrame({
        "Spieler_ID": [1, 2, 3, 4, 5, 6, 7, 8],
        "Name": ["Müller", "Neuer", "Wirtz", "Xhaka", "Hummels", "Sabitzer", "Reus", "Götze"],
        "Position": ["Sturm", "Tor", "Mittelfeld", "Mittelfeld", "Abwehr", "Mittelfeld", "Mittelfeld", "Mittelfeld"],
        "Verein_ID": [1, 1, 2, 2, 3, None, None, None]
    })

    spiele = pl.DataFrame({
        "Spiel_ID": [1, 2, 3, 4],
        "Heim_ID": [1, 2, 3, 1],
        "Gast_ID": [2, 3, 4, 3],
        "Datum": ["2024-09-15", "2024-09-22", "2024-09-29", "2024-10-06"],
        "Heim_Tore": [2, 1, 3, 4],
        "Gast_Tore": [1, 1, 0, 2]
    })

    friendships = pl.DataFrame({
        "person_a": ["Alice", "Alice", "Bob", "Carol", "Dave", "Eve"],
        "person_b": ["Bob", "Carol", "Carol", "Dave", "Eve", "Alice"]
    })

    return friendships, pl, spieler, spiele, vereine


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beachten Sie:**

        - 8 Spieler, davon 3 ohne Verein (Sabitzer, Reus, Götze haben `Verein_ID = NULL`)
        - RB Leipzig (Verein_ID 4) hat **0 Spieler** in unserer Tabelle
        - Die Spiele-Tabelle hat **zwei Fremdschlüssel** (Heim_ID, Gast_ID) auf Vereine

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 1: INNER JOIN — Nur Treffer

        Der **INNER JOIN** gibt nur Zeilen zurück, bei denen der JOIN-Schlüssel
        in **beiden** Tabellen existiert — die **Schnittmenge**.

        ```
        Spieler (links)       Vereine (rechts)
        +-----------+         +-----------+
        | Müller  1 |----+----|  1 Bayern  |
        | Neuer   1 |    |    |  2 Leverk. |
        | Wirtz   2 |----+----|  3 BVB     |
        | Xhaka   2 |    |    |  4 Leipzig |
        | Hummels 3 |----+    +-----------+
        | Sabitzer ∅ |  → weg!
        | Reus    ∅ |  → weg!
        | Götze   ∅ |  → weg!
        +-----------+

        Ergebnis: Nur 5 Zeilen (Spieler MIT Verein)
        ```

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
    vorhersage_inner = mo.ui.radio(
        options={
            "5": "5 Zeilen",
            "8": "8 Zeilen",
            "11": "11 Zeilen",
            "3": "3 Zeilen",
        },
        label="8 Spieler, 3 ohne Verein. Wie viele Zeilen liefert ein INNER JOIN zwischen Spieler und Vereine?"
    )
    vorhersage_inner
    return (vorhersage_inner,)


@app.cell(hide_code=True)
def _(vorhersage_inner, mo):
    if vorhersage_inner.value == "5":
        mo.output.replace(mo.md("✅ **Richtig!** Nur 5 Spieler haben eine gültige `Verein_ID`. Die 3 Spieler ohne Verein (NULL) finden keinen Partner in der Vereine-Tabelle und werden vom INNER JOIN herausgefiltert."))
    elif vorhersage_inner.value == "8":
        mo.output.replace(mo.md("❌ 8 wären alle Spieler — aber der INNER JOIN filtert Spieler **ohne** passenden Verein heraus. Sabitzer, Reus und Götze haben `Verein_ID = NULL` und finden keinen Partner. Es bleiben nur **5 Zeilen**."))
    elif vorhersage_inner.value == "11":
        mo.output.replace(mo.md("❌ 11 wäre die Summe beider Tabellen (8+4) abzüglich einer Zeile — aber so funktioniert ein JOIN nicht. Der INNER JOIN gibt nur Zeilen zurück, bei denen der Schlüssel in **beiden** Tabellen existiert. Das sind **5 Zeilen**."))
    elif vorhersage_inner.value == "3":
        mo.output.replace(mo.md("❌ 3 sind die Spieler **ohne** Verein. Der INNER JOIN zeigt aber die Spieler **mit** Verein: Müller, Neuer (Bayern), Wirtz, Xhaka (Leverkusen), Hummels (BVB) = **5 Zeilen**."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 8.1: Spieler mit Vereinsnamen
    """)
    return


@app.cell(hide_code=True)
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
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
        **Beobachtung:** Nur **5 Spieler** werden angezeigt! Sabitzer, Reus und Götze fehlen —
        sie haben keine `Verein_ID` und finden daher keinen Partner in der Vereine-Tabelle.
        Der INNER JOIN filtert sie automatisch heraus.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Probieren Sie selbst: INNER JOIN

    Ändern Sie die Abfrage! Probieren Sie:
    - Andere Spalten im `SELECT` (z.B. `v.Stadion`)
    - Einen `WHERE`-Filter (z.B. `WHERE v.Stadt = 'München'`)
    - `ORDER BY` nach einer anderen Spalte
    """)
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
        INNER JOIN vereine v ON s.Verein_ID = v.Verein_ID
        ORDER BY v.Name, s.Name
        """
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 3: LEFT JOIN + RIGHT JOIN

        ### LEFT JOIN — Alle aus der linken Tabelle

        Der **LEFT JOIN** behält alle Zeilen der **linken** Tabelle,
        auch wenn es keinen passenden Eintrag in der rechten gibt.
        Fehlende Werte werden mit NULL aufgefüllt.

        ```
        Spieler (links)       Vereine (rechts)
        +-----------+         +-----------+
        | Müller  1 |---------|  1 Bayern  |
        | Neuer   1 |         |  2 Leverk. |
        | Wirtz   2 |---------|  3 BVB     |
        | Xhaka   2 |         |  4 Leipzig |
        | Hummels 3 |---------+-----------+
        | Sabitzer ∅ | → NULL, NULL
        | Reus    ∅ | → NULL, NULL
        | Götze   ∅ | → NULL, NULL
        +-----------+

        Ergebnis: Alle 8 Spieler (3 mit NULL-Vereinsdaten)
        ```

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    vorhersage_left = mo.ui.radio(
        options={
            "inner_links": "INNER JOIN von links",
            "left_verein": "LEFT JOIN mit Vereine als linke Tabelle",
            "right_spieler": "RIGHT JOIN mit Spieler als linke Tabelle",
            "left_spieler": "LEFT JOIN mit Spieler als linke Tabelle",
        },
        label="RB Leipzig hat 0 Spieler. Welcher JOIN zeigt alle 4 Vereine — auch die ohne Spieler?"
    )
    vorhersage_left
    return (vorhersage_left,)


@app.cell(hide_code=True)
def _(vorhersage_left, mo):
    if vorhersage_left.value == "left_verein":
        mo.output.replace(mo.md("✅ **Richtig!** `FROM vereine v LEFT JOIN spieler s` behält alle Vereine — auch RB Leipzig ohne Spieler. Die Spieler-Spalten werden dort mit NULL gefüllt."))
    elif vorhersage_left.value == "inner_links":
        mo.output.replace(mo.md("❌ Ein INNER JOIN zeigt nur Treffer in **beiden** Tabellen. RB Leipzig hat keine Spieler → es würde nicht erscheinen. Sie brauchen einen **LEFT JOIN mit Vereine als linke Tabelle**."))
    elif vorhersage_left.value == "right_spieler":
        mo.output.replace(mo.md("❌ Nicht ganz. `FROM spieler s RIGHT JOIN vereine v` wäre technisch korrekt (behält alle Vereine rechts), aber die elegantere Lösung ist `FROM vereine v LEFT JOIN spieler s` — **LEFT JOIN mit Vereine als linke Tabelle**."))
    elif vorhersage_left.value == "left_spieler":
        mo.output.replace(mo.md("❌ `FROM spieler s LEFT JOIN vereine v` behält alle **Spieler** (links), nicht alle **Vereine**. Um alle Vereine zu sehen, muss Vereine die **linke** Tabelle sein: `FROM vereine v LEFT JOIN spieler s`."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 8.2: LEFT JOIN — Alle Spieler
    """)
    return


@app.cell(hide_code=True)
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
        **Beobachtung:** Jetzt sehen wir alle **8 Spieler**! Sabitzer, Reus und Götze
        haben NULL bei Verein und Stadt — der LEFT JOIN behält sie trotzdem.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 8.2b: Nur vereinslose Spieler

    **Wichtige Technik:** Mit `LEFT JOIN` + `WHERE ... IS NULL` finden wir unverknüpfte Einträge — sogenannte "Waisen-Datensätze".
    """)
    return


@app.cell(hide_code=True)
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
        **Anwendungsfälle für LEFT JOIN + IS NULL:**

        - Kunden ohne Bestellungen finden
        - Produkte ohne Verkäufe identifizieren
        - Mitarbeiter ohne Projekte auflisten
        - Datensätze mit fehlenden Referenzen aufspüren

        ---

        ### RIGHT JOIN — Das Spiegelbild

        Der **RIGHT JOIN** ist das Spiegelbild des LEFT JOIN: Er behält alle Zeilen
        der **rechten** Tabelle.

        ```sql
        -- Diese beiden sind äquivalent:
        FROM spieler s RIGHT JOIN vereine v ON ...
        FROM vereine v LEFT JOIN spieler s ON ...
        ```

        **Praxis-Tipp:** Die meisten SQL-Entwickler bevorzugen LEFT JOIN und
        ordnen die Tabellen entsprechend an. RIGHT JOIN ist seltener.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 8.3: RIGHT JOIN — Alle Vereine
    """)
    return


@app.cell(hide_code=True)
def _(mo, spieler, vereine):
    _df = mo.sql(
        f"""
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
        **Beobachtung:** RB Leipzig erscheint mit NULL-Werten für Spieler!
        Derselbe Effekt wie `FROM vereine v LEFT JOIN spieler s`, nur mit vertauschter Reihenfolge.

        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 4.x**

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 5: Self-Joins + Multiple JOINs

        ### Self-Join — Eine Tabelle mit sich selbst verknüpfen

        Ein **Self-Join** verknüpft eine Tabelle mit sich selbst.
        Dazu verwendet man **zwei verschiedene Aliase** für dieselbe Tabelle.

        **Typische Anwendungsfälle:**
        - Rückspiele finden (Heim ↔ Gast vertauscht)
        - Hierarchien abfragen (Mitarbeiter → Manager)
        - Vergleiche innerhalb einer Tabelle

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 8.4: Rückspiele finden (Self-Join)

    Welche Spiele haben ein Rückspiel in unseren Daten? (Heim und Gast sind vertauscht)
    """)
    return


@app.cell(hide_code=True)
def _(mo, spiele):
    _df = mo.sql(
        f"""
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
        WHERE s1.Datum < s2.Datum
        ORDER BY s1.Datum
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Erklärung:**
        - Wir joinen `spiele` mit sich selbst (Alias `s1` und `s2`)
        - Bedingung: Heim wird Gast und Gast wird Heim
        - `WHERE s1.Datum < s2.Datum` verhindert Duplikate (Hinspiel vor Rückspiel)

        ---

        ### Multiple JOINs: Spiele mit beiden Vereinsnamen

        Die Spiele-Tabelle hat **zwei Fremdschlüssel** (Heim_ID, Gast_ID).
        Wir brauchen **zwei JOINs** zur Vereine-Tabelle, um beide Mannschaftsnamen anzuzeigen.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, spiele, vereine):
    _df = mo.sql(
        f"""
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

        ### Sidebar: Graphen als Kantenlisten

        Soziale Netzwerke, Straßennetze und andere Graphen lassen sich
        elegant als **Kantenlisten** speichern und mit Self-Joins abfragen.

        ```
        Alice --- Bob
          |  \     |
          |   \    |
          |    \   |
        Eve    Carol --- Dave
        ```

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Freunde von Freunden (Graph-Query)

    Wer sind die "Freunde von Freunden" von Alice?
    (Personen, die Alice über genau einen Zwischenschritt erreichen kann)
    """)
    return


@app.cell(hide_code=True)
def _(friendships, mo):
    _df = mo.sql(
        f"""
        SELECT DISTINCT
            f1.person_a AS Person,
            f1.person_b AS Direkter_Freund,
            f2.person_b AS Freund_des_Freundes
        FROM friendships f1
        INNER JOIN friendships f2 ON f1.person_b = f2.person_a
        WHERE f1.person_a = 'Alice'
          AND f2.person_b != f1.person_a
        ORDER BY f1.person_b, f2.person_b
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Anwendungen von Graph-Abfragen:**

        - Soziale Netzwerke: "Personen, die Sie kennen könnten"
        - Routenplanung: Verbindungen zwischen Städten
        - Empfehlungssysteme: "Kunden kauften auch..."
        - Organisationshierarchien: Mitarbeiter → Manager → Director

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    join_quiz1 = mo.ui.radio(
        options={
            "inner": "INNER JOIN",
            "left": "LEFT JOIN",
            "right": "RIGHT JOIN",
            "self": "Self-Join"
        },
        label="**Quiz:** Welcher JOIN zeigt auch Spieler, die keinem Verein zugeordnet sind?"
    )
    join_quiz1
    return (join_quiz1,)


@app.cell(hide_code=True)
def _(join_quiz1, mo):
    if join_quiz1.value == "left":
        mo.output.replace(mo.md("✅ **Richtig!** LEFT JOIN behält alle Zeilen der linken Tabelle (Spieler), auch wenn kein passender Verein existiert. Die Vereinsspalten werden dann mit NULL gefüllt."))
    elif join_quiz1.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Wir brauchen einen JOIN, der *alle* Spieler behält — auch die ohne Verein. Das ist der **LEFT JOIN** (mit Spieler als linke Tabelle)."))
    return


@app.cell(hide_code=True)
def _(mo):
    join_quiz2 = mo.ui.radio(
        options={
            "inner": "INNER JOIN",
            "left": "LEFT JOIN",
            "right": "RIGHT JOIN",
            "self": "Self-Join"
        },
        label="**Quiz:** Welchen JOIN-Typ brauchen Sie, um Rückspiele zu finden (gleiche Tabelle, verschiedene Zeilen)?"
    )
    join_quiz2
    return (join_quiz2,)


@app.cell(hide_code=True)
def _(join_quiz2, mo):
    if join_quiz2.value == "self":
        mo.output.replace(mo.md("✅ **Richtig!** Ein Self-Join verknüpft eine Tabelle mit sich selbst. Wir geben der Tabelle zwei verschiedene Aliase (s1 und s2), um Hin- und Rückspiel zu vergleichen."))
    elif join_quiz2.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Wir suchen innerhalb *derselben* Tabelle nach zueinander passenden Zeilen — das ist ein **Self-Join**."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 3
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    vorhersage_multi = mo.ui.radio(
        options={
            "1": "1 JOIN",
            "2": "2 JOINs",
            "3": "3 JOINs",
            "0": "0 JOINs",
        },
        label="Die Spiele-Tabelle hat Heim_ID und Gast_ID. Wie viele JOINs brauchen Sie, um beide Mannschaftsnamen anzuzeigen?"
    )
    vorhersage_multi
    return (vorhersage_multi,)


@app.cell(hide_code=True)
def _(vorhersage_multi, mo):
    if vorhersage_multi.value == "2":
        mo.output.replace(mo.md("✅ **Richtig!** Jeder Fremdschlüssel braucht seinen eigenen JOIN: einen für `Heim_ID → Vereine` (Alias `vh`) und einen für `Gast_ID → Vereine` (Alias `vg`). Zwei Schlüssel = zwei JOINs."))
    elif vorhersage_multi.value == "1":
        mo.output.replace(mo.md("❌ Ein JOIN würde nur **einen** der beiden Mannschaftsnamen auflösen. Da die Spiele-Tabelle **zwei** Fremdschlüssel hat (Heim_ID und Gast_ID), brauchen Sie **2 JOINs** — einen pro Schlüssel."))
    elif vorhersage_multi.value == "3":
        mo.output.replace(mo.md("❌ 3 wären zu viele. Sie brauchen einen JOIN pro Fremdschlüssel: `Heim_ID → Vereine` und `Gast_ID → Vereine`. Das sind genau **2 JOINs**."))
    elif vorhersage_multi.value == "0":
        mo.output.replace(mo.md("❌ Ohne JOIN könnten Sie nur die IDs anzeigen, nicht die Vereinsnamen. Sie brauchen **2 JOINs** zur Vereine-Tabelle — einen für Heim_ID und einen für Gast_ID."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 6.x**

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 7: Visualisierung — JOINs öffnen neue Dimensionen

        Nach einem JOIN stehen Spalten aus **mehreren Tabellen** zur Verfügung.
        Das ermöglicht reichere Visualisierungen mit `color=` und `facet_col=`.
        """
    )
    return


@app.cell(hide_code=True)
def _():
    import plotly.express as px
    return (px,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Spieler pro Verein (LEFT JOIN + GROUP BY + COUNT)
    """)
    return


@app.cell(hide_code=True)
def _(mo, px, spieler, vereine):
    spieler_pro_verein = mo.sql(
        f"""
        SELECT
            v.Name AS Verein,
            COUNT(s.Spieler_ID) AS Anzahl_Spieler
        FROM vereine v
        LEFT JOIN spieler s ON v.Verein_ID = s.Verein_ID
        GROUP BY v.Name
        ORDER BY Anzahl_Spieler DESC
        """
    )

    fig_bar = px.bar(
        spieler_pro_verein,
        x="Verein",
        y="Anzahl_Spieler",
        color="Verein",
        title="Anzahl Spieler pro Verein (LEFT JOIN zeigt auch 0-Spieler-Vereine)",
        labels={"Anzahl_Spieler": "Anzahl Spieler"},
    )
    fig_bar
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Tore vs. Assists nach Verein (Streudiagramm)
    """)
    return


@app.cell(hide_code=True)
def _(pl, px, vereine):
    spieler_stats = pl.DataFrame({
        "Spieler_ID": [1, 2, 3, 4, 5, 6, 7, 8],
        "Name": ["Müller", "Neuer", "Wirtz", "Xhaka", "Hummels", "Sabitzer", "Reus", "Götze"],
        "Tore": [12, 0, 15, 3, 1, 7, 8, 5],
        "Assists": [6, 1, 10, 8, 2, 4, 9, 6],
        "Verein_ID": [1, 1, 2, 2, 3, None, None, None]
    })

    merged = spieler_stats.join(
        vereine, on="Verein_ID", how="inner", suffix="_verein"
    )

    fig_scatter = px.scatter(
        merged,
        x="Tore",
        y="Assists",
        color="Name_verein",
        text="Name",
        title="Tore vs. Assists nach Verein (INNER JOIN)",
        labels={"Name_verein": "Verein"},
        size_max=15,
    ).update_traces(textposition="top center")
    fig_scatter
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Durch den JOIN können wir `color="Verein"` nutzen —
        eine Dimension, die in der Spieler-Tabelle allein nicht als lesbarer Name existiert.
        Das ist die Stärke von JOINs für die Visualisierung!

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Viz-Choice: Den richtigen JOIN für Visualisierung wählen
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    viz_choice_8 = mo.ui.radio(
        options={
            "inner": "INNER JOIN",
            "left": "LEFT JOIN",
            "right": "RIGHT JOIN",
            "cross": "CROSS JOIN",
        },
        label="Spieler pro Verein inkl. Vereine mit 0 Spielern. Welcher JOIN?"
    )
    viz_choice_8
    return (viz_choice_8,)


@app.cell(hide_code=True)
def _(viz_choice_8, mo):
    if viz_choice_8.value == "left":
        mo.output.replace(mo.md("✅ **Richtig!** Ein **LEFT JOIN** (mit Vereine als linke Tabelle) stellt sicher, dass auch Vereine **ohne Spieler** im Ergebnis erscheinen — z.B. RB Leipzig mit 0 Spielern. Ein INNER JOIN würde diese Vereine verlieren."))
    elif viz_choice_8.value == "inner":
        mo.output.replace(mo.md("❌ Ein INNER JOIN zeigt nur Vereine, die **mindestens einen** Spieler haben. RB Leipzig (0 Spieler) würde fehlen. Für eine vollständige Übersicht brauchen Sie einen **LEFT JOIN**."))
    elif viz_choice_8.value == "right":
        mo.output.replace(mo.md("❌ Ein RIGHT JOIN *könnte* funktionieren (wenn Vereine rechts steht), aber die Konvention ist **LEFT JOIN** mit der 'vollständigen' Tabelle links. Das ist lesbarer und verbreiteter."))
    elif viz_choice_8.value == "cross":
        mo.output.replace(mo.md("❌ Ein CROSS JOIN erzeugt das **kartesische Produkt** — jede Kombination aus Verein und Spieler. Das wäre viel zu viel und inhaltlich falsch. Sie brauchen einen **LEFT JOIN**."))
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
    selbsttest_8 = mo.ui.radio(
        options={
            "left_null": "LEFT JOIN + WHERE ... IS NULL",
            "inner": "INNER JOIN",
            "not_in": "NOT IN Subquery",
        },
        label="Welches Pattern findet 'Waisen-Datensätze' (z.B. Spieler ohne Verein)?"
    )
    selbsttest_8
    return (selbsttest_8,)


@app.cell(hide_code=True)
def _(selbsttest_8, mo):
    if selbsttest_8.value == "left_null":
        mo.output.replace(mo.md("✅ **Richtig!** `LEFT JOIN` + `WHERE ... IS NULL` ist das Standardmuster, um Datensätze ohne Verknüpfung zu finden. Der LEFT JOIN behält alle Zeilen der linken Tabelle, und `IS NULL` filtert auf die, die keinen Partner in der rechten Tabelle haben."))
    elif selbsttest_8.value == "inner":
        mo.output.replace(mo.md("❌ Ein INNER JOIN zeigt nur Zeilen **mit** Verknüpfung — das Gegenteil von dem, was wir suchen. Für 'Waisen-Datensätze' brauchen Sie **LEFT JOIN + WHERE ... IS NULL**."))
    elif selbsttest_8.value == "not_in":
        mo.output.replace(mo.md("❌ `NOT IN` kann funktionieren, ist aber fehleranfällig bei NULL-Werten und oft langsamer. Das Standardmuster ist **LEFT JOIN + WHERE ... IS NULL** — es ist robust, performant und gut lesbar."))
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
        | **LEFT JOIN** | Alle links + passende rechts (NULL wo keine) | Fehlende Verknüpfungen finden |
        | **RIGHT JOIN** | Alle rechts + passende links (NULL wo keine) | Selten, meist LEFT bevorzugt |
        | **Self-Join** | Tabelle mit sich selbst verknüpfen | Hierarchien, Graphen, Rückspiele |

        ### Merksätze

        - **INNER** = Schnittmenge — nur Zeilen mit Partner in beiden Tabellen
        - **LEFT/RIGHT** = Alles von einer Seite, passende von der anderen, NULL wo nichts passt
        - **Self-Join** = Gleiche Tabelle, verschiedene Aliase (z.B. `s1`, `s2`)
        - **LEFT JOIN + IS NULL** = Waisen finden (Datensätze ohne Verknüpfung)
        - **Mehrere JOINs** = Ein JOIN pro Fremdschlüssel (z.B. Heim_ID + Gast_ID)

        ### Ausblick Session 9

        Nächste Woche: **Subqueries, Views & Transaktionen** — verschachtelte Abfragen, wiederverwendbare Views und Transaktionssicherheit
        """
    )
    return


if __name__ == "__main__":
    app.run()
