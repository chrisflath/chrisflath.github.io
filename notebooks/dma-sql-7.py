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
    app_title="DMA Session 7: ER → SQL",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _():
    import polars as pl
    import plotly.express as px
    return pl, px


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 7: Relationales Modell & Transformation

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · **▸ II: Datenmodellierung (S5–8)** · III: Fortgeschrittenes SQL (S9–10) · IV: Datenanalyse (S11–14)

        In dieser Session lernen Sie:

        - Das **relationale Modell** (Tabellen, Zeilen, Spalten)
        - **Primärschlüssel** und **Fremdschlüssel**
        - **Transformationsregeln**: ER → Relationales Schema
        - **CREATE TABLE** in SQL

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Das Relationale Modell

        | Begriff | Bedeutung | SQL-Äquivalent |
        |---------|-----------|----------------|
        | **Relation** | Tabelle | TABLE |
        | **Tupel** | Zeile/Datensatz | ROW |
        | **Attribut** | Spalte | COLUMN |
        | **Domäne** | Wertebereich | Datentyp (INT, VARCHAR, ...) |

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Transformationsregeln: Übersicht

        | ER-Element | → Relationales Modell |
        |------------|----------------------|
        | Entität | Tabelle |
        | Attribut | Spalte |
        | Schlüsselattribut | PRIMARY KEY |
        | **1:N-Beziehung** | Fremdschlüssel auf N-Seite |
        | **M:N-Beziehung** | Beziehungstabelle mit 2 FKs |
        | **1:1-Beziehung** | Zusammenlegen oder FK |

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
## Aufgabe 7.1: 1:N-Beziehung → SQL

> **Vorhersage:** Bei einer 1:N-Beziehung (ein Verein hat viele Spieler) — auf welcher Seite wird der Fremdschlüssel stehen? Beim Verein oder beim Spieler? Überlegen Sie, bevor Sie weiterscrollen.

**Gegeben:** Verein (1) ← hat → Spieler (N)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
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
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
**Aufgabe:** Ergänzen Sie das CREATE TABLE für Spieler mit dem Fremdschlüssel.
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Zuerst: Verein-Tabelle (bereits vollständig)
        CREATE TABLE IF NOT EXISTS Verein (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Ort VARCHAR(50)
        );

        -- Beispieldaten
        INSERT OR IGNORE INTO Verein VALUES (1, 'Bayern München', 'München');
        INSERT OR IGNORE INTO Verein VALUES (2, 'Bayer Leverkusen', 'Leverkusen');
        INSERT OR IGNORE INTO Verein VALUES (3, 'Borussia Dortmund', 'Dortmund');

        SELECT * FROM Verein;
        """
    )
    return


@app.cell
def _(mo):
    # Aufgabe: Fremdschlüssel verstehen
    _df = mo.sql(
        f"""
        -- Spieler-Tabelle mit Fremdschlüssel zu Verein
        CREATE TABLE IF NOT EXISTS Spieler (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Position VARCHAR(50),
            Verein_ID INTEGER,
            FOREIGN KEY (Verein_ID) REFERENCES Verein(ID)
        );

        -- Beispieldaten
        INSERT OR IGNORE INTO Spieler VALUES (1, 'Müller', 'Sturm', 1);
        INSERT OR IGNORE INTO Spieler VALUES (2, 'Neuer', 'Tor', 1);
        INSERT OR IGNORE INTO Spieler VALUES (3, 'Wirtz', 'Mittelfeld', 2);
        INSERT OR IGNORE INTO Spieler VALUES (4, 'Bellingham', 'Mittelfeld', 3);

        SELECT s.Name, s.Position, v.Name AS Verein
        FROM Spieler s
        JOIN Verein v ON s.Verein_ID = v.ID;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_fk = mo.ui.radio(
        options={
            "correct": "Auf der N-Seite (Spieler) — jeder Spieler verweist auf seinen Verein",
            "parent": "Auf der 1-Seite (Verein) — der Verein verweist auf seine Spieler",
            "both": "In beiden Tabellen — eine Referenz in jede Richtung",
            "join": "In einer separaten Join-Tabelle",
        },
        label="**Quiz:** Bei einer 1:N-Beziehung (Verein → Spieler) — auf welcher Seite steht der Fremdschlüssel?"
    )
    quiz_fk
    return (quiz_fk,)


@app.cell(hide_code=True)
def _(quiz_fk, mo):
    if quiz_fk.value == "correct":
        mo.output.replace(mo.md("Richtig! Der Fremdschlüssel steht immer auf der **N-Seite**. Jeder Spieler gehört zu *einem* Verein, also speichert die Spieler-Tabelle die `Verein_ID`. Der Verein selbst muss nicht wissen, welche Spieler er hat — das ergibt sich durch den JOIN."))
    elif quiz_fk.value:
        mo.output.replace(mo.md("Nicht ganz. Überlegen Sie: Kann ein Verein auf *alle* seine Spieler verweisen? Das wäre eine variable Anzahl! Stattdessen verweist jeder **einzelne Spieler** auf seinen (einen) Verein — der FK steht auf der N-Seite."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
---

## Aufgabe 7.2: M:N-Beziehung → SQL

**Gegeben:** Student (M) ← besucht → Kurs (N) mit Beziehungsattribut **Note**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
        erDiagram
            STUDENT ||--o{ STUDENT_KURS : besucht
            KURS ||--o{ STUDENT_KURS : "wird besucht"

            STUDENT {
                int ID PK
                string Name
            }

            KURS {
                int ID PK
                string Titel
            }

            STUDENT_KURS {
                int Student_ID PK,FK
                int Kurs_ID PK,FK
                decimal Note
            }
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
**Aufgabe:** Erstellen Sie die Beziehungstabelle `Student_Kurs`.
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Entitätstabellen
        CREATE TABLE IF NOT EXISTS Student (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Kurs (
            ID INTEGER PRIMARY KEY,
            Titel VARCHAR(200) NOT NULL
        );

        -- Beispieldaten
        INSERT OR IGNORE INTO Student VALUES (1, 'Anna');
        INSERT OR IGNORE INTO Student VALUES (2, 'Ben');
        INSERT OR IGNORE INTO Student VALUES (3, 'Clara');

        INSERT OR IGNORE INTO Kurs VALUES (101, 'Datenmanagement');
        INSERT OR IGNORE INTO Kurs VALUES (102, 'BWL');
        INSERT OR IGNORE INTO Kurs VALUES (103, 'Statistik');

        SELECT 'Studenten:' AS Info;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT * FROM Student;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT * FROM Kurs;
        """
    )
    return


@app.cell
def _(mo):
    # Beziehungstabelle für M:N
    _df = mo.sql(
        f"""
        -- Beziehungstabelle: Zusammengesetzter Primärschlüssel!
        CREATE TABLE IF NOT EXISTS Student_Kurs (
            Student_ID INTEGER,
            Kurs_ID INTEGER,
            Note DECIMAL(2,1),
            PRIMARY KEY (Student_ID, Kurs_ID),
            FOREIGN KEY (Student_ID) REFERENCES Student(ID),
            FOREIGN KEY (Kurs_ID) REFERENCES Kurs(ID)
        );

        -- Beispieldaten: Wer besucht welchen Kurs?
        INSERT OR IGNORE INTO Student_Kurs VALUES (1, 101, 1.3);  -- Anna besucht DMA
        INSERT OR IGNORE INTO Student_Kurs VALUES (1, 102, 2.0);  -- Anna besucht BWL
        INSERT OR IGNORE INTO Student_Kurs VALUES (2, 101, 1.7);  -- Ben besucht DMA
        INSERT OR IGNORE INTO Student_Kurs VALUES (3, 101, 1.0);  -- Clara besucht DMA
        INSERT OR IGNORE INTO Student_Kurs VALUES (3, 103, 1.3);  -- Clara besucht Statistik

        -- Abfrage: Wer besucht welchen Kurs mit welcher Note?
        SELECT s.Name AS Student, k.Titel AS Kurs, sk.Note
        FROM Student_Kurs sk
        JOIN Student s ON sk.Student_ID = s.ID
        JOIN Kurs k ON sk.Kurs_ID = k.ID
        ORDER BY s.Name, k.Titel;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
---

## Aufgabe 7.3: Online-Shop

Komplettes ER-Modell mit 1:N und M:N Beziehungen:
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
**Aufgabe:** Erstellen Sie alle CREATE TABLE-Statements in der richtigen Reihenfolge!
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 1. Kategorie (keine Abhängigkeiten)
        CREATE TABLE IF NOT EXISTS Kategorie (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL
        );

        INSERT OR IGNORE INTO Kategorie VALUES (1, 'Elektronik');
        INSERT OR IGNORE INTO Kategorie VALUES (2, 'Kleidung');
        INSERT OR IGNORE INTO Kategorie VALUES (3, 'Bücher');

        SELECT * FROM Kategorie;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 2. Produkt (FK zu Kategorie)
        CREATE TABLE IF NOT EXISTS Produkt (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(200) NOT NULL,
            Preis DECIMAL(10,2) NOT NULL,
            Kategorie_ID INTEGER,
            FOREIGN KEY (Kategorie_ID) REFERENCES Kategorie(ID)
        );

        INSERT OR IGNORE INTO Produkt VALUES (1, 'Laptop', 999.99, 1);
        INSERT OR IGNORE INTO Produkt VALUES (2, 'T-Shirt', 29.99, 2);
        INSERT OR IGNORE INTO Produkt VALUES (3, 'SQL-Handbuch', 49.99, 3);
        INSERT OR IGNORE INTO Produkt VALUES (4, 'Smartphone', 599.99, 1);

        SELECT p.Name, p.Preis, k.Name AS Kategorie
        FROM Produkt p
        JOIN Kategorie k ON p.Kategorie_ID = k.ID;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 3. Kunde
        CREATE TABLE IF NOT EXISTS Kunde (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Email VARCHAR(200) UNIQUE
        );

        INSERT OR IGNORE INTO Kunde VALUES (1, 'Max Mustermann', 'max@example.com');
        INSERT OR IGNORE INTO Kunde VALUES (2, 'Erika Musterfrau', 'erika@example.com');

        SELECT * FROM Kunde;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 4. Bestellung (FK zu Kunde)
        CREATE TABLE IF NOT EXISTS Bestellung (
            ID INTEGER PRIMARY KEY,
            Datum DATE NOT NULL,
            Kunde_ID INTEGER,
            FOREIGN KEY (Kunde_ID) REFERENCES Kunde(ID)
        );

        INSERT OR IGNORE INTO Bestellung VALUES (1, '2026-01-15', 1);
        INSERT OR IGNORE INTO Bestellung VALUES (2, '2026-01-20', 1);
        INSERT OR IGNORE INTO Bestellung VALUES (3, '2026-01-22', 2);

        SELECT b.ID AS Bestellung, b.Datum, k.Name AS Kunde
        FROM Bestellung b
        JOIN Kunde k ON b.Kunde_ID = k.ID;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 5. Bestellposition (M:N zwischen Bestellung und Produkt)
        CREATE TABLE IF NOT EXISTS Bestellposition (
            Bestellung_ID INTEGER,
            Produkt_ID INTEGER,
            Menge INTEGER NOT NULL DEFAULT 1,
            PRIMARY KEY (Bestellung_ID, Produkt_ID),
            FOREIGN KEY (Bestellung_ID) REFERENCES Bestellung(ID),
            FOREIGN KEY (Produkt_ID) REFERENCES Produkt(ID)
        );

        INSERT OR IGNORE INTO Bestellposition VALUES (1, 1, 1);  -- Bestellung 1: 1x Laptop
        INSERT OR IGNORE INTO Bestellposition VALUES (1, 3, 2);  -- Bestellung 1: 2x SQL-Handbuch
        INSERT OR IGNORE INTO Bestellposition VALUES (2, 4, 1);  -- Bestellung 2: 1x Smartphone
        INSERT OR IGNORE INTO Bestellposition VALUES (3, 2, 3);  -- Bestellung 3: 3x T-Shirt

        -- Vollständige Bestellübersicht
        SELECT
            b.ID AS Bestellung,
            k.Name AS Kunde,
            p.Name AS Produkt,
            bp.Menge,
            p.Preis * bp.Menge AS Summe
        FROM Bestellposition bp
        JOIN Bestellung b ON bp.Bestellung_ID = b.ID
        JOIN Kunde k ON b.Kunde_ID = k.ID
        JOIN Produkt p ON bp.Produkt_ID = p.ID
        ORDER BY b.ID, p.Name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ### Analyse: Umsatz pro Kategorie

        Jetzt sehen wir den Vorteil der normalisierten Struktur: Analysen über
        mehrere Tabellen hinweg.
        """
    )
    return


@app.cell
def _(mo, px):
    _umsatz = mo.sql(
        f"""
        SELECT
            k.Name AS Kategorie,
            SUM(p.Preis * bp.Menge) AS Umsatz
        FROM Bestellposition bp
        JOIN Produkt p ON bp.Produkt_ID = p.ID
        JOIN Kategorie k ON p.Kategorie_ID = k.ID
        GROUP BY k.Name
        ORDER BY Umsatz DESC
        """
    )
    px.bar(
        _umsatz,
        x="Kategorie",
        y="Umsatz",
        color="Kategorie",
        title="Umsatz pro Produktkategorie",
        labels={"Umsatz": "Umsatz (€)", "Kategorie": ""},
        color_discrete_sequence=["#003560", "#E87722", "#5B9BD5"],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Diese Analyse wäre mit einer einzigen flachen Tabelle *möglich* gewesen --
        aber anfällig für Inkonsistenzen. Das normalisierte Schema garantiert, dass
        jeder Preis und jede Kategorie genau einmal definiert ist.

        ---

        ### Datenverteilung über Tabellen
        """
    )
    return


@app.cell
def _(mo):
    _zeilen = mo.sql(
        f"""
        SELECT 'Kategorie' AS Tabelle, COUNT(*) AS Zeilen FROM Kategorie
        UNION ALL
        SELECT 'Produkt', COUNT(*) FROM Produkt
        UNION ALL
        SELECT 'Kunde', COUNT(*) FROM Kunde
        UNION ALL
        SELECT 'Bestellung', COUNT(*) FROM Bestellung
        UNION ALL
        SELECT 'Bestellposition', COUNT(*) FROM Bestellposition
        ORDER BY Zeilen DESC
        """
    )
    return (_zeilen,)


@app.cell
def _(_zeilen, px):
    px.bar(
        _zeilen,
        x="Tabelle",
        y="Zeilen",
        title="Zeilenanzahl pro Tabelle im Online-Shop-Schema",
        labels={"Zeilen": "Anzahl Zeilen", "Tabelle": ""},
        color_discrete_sequence=["#003560"],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Erkenntnis:** Entitätstabellen (Kategorie, Kunde) haben typischerweise weniger Zeilen
        als Beziehungstabellen (Bestellposition) oder Transaktionstabellen (Bestellung).
        Die M:N-Auflösungstabelle Bestellposition wächst am schnellsten -- das ist normal!

        ---

        ## Aufgabe 7.4: Referentielle Integrität

        Was passiert, wenn wir versuchen, einen referenzierten Datensatz zu löschen?
        """
    )
    return


@app.cell
def _(mo):
    # Test: Was passiert bei Löschung?
    _df = mo.sql(
        f"""
        -- Versuch: Kategorie löschen, die noch Produkte hat
        -- Dies würde normalerweise einen Fehler verursachen!

        -- DuckDB prüft Foreign Keys automatisch

        -- Zeige Produkte in Kategorie 'Elektronik':
        SELECT p.Name, k.Name AS Kategorie
        FROM Produkt p
        JOIN Kategorie k ON p.Kategorie_ID = k.ID
        WHERE k.Name = 'Elektronik';
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Referentielle Integrität:**

        | Option | SQL | Bedeutung |
        |--------|-----|-----------|
        | Verbieten | `RESTRICT` | Löschung wird abgelehnt |
        | Kaskadieren | `CASCADE` | Abhängige Zeilen werden mitgelöscht |
        | NULL setzen | `SET NULL` | FK wird auf NULL gesetzt |

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Aufgabe 7.5: Fremdschlüssel als Schutzwall

        Versuchen Sie, einen Spieler mit einem nicht existierenden Verein einzufügen.
        Was passiert?
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Versuch: Spieler mit Verein_ID 999 einfügen (existiert nicht!)
        -- In einer Datenbank mit erzwungenen FK-Constraints würde das scheitern:
        --   INSERT INTO Spieler VALUES (99, 'Test', 'Sturm', 999);
        --   → ERROR: Foreign key constraint violated

        -- Zeigen wir die existierenden Vereine:
        SELECT ID, Name FROM Verein;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Erkenntnis:** Der Fremdschlüssel-Constraint verhindert, dass wir auf
        nicht existierende Datensätze verweisen. Das schützt die **referentielle
        Integrität** -- jeder Verweis zeigt auf einen echten Datensatz.

        Ohne diesen Schutz könnten Spieler zu "Geistervereinen" gehören!

        ---

        ## Freie Exploration

        Probieren Sie eigene Abfragen auf den erstellten Tabellen!

        **Ideen:**
        - Welcher Kunde hat die meisten Bestellungen?
        - Welches Produkt wurde am häufigsten bestellt?
        - Wie hoch ist der Gesamtumsatz?
        """
    )
    return


@app.cell
def _(mo, px):
    _bestellungen_pro_kunde = mo.sql(
        f"""
        SELECT
            k.Name AS Kunde,
            COUNT(b.ID) AS Bestellungen
        FROM Kunde k
        LEFT JOIN Bestellung b ON k.ID = b.Kunde_ID
        GROUP BY k.Name
        ORDER BY Bestellungen DESC
        """
    )
    px.bar(
        _bestellungen_pro_kunde,
        x="Kunde",
        y="Bestellungen",
        color="Kunde",
        title="Bestellungen pro Kunde (LEFT JOIN zeigt auch Kunden ohne Bestellung)",
        labels={"Bestellungen": "Anzahl Bestellungen", "Kunde": ""},
        color_discrete_sequence=["#003560", "#E87722"],
    )
    return


@app.cell
def _(mo):
    # Ihre Abfrage hier:
    _df = mo.sql(
        f"""
        -- Beispiel: Welches Produkt wurde am häufigsten bestellt?
        SELECT
            p.Name AS Produkt,
            SUM(bp.Menge) AS Gesamtmenge
        FROM Bestellposition bp
        JOIN Produkt p ON bp.Produkt_ID = p.ID
        GROUP BY p.Name
        ORDER BY Gesamtmenge DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung: Gesamtumsatz": mo.md("""
```sql
SELECT
    SUM(p.Preis * bp.Menge) AS Gesamtumsatz
FROM Bestellposition bp
JOIN Produkt p ON bp.Produkt_ID = p.ID;
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Transformation | Regel |
        |---------------|-------|
        | **1:N** | Fremdschlüssel auf der N-Seite |
        | **M:N** | Beziehungstabelle mit 2 Fremdschlüsseln |
        | **1:1** | Zusammenlegen oder FK |

        **SQL-Syntax:**
        ```sql
        CREATE TABLE Name (
            ID INTEGER PRIMARY KEY,
            Attribut DATENTYP [CONSTRAINT],
            FK_ID INTEGER,
            FOREIGN KEY (FK_ID) REFERENCES AndereTabelle(ID)
        );
        ```

        **Nächste Session:** Normalisierung (1NF, 2NF, 3NF)
        """
    )
    return


if __name__ == "__main__":
    app.run()
