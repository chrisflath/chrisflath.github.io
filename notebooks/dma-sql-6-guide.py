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
    app_title="DMA Session 6: ER → SQL — Guide",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 6: ER → SQL — Guide

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · **▸ II: Datenmodellierung (S5–7)** · III: Fortgeschrittenes SQL (S8–9) · IV: Datenanalyse (S10–13)

        ### Lernziele

        Nach dieser Session können Sie:

        - Das **relationale Modell** beschreiben (Relation, Tupel, Attribut, Domäne)
        - **Primärschlüssel** und **Fremdschlüssel** erklären
        - **Transformationsregeln** von ER → SQL anwenden (1:N, M:N, 1:1)
        - Die richtige **CREATE TABLE Reihenfolge** bestimmen

        ---
        """
    )
    return


# ============================================================
# Phase 1: Relationales Modell + 1:N Transformation
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 1: Relationales Modell + 1:N Transformation

        ### Das Relationale Modell

        Edgar F. Codd formulierte 1970 das relationale Modell — die theoretische
        Grundlage aller SQL-Datenbanken. Die zentralen Begriffe:

        | Formaler Begriff | Bedeutung | SQL-Äquivalent |
        |------------------|-----------|----------------|
        | **Relation** | Tabelle | `TABLE` |
        | **Tupel** | Zeile / Datensatz | `ROW` |
        | **Attribut** | Spalte / Eigenschaft | `COLUMN` |
        | **Domäne** | Wertebereich eines Attributs | Datentyp (`INT`, `VARCHAR`, ...) |

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Transformationsregeln: Übersicht

        Wie wird ein ER-Diagramm in SQL-Tabellen überführt?

        | ER-Element | → Relationales Modell |
        |------------|----------------------|
        | Entität | Tabelle (`CREATE TABLE`) |
        | Attribut | Spalte |
        | Schlüsselattribut | `PRIMARY KEY` |
        | **1:N-Beziehung** | Fremdschlüssel auf der N-Seite |
        | **M:N-Beziehung** | Beziehungstabelle mit 2 Fremdschlüsseln |
        | **1:1-Beziehung** | Zusammenlegen oder Fremdschlüssel |

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 1:N-Beziehung: Verein → Spieler

        Ein Verein hat **viele** Spieler, aber jeder Spieler gehört zu **einem** Verein.
        Das ist eine klassische 1:N-Beziehung.
        """
    )
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
    ### Vorhersage 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_fk = mo.ui.radio(
        options={
            "n_seite": "Auf der N-Seite (Spieler) — jeder Spieler verweist auf seinen Verein",
            "1_seite": "Auf der 1-Seite (Verein) — der Verein listet seine Spieler",
            "beide": "In beiden Tabellen — eine Referenz in jede Richtung",
            "extra": "In einer separaten Beziehungstabelle",
        },
        label="**Vorhersage:** 1:N-Beziehung (Verein → Spieler) — wo steht der Fremdschlüssel?",
    )
    pred_fk
    return (pred_fk,)


@app.cell(hide_code=True)
def _(pred_fk, mo):
    if pred_fk.value == "n_seite":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Der Fremdschlüssel steht immer auf der **N-Seite**. "
                "Jeder Spieler gehört zu *einem* Verein, also speichert die Spieler-Tabelle "
                "die `Verein_ID`. Ein Verein kann nicht alle seine Spieler in einer einzigen Spalte auflisten — "
                "das wäre eine variable Anzahl!"
            )
        )
    elif pred_fk.value == "1_seite":
        mo.output.replace(
            mo.md(
                "❌ Nicht ganz. Wenn der Verein seine Spieler listen würde, bräuchte er "
                "eine variable Anzahl von Spalten (Spieler1_ID, Spieler2_ID, ...) — das ist nicht möglich. "
                "Stattdessen verweist jeder **einzelne Spieler** auf seinen Verein. "
                "Der FK steht auf der **N-Seite (Spieler)**."
            )
        )
    elif pred_fk.value == "beide":
        mo.output.replace(
            mo.md(
                "❌ Zwei Referenzen wären redundant. Es reicht, wenn jeder Spieler auf seinen "
                "Verein verweist — der Verein kann seine Spieler über einen JOIN finden. "
                "Der FK steht nur auf der **N-Seite (Spieler)**."
            )
        )
    elif pred_fk.value == "extra":
        mo.output.replace(
            mo.md(
                "❌ Eine separate Beziehungstabelle braucht man bei **M:N**-Beziehungen. "
                "Bei 1:N reicht ein Fremdschlüssel auf der **N-Seite (Spieler)** — "
                "das ist einfacher und effizienter."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ### Geführtes Beispiel 6.1: Verein-Tabelle anlegen

        Wir erstellen zuerst die **1-Seite** (Verein), da sie von niemandem referenziert werden muss, bevor sie existiert.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Verein (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Ort VARCHAR(50)
        );

        INSERT OR IGNORE INTO Verein VALUES (1, 'Bayern München', 'München');
        INSERT OR IGNORE INTO Verein VALUES (2, 'Bayer Leverkusen', 'Leverkusen');
        INSERT OR IGNORE INTO Verein VALUES (3, 'Borussia Dortmund', 'Dortmund');

        SELECT * FROM Verein;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Geführtes Beispiel 6.1b: Spieler-Tabelle mit Fremdschlüssel

        Jetzt die **N-Seite** (Spieler) mit dem Fremdschlüssel `Verein_ID`:
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Spieler (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Position VARCHAR(50),
            Verein_ID INTEGER,
            FOREIGN KEY (Verein_ID) REFERENCES Verein(ID)
        );

        INSERT OR IGNORE INTO Spieler VALUES (1, 'Müller', 'Sturm', 1);
        INSERT OR IGNORE INTO Spieler VALUES (2, 'Neuer', 'Tor', 1);
        INSERT OR IGNORE INTO Spieler VALUES (3, 'Wirtz', 'Mittelfeld', 2);
        INSERT OR IGNORE INTO Spieler VALUES (4, 'Bellingham', 'Mittelfeld', 3);

        SELECT * FROM Spieler;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 6.1c: JOIN — Spieler mit Vereinsnamen
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        SELECT s.Name AS Spieler, s.Position, v.Name AS Verein, v.Ort
        FROM Spieler s
        JOIN Verein v ON s.Verein_ID = v.ID
        ORDER BY v.Name, s.Name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Durch den Fremdschlüssel `Verein_ID` können wir die Tabellen
        wieder zusammenführen. Jeder Spieler verweist auf genau **einen** Verein —
        der JOIN stellt die Verbindung her.

        ---

        ### Probieren Sie selbst: CREATE TABLE anpassen

        Ändern Sie die Spieler-Tabelle! Probieren Sie z.B.:
        - Ein neues Attribut (z.B. `Trikotnummer INTEGER`)
        - Einen weiteren Spieler mit `INSERT`
        - Einen `NOT NULL` Constraint auf `Verein_ID`
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Probieren Sie Änderungen an der Tabelle:
        SELECT s.Name AS Spieler, s.Position, v.Name AS Verein
        FROM Spieler s
        JOIN Verein v ON s.Verein_ID = v.ID
        ORDER BY v.Name, s.Name;
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


# ============================================================
# Phase 3: M:N Beziehungen
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 3: M:N Beziehungen

        ### Warum reicht ein Fremdschlüssel nicht?

        Bei einer **M:N-Beziehung** kann jede Seite mit *mehreren* Einträgen der
        anderen Seite verknüpft sein. Ein einzelner Fremdschlüssel kann nur auf
        **einen** Eintrag verweisen — das reicht nicht.

        **Lösung:** Eine **Beziehungstabelle** (auch: Kreuztabelle, Junction Table)
        mit zwei Fremdschlüsseln und einem zusammengesetzten Primärschlüssel.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Beispiel: Student ↔ Kurs (M:N)

    Ein Student kann **mehrere Kurse** besuchen, und ein Kurs hat **mehrere Studenten**.
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
                int Student_ID PK_FK
                int Kurs_ID PK_FK
                decimal Note
            }
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
    pred_mn = mo.ui.radio(
        options={
            "0": "0",
            "1": "1",
            "2": "2",
            "3": "3",
        },
        label="**Vorhersage:** Wie viele Fremdschlüssel hat eine M:N-Beziehungstabelle mindestens?",
    )
    pred_mn
    return (pred_mn,)


@app.cell(hide_code=True)
def _(pred_mn, mo):
    if pred_mn.value == "2":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Jede M:N-Beziehungstabelle braucht mindestens **2 Fremdschlüssel** — "
                "einen für jede Seite der Beziehung. `Student_ID` verweist auf Student, "
                "`Kurs_ID` verweist auf Kurs. Zusammen bilden sie den zusammengesetzten Primärschlüssel."
            )
        )
    elif pred_mn.value == "0":
        mo.output.replace(
            mo.md(
                "❌ Ohne Fremdschlüssel wäre die Beziehungstabelle nicht mit den Entitätstabellen "
                "verbunden. Sie braucht mindestens **2 Fremdschlüssel** — einen pro Seite der M:N-Beziehung."
            )
        )
    elif pred_mn.value == "1":
        mo.output.replace(
            mo.md(
                "❌ Ein Fremdschlüssel verbindet nur mit **einer** Seite. Bei einer M:N-Beziehung "
                "müssen **beide** Seiten referenziert werden — also mindestens **2 Fremdschlüssel**."
            )
        )
    elif pred_mn.value == "3":
        mo.output.replace(
            mo.md(
                "❌ 3 wären zu viele für eine einfache M:N-Beziehung. Es braucht genau **2 Fremdschlüssel** — "
                "einen pro Seite. (Mehr FKs gibt es nur bei ternären Beziehungen mit 3 Entitäten.)"
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ### Geführtes Beispiel 6.2: Entitätstabellen anlegen

        Zuerst die beiden Entitätstabellen, **dann** die Beziehungstabelle — die Reihenfolge
        ist wichtig, weil die Beziehungstabelle auf beide verweist.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Student (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Kurs (
            ID INTEGER PRIMARY KEY,
            Titel VARCHAR(200) NOT NULL
        );

        INSERT OR IGNORE INTO Student VALUES (1, 'Anna');
        INSERT OR IGNORE INTO Student VALUES (2, 'Ben');
        INSERT OR IGNORE INTO Student VALUES (3, 'Clara');

        INSERT OR IGNORE INTO Kurs VALUES (101, 'Datenmanagement');
        INSERT OR IGNORE INTO Kurs VALUES (102, 'BWL');
        INSERT OR IGNORE INTO Kurs VALUES (103, 'Statistik');

        SELECT * FROM Student;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        SELECT * FROM Kurs;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 6.2b: Beziehungstabelle mit zusammengesetztem PK
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Student_Kurs (
            Student_ID INTEGER,
            Kurs_ID INTEGER,
            Note DECIMAL(2,1),
            PRIMARY KEY (Student_ID, Kurs_ID),
            FOREIGN KEY (Student_ID) REFERENCES Student(ID),
            FOREIGN KEY (Kurs_ID) REFERENCES Kurs(ID)
        );

        INSERT OR IGNORE INTO Student_Kurs VALUES (1, 101, 1.3);
        INSERT OR IGNORE INTO Student_Kurs VALUES (1, 102, 2.0);
        INSERT OR IGNORE INTO Student_Kurs VALUES (2, 101, 1.7);
        INSERT OR IGNORE INTO Student_Kurs VALUES (3, 101, 1.0);
        INSERT OR IGNORE INTO Student_Kurs VALUES (3, 103, 1.3);

        SELECT * FROM Student_Kurs;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Die Kombination `(Student_ID, Kurs_ID)` ist der **zusammengesetzte Primärschlüssel**.
        Jede Kombination darf nur einmal vorkommen — Anna kann den Kurs "Datenmanagement" nur einmal besuchen.
        Das Attribut `Note` ist ein **Beziehungsattribut**: Es gehört weder zum Studenten noch zum Kurs,
        sondern zur Beziehung zwischen beiden.

        ---

        ### Geführtes Beispiel 6.2c: JOIN über die Beziehungstabelle
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
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
    mo.md(
        r"""
        **Erkenntnis:** Die Beziehungstabelle wird beim JOIN als **Brücke** zwischen den
        beiden Entitätstabellen verwendet. Ein JOIN über die M:N-Auflösung erfordert
        immer **zwei JOINs** — einen pro Fremdschlüssel.

        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 4.x**

        ---
        """
    )
    return


# ============================================================
# Phase 5: Online-Shop + Referentielle Integrität
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 5: Online-Shop + Referentielle Integrität

        ### Ein komplettes Datenmodell mit mehreren Beziehungstypen

        Der folgende Online-Shop kombiniert **1:N** und **M:N** Beziehungen
        in einem realistischen Schema mit 5 Tabellen.
        """
    )
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
                int Bestellung_ID PK_FK
                int Produkt_ID PK_FK
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
    ### Vorhersage 3
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_order = mo.ui.radio(
        options={
            "richtig": "Kategorie → Produkt → Kunde → Bestellung → Bestellposition",
            "reverse": "Bestellposition → Bestellung → Kunde → Produkt → Kategorie",
            "egal": "Die Reihenfolge spielt keine Rolle",
            "wrong": "Kunde → Bestellung → Bestellposition → Kategorie → Produkt",
        },
        label="**Vorhersage:** In welcher Reihenfolge müssen die CREATE TABLE Statements ausgeführt werden?",
    )
    pred_order
    return (pred_order,)


@app.cell(hide_code=True)
def _(pred_order, mo):
    if pred_order.value == "richtig":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Tabellen, die von anderen referenziert werden, müssen **zuerst** "
                "erstellt werden. Kategorie hat keine Abhängigkeiten → zuerst. Produkt verweist auf "
                "Kategorie → danach. Bestellposition verweist auf Bestellung *und* Produkt → ganz am Ende."
            )
        )
    elif pred_order.value == "reverse":
        mo.output.replace(
            mo.md(
                "❌ Umgekehrt! Bestellposition hat Fremdschlüssel auf Bestellung und Produkt — "
                "diese müssen **vorher** existieren. Die Reihenfolge ist: zuerst die Tabellen "
                "**ohne** Abhängigkeiten, dann die mit FK. Richtig: "
                "**Kategorie → Produkt → Kunde → Bestellung → Bestellposition**."
            )
        )
    elif pred_order.value == "egal":
        mo.output.replace(
            mo.md(
                "❌ Die Reihenfolge ist **nicht** egal! Ein `FOREIGN KEY` kann nur auf eine Tabelle "
                "verweisen, die **bereits existiert**. Deshalb müssen referenzierte Tabellen zuerst "
                "angelegt werden: **Kategorie → Produkt → Kunde → Bestellung → Bestellposition**."
            )
        )
    elif pred_order.value == "wrong":
        mo.output.replace(
            mo.md(
                "❌ Fast, aber Kategorie muss **vor** Produkt kommen (Produkt hat FK auf Kategorie). "
                "Richtige Reihenfolge: **Kategorie → Produkt → Kunde → Bestellung → Bestellposition**."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ### Geführtes Beispiel 6.3: CREATE TABLE in der richtigen Reihenfolge

        **Schritt 1:** Kategorie — hat keine Abhängigkeiten.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Schritt 2:** Produkt — Fremdschlüssel auf Kategorie (1:N).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Schritt 3:** Kunde — keine Fremdschlüssel, kann parallel zu Produkt erstellt werden.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Schritt 4:** Bestellung — Fremdschlüssel auf Kunde (1:N).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Schritt 5:** Bestellposition — M:N-Auflösung zwischen Bestellung und Produkt.
        Diese Tabelle kommt **zuletzt**, weil sie auf beide verweist.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Bestellposition (
            Bestellung_ID INTEGER,
            Produkt_ID INTEGER,
            Menge INTEGER NOT NULL DEFAULT 1,
            PRIMARY KEY (Bestellung_ID, Produkt_ID),
            FOREIGN KEY (Bestellung_ID) REFERENCES Bestellung(ID),
            FOREIGN KEY (Produkt_ID) REFERENCES Produkt(ID)
        );

        INSERT OR IGNORE INTO Bestellposition VALUES (1, 1, 1);
        INSERT OR IGNORE INTO Bestellposition VALUES (1, 3, 2);
        INSERT OR IGNORE INTO Bestellposition VALUES (2, 4, 1);
        INSERT OR IGNORE INTO Bestellposition VALUES (3, 2, 3);

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

        ### Referentielle Integrität

        Was passiert, wenn jemand eine referenzierte Zeile löschen möchte?
        SQL bietet drei Strategien:

        | Option | SQL-Syntax | Bedeutung |
        |--------|------------|-----------|
        | **Verbieten** | `ON DELETE RESTRICT` | Löschung wird abgelehnt (Standard!) |
        | **Kaskadieren** | `ON DELETE CASCADE` | Abhängige Zeilen werden mitgelöscht |
        | **NULL setzen** | `ON DELETE SET NULL` | FK wird auf `NULL` gesetzt |

        **Praxis-Tipp:** `RESTRICT` ist fast immer die sicherste Wahl —
        lieber eine Fehlermeldung als versehentlich gelöschte Daten!

        ---
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
        label="**Quiz:** Bei einer 1:N-Beziehung (Verein → Spieler) — auf welcher Seite steht der Fremdschlüssel?",
    )
    quiz_fk
    return (quiz_fk,)


@app.cell(hide_code=True)
def _(quiz_fk, mo):
    if quiz_fk.value == "correct":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Der Fremdschlüssel steht immer auf der **N-Seite**. "
                "Jeder Spieler gehört zu *einem* Verein, also speichert die Spieler-Tabelle "
                "die `Verein_ID`. Der Verein selbst muss nicht wissen, welche Spieler er hat — "
                "das ergibt sich durch den JOIN."
            )
        )
    elif quiz_fk.value:
        mo.output.replace(
            mo.md(
                "❌ Nicht ganz. Überlegen Sie: Kann ein Verein auf *alle* seine Spieler verweisen? "
                "Das wäre eine variable Anzahl! Stattdessen verweist jeder **einzelne Spieler** "
                "auf seinen (einen) Verein — der FK steht auf der **N-Seite**."
            )
        )
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


# ============================================================
# Phase 7: Visualisierung
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 7: Visualisierung — Normalisierte Daten analysieren

        Durch die Aufteilung in mehrere Tabellen können wir jetzt differenzierte
        Analysen durchführen. JOINs bringen die Informationen zusammen.
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
    ### Umsatz pro Kategorie
    """)
    return


@app.cell(hide_code=True)
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
    mo.md(r"""
    ### Zeilenanzahl pro Tabelle
    """)
    return


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
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
        Die M:N-Auflösungstabelle wächst am schnellsten — das ist normal!

        ---

        ### Viz-Choice: Den richtigen Charttyp wählen
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    viz_choice_6 = mo.ui.radio(
        options={
            "bar": "Balkendiagramm",
            "pie": "Kreisdiagramm",
            "line": "Liniendiagramm",
            "heatmap": "Heatmap",
        },
        label="Umsatz pro Produktkategorie darstellen — welcher Charttyp?",
    )
    viz_choice_6
    return (viz_choice_6,)


@app.cell(hide_code=True)
def _(viz_choice_6, mo):
    if viz_choice_6.value == "bar":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Ein **Balkendiagramm** eignet sich ideal für den Vergleich von "
                "Kategorien — die Balkenlänge macht Unterschiede sofort sichtbar. "
                "Kategorien sind nominale Daten → Balken statt Linien."
            )
        )
    elif viz_choice_6.value == "pie":
        mo.output.replace(
            mo.md(
                "❌ Kreisdiagramme zeigen Anteile am Ganzen, aber der Mensch kann Winkel "
                "schlecht vergleichen. Ein **Balkendiagramm** macht die Unterschiede zwischen "
                "Kategorien deutlich besser sichtbar."
            )
        )
    elif viz_choice_6.value == "line":
        mo.output.replace(
            mo.md(
                "❌ Liniendiagramme sind für **zeitliche Verläufe** gedacht — sie suggerieren "
                "eine Reihenfolge zwischen den Datenpunkten. Kategorien haben keine natürliche "
                "Reihenfolge → ein **Balkendiagramm** ist die bessere Wahl."
            )
        )
    elif viz_choice_6.value == "heatmap":
        mo.output.replace(
            mo.md(
                "❌ Heatmaps eignen sich für **zweidimensionale** Daten (z.B. Korrelationen). "
                "Hier haben wir nur eine Dimension (Kategorie → Umsatz) — "
                "ein **Balkendiagramm** ist einfacher und klarer."
            )
        )
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
    selbsttest_6 = mo.ui.radio(
        options={
            "restrict": "Die Löschung wird verhindert (RESTRICT)",
            "auto_delete": "Alle Produkte werden automatisch mitgelöscht",
            "nichts": "Nichts — Fremdschlüssel werden ignoriert",
        },
        label="Was passiert beim Löschen einer Kategorie, die noch Produkte enthält (Standard-Verhalten)?",
    )
    selbsttest_6
    return (selbsttest_6,)


@app.cell(hide_code=True)
def _(selbsttest_6, mo):
    if selbsttest_6.value == "restrict":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Das Standardverhalten ist **RESTRICT** — die Datenbank "
                "verweigert die Löschung, solange noch abhängige Datensätze existieren. "
                "Das schützt die referentielle Integrität: Kein Produkt verweist auf eine "
                "nicht existierende Kategorie."
            )
        )
    elif selbsttest_6.value == "auto_delete":
        mo.output.replace(
            mo.md(
                "❌ Automatisches Mitlöschen wäre **CASCADE** — das muss explizit mit "
                "`ON DELETE CASCADE` definiert werden. Das Standard-Verhalten ist **RESTRICT**: "
                "Die Löschung wird verhindert, um Datenverlust zu vermeiden."
            )
        )
    elif selbsttest_6.value == "nichts":
        mo.output.replace(
            mo.md(
                "❌ Fremdschlüssel-Constraints werden **nicht** ignoriert! Die Datenbank prüft "
                "bei jeder Änderung, ob die Integrität gewahrt bleibt. Das Standard-Verhalten "
                "ist **RESTRICT**: Die Löschung wird abgelehnt."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        ### Transformationsregeln

        | Beziehungstyp | Transformation | Beispiel |
        |---------------|---------------|----------|
        | **1:N** | FK auf der N-Seite | `Spieler.Verein_ID → Verein.ID` |
        | **M:N** | Beziehungstabelle mit 2 FKs + zusammengesetztem PK | `Student_Kurs(Student_ID, Kurs_ID)` |
        | **1:1** | Zusammenlegen oder FK auf einer Seite | Je nach Kontext |

        ### SQL-Syntax-Template

        ```sql
        CREATE TABLE Name (
            ID INTEGER PRIMARY KEY,
            Attribut DATENTYP [NOT NULL | UNIQUE | DEFAULT ...],
            FK_ID INTEGER,
            FOREIGN KEY (FK_ID) REFERENCES AndereTabelle(ID)
                [ON DELETE RESTRICT | CASCADE | SET NULL]
        );
        ```

        ### Merksätze

        - **Reihenfolge:** Referenzierte Tabellen zuerst erstellen
        - **1:N:** FK auf der N-Seite — "der Viele verweist auf den Einen"
        - **M:N:** Beziehungstabelle mit zusammengesetztem PK aus 2 FKs
        - **RESTRICT** ist der sichere Standard für referentielle Integrität

        ### Ausblick Session 7

        Nächste Woche: **Normalisierung (1NF, 2NF, 3NF)** — Wie erkennt man, ob ein Datenbankschema
        gut strukturiert ist? Und wie verbessert man es systematisch?
        """
    )
    return


if __name__ == "__main__":
    app.run()
