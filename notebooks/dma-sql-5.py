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
    app_title="DMA Session 5: Datenmodellierung \u2014 \u00dcbungen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 5: Datenmodellierung — Übungen

        Theorie und geführte Beispiele → **05-datenmodellierung-guide.py**

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

    # Die "schlechte" Mega-Tabelle mit Redundanzen
    spieler_schlecht = pl.DataFrame({
        "Spieler": ["Müller", "Neuer", "Kimmich", "Sané", "Musiala",
                    "Wirtz", "Tah", "Frimpong", "Füllkrug", "Nmecha"],
        "Position": ["Sturm", "Tor", "Mittelfeld", "Sturm", "Mittelfeld",
                     "Mittelfeld", "Abwehr", "Abwehr", "Sturm", "Sturm"],
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
                          1904, 1904, 1904, 1895, 1895]
    })

    # Normalisierte Tabelle: Vereine (jeder Verein nur EINMAL)
    vereine = pl.DataFrame({
        "Verein_ID": [1, 2, 3],
        "Verein": ["Bayern München", "Bayer Leverkusen", "West Ham United"],
        "Vereinsort": ["München", "Leverkusen", "London"],
        "Stadion": ["Allianz Arena", "BayArena", "London Stadium"],
        "Gründungsjahr": [1900, 1904, 1895]
    })

    # Normalisierte Tabelle: Spieler (mit Verweis auf Verein)
    spieler_gut = pl.DataFrame({
        "Spieler_ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Spieler": ["Müller", "Neuer", "Kimmich", "Sané", "Musiala",
                    "Wirtz", "Tah", "Frimpong", "Füllkrug", "Nmecha"],
        "Position": ["Sturm", "Tor", "Mittelfeld", "Sturm", "Mittelfeld",
                     "Mittelfeld", "Abwehr", "Abwehr", "Sturm", "Sturm"],
        "Verein_ID": [1, 1, 1, 1, 1, 2, 2, 2, 3, 3]
    })

    spieler_schlecht
    return pl, px, spieler_gut, spieler_schlecht, vereine


# ============================================================
# Phase 2: Redundanz identifizieren
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 2: Redundanz identifizieren

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 2.1: Redundanz zählen

        Wie oft wird jede Vereinsinformation in der Mega-Tabelle gespeichert?
        Führen Sie die Abfrage aus und beobachten Sie die Wiederholungen:
        """
    )
    return


@app.cell
def _(mo, spieler_schlecht):
    _df = mo.sql(
        f"""
        SELECT Verein, Vereinsort, Stadion, COUNT(*) AS Anzahl_Wiederholungen
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
        ### 🟡 Aufgabe 2.2: Redundanz pro Verein

        Wie viele Zeilen sind pro Verein **redundant**?
        Ergänzen Sie die fehlenden `???`:
        """
    )
    return


@app.cell
def _(mo, spieler_schlecht):
    _df = mo.sql(
        f"""
        SELECT
            Verein,
            COUNT(*) AS Gesamt_Zeilen,
            ??? AS Redundante_Zeilen
        FROM spieler_schlecht
        GROUP BY ???
        ORDER BY Redundante_Zeilen DESC
        -- Tipp: COUNT(*) - 1 berechnet redundante Zeilen, GROUP BY Verein
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Verein,
    COUNT(*) AS Gesamt_Zeilen,
    COUNT(*) - 1 AS Redundante_Zeilen
FROM spieler_schlecht
GROUP BY Verein
ORDER BY Redundante_Zeilen DESC
```

**Erklärung:** Jeder Verein muss nur **einmal** gespeichert werden. Alle weiteren Zeilen (`COUNT(*) - 1`) sind reine Redundanz. Bayern München hat 5 Spieler, also 4 redundante Vereinseinträge.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.3: Speicherplatz-Berechnung

        Berechnen Sie für die gesamte Mega-Tabelle:
        - Wie viele **Gesamtzeilen** gibt es?
        - Wie viele **verschiedene Vereine** existieren?
        - Wie viele **redundante Vereinseinträge** gibt es (Differenz)?

        **Hinweis:** Verwenden Sie `COUNT(*)`, `COUNT(DISTINCT Verein)` und die Differenz.
        """
    )
    return


@app.cell
def _(mo, spieler_schlecht):
    _df = mo.sql(
        f"""
        -- 🔵 Schreiben Sie Ihre Abfrage:
        SELECT 'Ihre Lösung hier' AS Hinweis;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    COUNT(*) AS Gesamtzeilen,
    COUNT(DISTINCT Verein) AS Verschiedene_Vereine,
    COUNT(*) - COUNT(DISTINCT Verein) AS Redundante_Vereinseinträge
FROM spieler_schlecht
```

**Ergebnis:** 10 Gesamtzeilen, 3 verschiedene Vereine, also **7 redundante** Vereinseinträge. Das bedeutet: 70% der Vereinsinformationen sind überflüssig gespeichert!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 2.4: Fehlende GROUP BY

        Die folgende Abfrage hat einen Fehler. Finden und beheben Sie ihn:
        """
    )
    return


@app.cell
def _(mo, spieler_schlecht):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT Verein, COUNT(DISTINCT Vereinsort) AS Verschiedene_Orte
        FROM spieler_schlecht
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** Es fehlt `GROUP BY Verein`! Ohne `GROUP BY` weiß SQL nicht, für welchen Verein die Zählung gelten soll.

**Korrektur:**
```sql
SELECT Verein, COUNT(DISTINCT Vereinsort) AS Verschiedene_Orte
FROM spieler_schlecht
GROUP BY Verein
```

**Merke:** Sobald Sie eine Aggregatfunktion (`COUNT`, `SUM`, ...) zusammen mit einer normalen Spalte verwenden, brauchen Sie `GROUP BY` für die normale Spalte.
""")})
    return


# ============================================================
# Phase 4: Anomalien erleben
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 4: Anomalien erleben

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.1: Änderungsanomalie erleben

        **Szenario:** Bayern München baut ein neues Stadion namens "FC Bayern Arena".
        Wir führen ein Update durch — aber "vergessen" absichtlich einen Spieler (Musiala):
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
        **Inkonsistenz!** Musiala spielt noch in der "Allianz Arena",
        alle anderen Bayern-Spieler in der "FC Bayern Arena".

        Prüfen Sie die Inkonsistenz mit einer Abfrage:
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
        ### 🟡 Aufgabe 4.2: Normalisierte Tabelle prüfen

        Prüfen Sie: Gibt es in der normalisierten `vereine`-Tabelle noch Redundanz?
        Ergänzen Sie die `???`:
        """
    )
    return


@app.cell
def _(mo, vereine):
    _df = mo.sql(
        f"""
        -- Prüfen: Gibt es in der normalisierten Tabelle noch Redundanz?
        SELECT
            COUNT(*) AS Vereine_Gesamt,
            COUNT(DISTINCT ???) AS Verschiedene_Vereine
        FROM vereine
        -- Tipp: Was sollte gleich sein wenn keine Redundanz?
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    COUNT(*) AS Vereine_Gesamt,
    COUNT(DISTINCT Verein) AS Verschiedene_Vereine
FROM vereine
```

**Ergebnis:** Beide Werte sind **3 = 3** — keine Redundanz! Jeder Verein existiert genau einmal in der normalisierten Tabelle.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.3: JOIN über normalisierte Tabellen

        Kombinieren Sie `spieler_gut` und `vereine` per JOIN, um Spieler mit ihrem
        Vereinsnamen und Stadion anzuzeigen.

        **Hinweis:** Verbinden Sie über `Verein_ID` und sortieren Sie nach Verein und Spieler.
        """
    )
    return


@app.cell
def _(mo, spieler_gut, vereine):
    _df = mo.sql(
        f"""
        -- 🔵 Schreiben Sie Ihre JOIN-Abfrage:
        SELECT 'Ihre Lösung hier' AS Hinweis;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT s.Spieler, s.Position, v.Verein, v.Stadion
FROM spieler_gut s
JOIN vereine v ON s.Verein_ID = v.Verein_ID
ORDER BY v.Verein, s.Spieler
```

**Erklärung:** Der JOIN kombiniert die beiden Tabellen über den gemeinsamen Schlüssel `Verein_ID`. Die Daten sind getrennt gespeichert (keine Redundanz), können aber jederzeit wieder zusammengeführt werden.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 4.4: Falsche JOIN-Spalte

        Die folgende Abfrage hat einen Fehler im JOIN. Finden und beheben Sie ihn:
        """
    )
    return


@app.cell
def _(mo, spieler_gut, vereine):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT s.Spieler, v.Verein, v.Stadion
        FROM spieler_gut s
        JOIN vereine v ON s.Spieler_ID = v.Verein_ID
        ORDER BY v.Verein
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** `s.Spieler_ID = v.Verein_ID` verbindet die **falschen** Spalten! Die `Spieler_ID` ist der Primärschlüssel des Spielers und hat nichts mit dem Verein zu tun.

**Korrektur:**
```sql
SELECT s.Spieler, v.Verein, v.Stadion
FROM spieler_gut s
JOIN vereine v ON s.Verein_ID = v.Verein_ID
ORDER BY v.Verein
```

**Merke:** Beim JOIN muss der **Fremdschlüssel** (`s.Verein_ID`) mit dem **Primärschlüssel** (`v.Verein_ID`) der referenzierten Tabelle verbunden werden.
""")})
    return


# ============================================================
# Phase 6: ER-Modellierung
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 6: ER-Modellierung

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.1: Kardinalitäten bestimmen

        Bestimmen Sie für jedes Szenario die richtige Kardinalität (1:1, 1:N, oder M:N):
        """
    )
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
        mo.output.replace(mo.md("Richtig! Co-Autoren und Vielschreiber — M:N!"))
    elif quiz4.value:
        mo.output.replace(mo.md("Nicht ganz. Denken Sie an Co-Autoren: Ein Buch kann *mehrere* Autoren haben."))
    return


@app.cell(hide_code=True)
def _(mo):
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
    mo.md(
        r"""
        ### 🟡 Aufgabe 6.2: ER-Diagramm ergänzen

        Betrachten Sie das folgende ER-Diagramm für unsere Fußball-Daten.
        Die Kardinalität Verein-Spieler ist bereits eingetragen (`||--|{` = 1:N).

        **Frage:** Warum ist die Beziehung 1:N und nicht M:N?
        """
    )
    return


@app.cell
def _(mo):
    mo.mermaid("""
erDiagram
    VEREIN ||--|{ SPIELER : hat
    VEREIN {
        int ID PK
        string Name
        string Ort
    }
    SPIELER {
        int ID PK
        string Name
        string Position
        int Verein_ID FK
    }
""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Erklärung:** Die Beziehung ist **1:N**, weil jeder Spieler zu genau **einem** Verein gehört,
        aber ein Verein **viele** Spieler haben kann. In der Crow's-Foot-Notation zeigt `||--|{`:
        - `||` (linke Seite) = genau eins (ein Spieler hat einen Verein)
        - `|{` (rechte Seite) = eins oder mehr (ein Verein hat viele Spieler)

        Der **Fremdschlüssel** `Verein_ID` steht in der Spieler-Tabelle (N-Seite), weil jeder
        Spieler auf seinen einen Verein verweist.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.3: Bibliotheks-ER entwerfen

        Entwerfen Sie ein ER-Diagramm für eine einfache Bibliothek mit:

        - **Bücher** (ISBN, Titel)
        - **Autoren** (Name)
        - **Studierende** (MatrikelNr, Name)

        **Beziehungen:**
        - Autor **schreibt** Buch (M:N — Co-Autoren möglich)
        - Studierender **leiht aus** Buch (M:N — mehrere Bücher gleichzeitig)

        Erstellen Sie das Diagramm mit `mo.mermaid()`:
        """
    )
    return


@app.cell
def _(mo):
    # 🔵 Entwerfen Sie Ihr ER-Diagramm hier:
    mo.md("*Ersetzen Sie diese Zelle durch Ihr `mo.mermaid()`-Diagramm.*")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```python
mo.mermaid(\"\"\"
erDiagram
    AUTOR }|--|{ BUCH : schreibt
    STUDIERENDER }|--o{ AUSLEIHE : leiht
    BUCH ||--o{ AUSLEIHE : "wird ausgeliehen"

    BUCH {
        string ISBN PK
        string Titel
    }
    AUTOR {
        int ID PK
        string Name
    }
    STUDIERENDER {
        int MatrikelNr PK
        string Name
    }
    AUSLEIHE {
        string ISBN FK
        int MatrikelNr FK
        date Ausleihdatum
        date Rueckgabedatum
    }
\"\"\")
```

**Beobachtungen:**
- **Autor-Buch** ist M:N (Co-Autoren, Vielschreiber) — benötigt eine eigene Beziehungstabelle
- **Studierender-Buch** ist M:N mit Attributen (Datum) — aufgelöst durch die Ausleihe-Tabelle
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.4: Entitäten aus Textbeschreibung identifizieren

        Lesen Sie die folgende Beschreibung und identifizieren Sie:
        1. Welche **Entitäten** gibt es?
        2. Welche **Beziehungen** bestehen?
        3. Welche **Kardinalitäten** haben diese?

        ---

        **Szenario: Fußball-Liga**

        *"In einer Fußball-Liga spielen mehrere Vereine. Jeder Verein hat einen Namen,
        einen Ort und ein Gründungsjahr. Spieler gehören zu einem Verein und haben
        einen Namen, eine Position und ein Geburtsdatum. Vereine spielen Spiele
        gegeneinander, wobei jedes Spiel an einem bestimmten Datum stattfindet
        und ein Ergebnis (Tore Heim, Tore Gast) hat."*

        ---

        Notieren Sie Ihre Lösung:
        """
    )
    return


@app.cell
def _(mo):
    # 🔵 Notieren Sie hier Ihre Entitäten, Beziehungen und Kardinalitäten:
    mo.md("*Ersetzen Sie diese Zelle durch Ihre Analyse.*")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "🔑 Musterlösung": mo.md(r"""
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
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.5: 1:N falsch als M:N modelliert

        Ein Kollege modelliert "Person besitzt Personalausweis" als M:N-Beziehung
        mit einer eigenen Beziehungstabelle. Was ist daran falsch?
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 🔴 Ein Kollege modelliert "Person besitzt Personalausweis" als M:N.
        -- Was ist daran falsch?
        SELECT 'Person-Ausweis ist 1:1, nicht M:N!' AS Problem,
               'Jede Person hat genau EINEN Ausweis' AS Erklärung
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** Die Beziehung Person-Personalausweis ist **1:1**, nicht M:N!

- Jede Person hat **genau einen** Personalausweis
- Jeder Personalausweis gehört zu **genau einer** Person

**Problem bei M:N-Modellierung:**
- Eine unnötige **Beziehungstabelle** wird erstellt (verschwendeter Speicher)
- Das Modell erlaubt fälschlicherweise, dass eine Person *mehrere* Ausweise hat
- Die Datenintegrität ist nicht korrekt abgebildet

**Richtige Modellierung:** 1:1 — entweder die Tabellen zusammenlegen oder einen Fremdschlüssel mit `UNIQUE`-Constraint verwenden.
""")})
    return


# ============================================================
# Exploration
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration — Herausforderungen
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Neuer Verein per INSERT + LEFT JOIN

        Im normalisierten Design können Sie einen neuen Verein hinzufügen, der noch
        keine Spieler hat. Zeigen Sie mit einem `LEFT JOIN`, dass der Verein trotzdem
        in der Datenbank existiert (Anzahl_Spieler = 0).
        """
    )
    return


@app.cell
def _(mo, spieler_gut, vereine):
    _df = mo.sql(
        f"""
        -- ⭐ Neuer Verein ohne Spieler prüfen:
        SELECT 'Ihre Lösung hier' AS Hinweis;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
-- In der normalisierten Vereine-Tabelle existieren alle Vereine unabhängig
SELECT v.Verein, COUNT(s.Spieler_ID) AS Anzahl_Spieler
FROM vereine v
LEFT JOIN spieler_gut s ON v.Verein_ID = s.Verein_ID
GROUP BY v.Verein
ORDER BY Anzahl_Spieler
```

**Erklärung:** Der `LEFT JOIN` zeigt alle Vereine — auch solche ohne Spieler. In der Mega-Tabelle wäre ein Verein ohne Spieler gar nicht speicherbar (Einfügeanomalie!). Das normalisierte Design löst dieses Problem elegant.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐ ER-Diagramm für Spotify

        Entwerfen Sie ein ER-Diagramm für einen Musik-Streaming-Dienst mit:
        **Künstler**, **Album**, **Song**, **Playlist**, **User**

        Überlegen Sie: Welche Beziehungen sind 1:N, welche M:N?
        """
    )
    return


@app.cell
def _(mo):
    # ⭐⭐ Entwerfen Sie Ihr Spotify-ER-Diagramm:
    mo.md("*Ersetzen Sie diese Zelle durch Ihr `mo.mermaid()`-Diagramm.*")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```python
mo.mermaid(\"\"\"
erDiagram
    KUENSTLER ||--|{ ALBUM : veroeffentlicht
    ALBUM ||--|{ SONG : enthaelt
    KUENSTLER }|--|{ SONG : "wirkt mit"
    USER ||--o{ PLAYLIST : erstellt
    PLAYLIST }|--|{ SONG : enthaelt

    KUENSTLER {
        int ID PK
        string Name
        string Genre
    }
    ALBUM {
        int ID PK
        string Titel
        date Erscheinungsdatum
        int Kuenstler_ID FK
    }
    SONG {
        int ID PK
        string Titel
        int Dauer_Sekunden
        int Album_ID FK
    }
    USER {
        int ID PK
        string Username
        string Email
    }
    PLAYLIST {
        int ID PK
        string Name
        int User_ID FK
    }
\"\"\")
```

**Beziehungen:**
- **Künstler → Album**: 1:N (ein Künstler hat viele Alben)
- **Album → Song**: 1:N (ein Album enthält viele Songs)
- **Künstler ↔ Song**: M:N (Features/Kollaborationen)
- **User → Playlist**: 1:N (ein User erstellt viele Playlists)
- **Playlist ↔ Song**: M:N (ein Song kann in vielen Playlists sein)
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐⭐ ER für Uni-Kurssystem mit (Min,Max)-Notation

        Entwerfen Sie ein ER-Modell für ein Universitäts-Kurssystem.
        Verwenden Sie die **(Min,Max)-Notation** für präzise Kardinalitäten:

        - **Professor** hält Kurse: (0,N) — ein Professor kann 0 bis N Kurse halten
        - **Kurs** hat Professor: (1,1) — jeder Kurs hat genau einen Professor
        - **Student** besucht Kurse: (0,N) — ein Student kann 0 bis N Kurse besuchen
        - **Kurs** hat Studenten: (5,300) — mindestens 5, maximal 300 Teilnehmer
        - **Raum** wird Kurs zugeordnet: (0,N) — ein Raum kann für mehrere Kurse genutzt werden
        - **Kurs** findet in Raum statt: (1,1) — jeder Kurs hat genau einen Raum

        Notieren Sie die Entitäten, Beziehungen und (Min,Max)-Angaben:
        """
    )
    return


@app.cell
def _(mo):
    # ⭐⭐⭐ Entwerfen Sie Ihr Uni-Kurssystem-ER:
    mo.md("*Ersetzen Sie diese Zelle durch Ihre Lösung.*")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
**Entitäten:**
- **Professor** (PersNr PK, Name, Fachgebiet)
- **Kurs** (KursNr PK, Titel, SWS)
- **Student** (MatrikelNr PK, Name, Studiengang)
- **Raum** (RaumNr PK, Gebäude, Kapazität)

**Beziehungen mit (Min,Max)-Notation:**

| Beziehung | Entität A | (Min,Max) A | Entität B | (Min,Max) B |
|-----------|-----------|-------------|-----------|-------------|
| hält | Professor | (0,N) | Kurs | (1,1) |
| besucht | Student | (0,N) | Kurs | (5,300) |
| findet statt in | Kurs | (1,1) | Raum | (0,N) |

**Erklärung der (Min,Max)-Werte:**
- Professor (0,N): Ein Professor kann im Forschungssemester 0 Kurse halten
- Kurs (1,1): Jeder Kurs braucht genau einen verantwortlichen Professor
- Student (0,N): Erstsemester können sich noch in keinen Kurs eingeschrieben haben
- Kurs (5,300): Mindestteilnehmerzahl 5, Hörsaalkapazität 300
- Kurs (1,1): Jeder Kurs braucht genau einen Raum
- Raum (0,N): Räume können ungenutzt sein oder mehrfach belegt werden
""")})
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

        ### Teil 1: Redundanz und Anomalien

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

        **Nächste Session:** ER → SQL (CREATE TABLE)
        """
    )
    return


if __name__ == "__main__":
    app.run()
