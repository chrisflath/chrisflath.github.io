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
    app_title="DMA Session 6: ER → SQL — Übungen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 6: ER → SQL — Übungen

        Theorie und geführte Beispiele → **06-er-zu-sql-guide.py**

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
    return pl, px


# ============================================================
# Phase 2: 1:N-Beziehungen
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 2: 1:N-Beziehungen in SQL

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 2.1: Verein und Spieler (1:N)

        Bei einer 1:N-Beziehung steht der Fremdschlüssel auf der **N-Seite**.
        Hier: Jeder Spieler verweist auf seinen Verein.

        Führen Sie die Zelle aus und beobachten Sie die Struktur:
        """
    )
    return


@app.cell
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

        SELECT s.Name, s.Position, v.Name AS Verein
        FROM Spieler s JOIN Verein v ON s.Verein_ID = v.ID;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 2.2: Abteilung und Mitarbeiter — FK ergänzen

        Die Tabelle `Mitarbeiter` benötigt einen Fremdschlüssel zu `Abteilung`.
        Ersetzen Sie die `???` durch die richtigen Werte:
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Erstellen Sie die Tabelle Mitarbeiter mit FK zu Abteilung
        CREATE TABLE IF NOT EXISTS Abteilung (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL
        );
        INSERT OR IGNORE INTO Abteilung VALUES (1, 'IT');
        INSERT OR IGNORE INTO Abteilung VALUES (2, 'Marketing');

        CREATE TABLE IF NOT EXISTS Mitarbeiter (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            ??? INTEGER,
            FOREIGN KEY (???) REFERENCES ???(ID)
        );
        -- Tipp: Abteilung_ID als Fremdschlüssel zu Abteilung
        INSERT OR IGNORE INTO Mitarbeiter VALUES (1, 'Schmidt', 1);
        INSERT OR IGNORE INTO Mitarbeiter VALUES (2, 'Weber', 2);

        SELECT m.Name, a.Name AS Abteilung
        FROM Mitarbeiter m JOIN Abteilung a ON m.Abteilung_ID = a.ID;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
CREATE TABLE IF NOT EXISTS Mitarbeiter (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Abteilung_ID INTEGER,
    FOREIGN KEY (Abteilung_ID) REFERENCES Abteilung(ID)
);
```

**Erklärung:** Der Fremdschlüssel `Abteilung_ID` verweist auf die `ID`-Spalte der Tabelle `Abteilung`. Die `FOREIGN KEY`-Klausel gibt an, welche Spalte auf welche Tabelle verweist.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.3: Professor und Kurs (1:N) — Selbstständig

        Erstellen Sie ein Schema für **Professoren** und **Kurse** (1:N).
        Jeder Kurs wird von genau einem Professor gehalten.

        - `Professor`: ID, Name, Fachgebiet
        - `Kurs`: ID, Titel, SWS, Professor_ID (FK)

        Fügen Sie jeweils 2–3 Beispieldatensätze ein und schreiben Sie eine JOIN-Abfrage.
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 🔵 Erstellen Sie Ihre Tabellen hier:
        SELECT 'Ihre Lösung hier' AS Hinweis;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
CREATE TABLE IF NOT EXISTS Professor (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Fachgebiet VARCHAR(100)
);
INSERT OR IGNORE INTO Professor VALUES (1, 'Prof. Müller', 'Informatik');
INSERT OR IGNORE INTO Professor VALUES (2, 'Prof. Schmidt', 'BWL');

CREATE TABLE IF NOT EXISTS Kurs (
    ID INTEGER PRIMARY KEY,
    Titel VARCHAR(200) NOT NULL,
    SWS INTEGER,
    Professor_ID INTEGER,
    FOREIGN KEY (Professor_ID) REFERENCES Professor(ID)
);
INSERT OR IGNORE INTO Kurs VALUES (1, 'Datenmanagement', 4, 1);
INSERT OR IGNORE INTO Kurs VALUES (2, 'Programmierung', 4, 1);
INSERT OR IGNORE INTO Kurs VALUES (3, 'Marketing', 2, 2);

SELECT k.Titel, k.SWS, p.Name AS Professor
FROM Kurs k JOIN Professor p ON k.Professor_ID = p.ID;
```

**Erklärung:** Der FK `Professor_ID` steht in der Kurs-Tabelle (N-Seite), da jeder Kurs genau einem Professor zugeordnet ist, ein Professor aber mehrere Kurse halten kann.
""")})
    return


# ============================================================
# Phase 4: M:N-Beziehungen
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 4: M:N-Beziehungen in SQL

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.1: Student und Kurs (M:N)

        Eine M:N-Beziehung wird über eine **Beziehungstabelle** mit zwei Fremdschlüsseln
        und einem zusammengesetzten Primärschlüssel aufgelöst.

        Führen Sie die Zelle aus und beobachten Sie die Struktur:
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Student (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Kurs_MN (
            ID INTEGER PRIMARY KEY,
            Titel VARCHAR(200) NOT NULL
        );

        INSERT OR IGNORE INTO Student VALUES (1, 'Anna');
        INSERT OR IGNORE INTO Student VALUES (2, 'Ben');
        INSERT OR IGNORE INTO Student VALUES (3, 'Clara');

        INSERT OR IGNORE INTO Kurs_MN VALUES (101, 'Datenmanagement');
        INSERT OR IGNORE INTO Kurs_MN VALUES (102, 'BWL');
        INSERT OR IGNORE INTO Kurs_MN VALUES (103, 'Statistik');

        CREATE TABLE IF NOT EXISTS Student_Kurs (
            Student_ID INTEGER,
            Kurs_ID INTEGER,
            Note DECIMAL(2,1),
            PRIMARY KEY (Student_ID, Kurs_ID),
            FOREIGN KEY (Student_ID) REFERENCES Student(ID),
            FOREIGN KEY (Kurs_ID) REFERENCES Kurs_MN(ID)
        );

        INSERT OR IGNORE INTO Student_Kurs VALUES (1, 101, 1.3);
        INSERT OR IGNORE INTO Student_Kurs VALUES (1, 102, 2.0);
        INSERT OR IGNORE INTO Student_Kurs VALUES (2, 101, 1.7);
        INSERT OR IGNORE INTO Student_Kurs VALUES (3, 101, 1.0);
        INSERT OR IGNORE INTO Student_Kurs VALUES (3, 103, 1.3);

        SELECT s.Name AS Student, k.Titel AS Kurs, sk.Note
        FROM Student_Kurs sk
        JOIN Student s ON sk.Student_ID = s.ID
        JOIN Kurs_MN k ON sk.Kurs_ID = k.ID
        ORDER BY s.Name, k.Titel;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 4.2: Autor und Buch (M:N) — Beziehungstabelle ergänzen

        Ein Buch kann mehrere Autoren haben, und ein Autor kann mehrere Bücher schreiben.
        Ergänzen Sie die `???` in der Beziehungstabelle:
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Autor (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Buch (
            ID INTEGER PRIMARY KEY,
            Titel VARCHAR(200) NOT NULL
        );
        INSERT OR IGNORE INTO Autor VALUES (1, 'Kemper');
        INSERT OR IGNORE INTO Autor VALUES (2, 'Eickler');
        INSERT OR IGNORE INTO Buch VALUES (1, 'Datenbanksysteme');
        INSERT OR IGNORE INTO Buch VALUES (2, 'SQL-Praxis');

        -- Ergänzen Sie die Beziehungstabelle:
        CREATE TABLE IF NOT EXISTS Autor_Buch (
            Autor_ID INTEGER,
            Buch_ID INTEGER,
            PRIMARY KEY (???, ???),
            FOREIGN KEY (Autor_ID) REFERENCES Autor(ID),
            FOREIGN KEY (???) REFERENCES Buch(ID)
        );
        INSERT OR IGNORE INTO Autor_Buch VALUES (1, 1);
        INSERT OR IGNORE INTO Autor_Buch VALUES (2, 1);
        INSERT OR IGNORE INTO Autor_Buch VALUES (1, 2);

        SELECT a.Name AS Autor, b.Titel AS Buch
        FROM Autor_Buch ab
        JOIN Autor a ON ab.Autor_ID = a.ID
        JOIN Buch b ON ab.Buch_ID = b.ID;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
CREATE TABLE IF NOT EXISTS Autor_Buch (
    Autor_ID INTEGER,
    Buch_ID INTEGER,
    PRIMARY KEY (Autor_ID, Buch_ID),
    FOREIGN KEY (Autor_ID) REFERENCES Autor(ID),
    FOREIGN KEY (Buch_ID) REFERENCES Buch(ID)
);
```

**Erklärung:** Der zusammengesetzte Primärschlüssel `(Autor_ID, Buch_ID)` stellt sicher, dass jede Autor-Buch-Kombination nur einmal vorkommen kann. Beide Spalten sind gleichzeitig Fremdschlüssel.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.3: Bibliotheks-Ausleihe (M:N) — Selbstständig

        Erstellen Sie drei Tabellen für eine Bibliotheks-Ausleihe:

        - `Buch_Bib`: ID, Titel, ISBN
        - `Student_Bib`: MatrikelNr (PK), Name
        - `Ausleihe`: Buch_ID (FK), MatrikelNr (FK), Ausleihdatum — zusammengesetzter PK

        Fügen Sie Beispieldaten ein und schreiben Sie eine JOIN-Abfrage, die zeigt,
        welcher Student welches Buch ausgeliehen hat.
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 🔵 Erstellen Sie Ihre Tabellen hier:
        SELECT 'Ihre Lösung hier' AS Hinweis;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
CREATE TABLE IF NOT EXISTS Buch_Bib (
    ID INTEGER PRIMARY KEY,
    Titel VARCHAR(200) NOT NULL,
    ISBN VARCHAR(20)
);
CREATE TABLE IF NOT EXISTS Student_Bib (
    MatrikelNr INTEGER PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS Ausleihe (
    Buch_ID INTEGER,
    MatrikelNr INTEGER,
    Ausleihdatum DATE NOT NULL,
    PRIMARY KEY (Buch_ID, MatrikelNr),
    FOREIGN KEY (Buch_ID) REFERENCES Buch_Bib(ID),
    FOREIGN KEY (MatrikelNr) REFERENCES Student_Bib(MatrikelNr)
);

INSERT OR IGNORE INTO Buch_Bib VALUES (1, 'Datenbanksysteme', '978-3-486-72139-3');
INSERT OR IGNORE INTO Buch_Bib VALUES (2, 'SQL für Einsteiger', '978-3-446-43740-1');
INSERT OR IGNORE INTO Student_Bib VALUES (12345, 'Anna Müller');
INSERT OR IGNORE INTO Student_Bib VALUES (67890, 'Ben Schmidt');
INSERT OR IGNORE INTO Ausleihe VALUES (1, 12345, '2026-04-01');
INSERT OR IGNORE INTO Ausleihe VALUES (2, 67890, '2026-04-05');
INSERT OR IGNORE INTO Ausleihe VALUES (1, 67890, '2026-04-10');

SELECT s.Name AS Student, b.Titel AS Buch, a.Ausleihdatum
FROM Ausleihe a
JOIN Buch_Bib b ON a.Buch_ID = b.ID
JOIN Student_Bib s ON a.MatrikelNr = s.MatrikelNr
ORDER BY a.Ausleihdatum;
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 4.4: Falscher Primärschlüssel in M:N-Tabelle

        Die folgende Einschreibungstabelle hat einen Fehler im Primärschlüssel.
        Finden Sie das Problem und erklären Sie, was passiert:
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese M:N-Tabelle hat einen Fehler im Primärschlüssel!
        CREATE TABLE IF NOT EXISTS Einschreibung (
            Student_ID INTEGER PRIMARY KEY,
            Kurs_ID INTEGER,
            Semester VARCHAR(10),
            FOREIGN KEY (Student_ID) REFERENCES Student(ID),
            FOREIGN KEY (Kurs_ID) REFERENCES Kurs_MN(ID)
        );
        -- Problem: Ein Student kann sich nur in EINEN Kurs einschreiben!
        -- Was muss geändert werden?
        SELECT 'Finden Sie den Fehler im PRIMARY KEY' AS Aufgabe;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Fehler:** `Student_ID INTEGER PRIMARY KEY` allein bedeutet, dass jeder Student nur **einmal** in der Tabelle vorkommen kann. Ein Student könnte sich also nur in **einen einzigen** Kurs einschreiben!

**Korrektur:** Der Primärschlüssel muss **zusammengesetzt** sein:

```sql
CREATE TABLE IF NOT EXISTS Einschreibung (
    Student_ID INTEGER,
    Kurs_ID INTEGER,
    Semester VARCHAR(10),
    PRIMARY KEY (Student_ID, Kurs_ID),
    FOREIGN KEY (Student_ID) REFERENCES Student(ID),
    FOREIGN KEY (Kurs_ID) REFERENCES Kurs_MN(ID)
);
```

**Merke:** Bei M:N-Beziehungen besteht der Primärschlüssel der Beziehungstabelle aus **beiden** Fremdschlüsseln zusammen.
""")})
    return


# ============================================================
# Phase 6: Online-Shop + Komplexe Schemas
# ============================================================


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 6: Komplexe Schemas

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.1: Online-Shop — Vollständiges Schema

        Ein realistisches Schema mit 5 Tabellen. Beachten Sie die Reihenfolge der
        `CREATE TABLE`-Statements — Tabellen ohne Abhängigkeiten kommen zuerst!

        Führen Sie die Zelle aus und studieren Sie die Struktur:
        """
    )
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

        -- 3. Kunde (keine Abhängigkeiten)
        CREATE TABLE IF NOT EXISTS Kunde (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Email VARCHAR(200) UNIQUE
        );
        INSERT OR IGNORE INTO Kunde VALUES (1, 'Max Mustermann', 'max@example.com');
        INSERT OR IGNORE INTO Kunde VALUES (2, 'Erika Musterfrau', 'erika@example.com');
        INSERT OR IGNORE INTO Kunde VALUES (3, 'Tim Tester', 'tim@example.com');

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

        -- 5. Bestellposition (M:N zwischen Bestellung und Produkt)
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
        INSERT OR IGNORE INTO Bestellposition VALUES (3, 3, 1);

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
        ### 🟡 Aufgabe 6.2: Bewertungstabelle ergänzen

        Ergänzen Sie eine Bewertungstabelle zum Online-Shop.
        Ersetzen Sie die `???` durch die richtigen Fremdschlüssel-Referenzen:
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Ergänzen Sie eine Bewertungstabelle
        CREATE TABLE IF NOT EXISTS Bewertung (
            ID INTEGER PRIMARY KEY,
            Kunde_ID INTEGER,
            Produkt_ID INTEGER,
            Sterne INTEGER CHECK(Sterne BETWEEN 1 AND 5),
            Kommentar VARCHAR(500),
            FOREIGN KEY (???) REFERENCES Kunde(ID),
            FOREIGN KEY (???) REFERENCES Produkt(ID)
        );
        INSERT OR IGNORE INTO Bewertung VALUES (1, 1, 1, 5, 'Tolles Laptop!');
        INSERT OR IGNORE INTO Bewertung VALUES (2, 2, 2, 4, 'Gute Qualität');

        SELECT k.Name AS Kunde, p.Name AS Produkt, b.Sterne, b.Kommentar
        FROM Bewertung b
        JOIN Kunde k ON b.Kunde_ID = k.ID
        JOIN Produkt p ON b.Produkt_ID = p.ID;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
CREATE TABLE IF NOT EXISTS Bewertung (
    ID INTEGER PRIMARY KEY,
    Kunde_ID INTEGER,
    Produkt_ID INTEGER,
    Sterne INTEGER CHECK(Sterne BETWEEN 1 AND 5),
    Kommentar VARCHAR(500),
    FOREIGN KEY (Kunde_ID) REFERENCES Kunde(ID),
    FOREIGN KEY (Produkt_ID) REFERENCES Produkt(ID)
);
```

**Erklärung:** Die `FOREIGN KEY`-Klauseln verweisen auf die jeweilige Spalte in der aktuellen Tabelle und die referenzierte Tabelle. `CHECK(Sterne BETWEEN 1 AND 5)` ist ein zusätzlicher **CHECK-Constraint**, der ungültige Werte verhindert.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.3: Gesamtumsatz pro Kunde

        Berechnen Sie den Gesamtumsatz pro Kunde.

        **Hinweis:** Sie benötigen einen JOIN über Bestellposition, Bestellung, Kunde und
        Produkt. Verwenden Sie `SUM(Preis * Menge)` und `GROUP BY`.
        """
    )
    return


@app.cell
def _(mo):
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
    k.Name AS Kunde,
    COUNT(DISTINCT b.ID) AS Bestellungen,
    SUM(p.Preis * bp.Menge) AS Gesamtumsatz
FROM Bestellposition bp
JOIN Bestellung b ON bp.Bestellung_ID = b.ID
JOIN Kunde k ON b.Kunde_ID = k.ID
JOIN Produkt p ON bp.Produkt_ID = p.ID
GROUP BY k.Name
ORDER BY Gesamtumsatz DESC;
```

**Erklärung:** Der 4-Tabellen-JOIN verknüpft alle relevanten Informationen. `SUM(p.Preis * bp.Menge)` berechnet den Umsatz pro Position, gruppiert nach Kunde. `COUNT(DISTINCT b.ID)` zählt die verschiedenen Bestellungen.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.4: Kunden ohne Bestellungen (LEFT JOIN)

        Finden Sie alle Kunden, die **noch keine Bestellung** aufgegeben haben.

        **Hinweis:** Verwenden Sie `LEFT JOIN` und prüfen Sie mit `IS NULL`, ob keine
        Bestellung existiert.
        """
    )
    return


@app.cell
def _(mo):
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
SELECT k.Name AS Kunde, k.Email
FROM Kunde k
LEFT JOIN Bestellung b ON k.ID = b.Kunde_ID
WHERE b.ID IS NULL;
```

**Erklärung:** `LEFT JOIN` behält alle Kunden, auch wenn sie keine Bestellung haben. In diesem Fall sind die Bestellungs-Spalten `NULL`. `WHERE b.ID IS NULL` filtert genau diese Kunden heraus. Das ist ein klassisches Muster, um "fehlende" Beziehungen zu finden.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.5: CREATE TABLE in falscher Reihenfolge

        Die folgenden `CREATE TABLE`-Statements sind in der **falschen Reihenfolge**.
        Welche Tabelle muss **zuerst** erstellt werden und warum?
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese CREATE TABLE Statements sind in der falschen Reihenfolge!
        -- Welche Tabelle muss ZUERST erstellt werden?

        -- CREATE TABLE Bestellung_Test (
        --     ID INTEGER PRIMARY KEY,
        --     Kunde_ID INTEGER,
        --     FOREIGN KEY (Kunde_ID) REFERENCES Kunde_Test(ID)
        -- );
        -- CREATE TABLE Kunde_Test (
        --     ID INTEGER PRIMARY KEY,
        --     Name VARCHAR(100)
        -- );

        -- Erklärung: Bestellung verweist auf Kunde, also muss Kunde ZUERST existieren!
        SELECT 'Bestellung referenziert Kunde — Kunde muss zuerst erstellt werden!' AS Erklärung;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** `Bestellung_Test` hat einen Fremdschlüssel, der auf `Kunde_Test(ID)` verweist. Die referenzierte Tabelle `Kunde_Test` muss **vor** der referenzierenden Tabelle existieren!

**Richtige Reihenfolge:**
```sql
-- 1. Zuerst die referenzierte Tabelle:
CREATE TABLE Kunde_Test (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(100)
);

-- 2. Dann die Tabelle mit dem Fremdschlüssel:
CREATE TABLE Bestellung_Test (
    ID INTEGER PRIMARY KEY,
    Kunde_ID INTEGER,
    FOREIGN KEY (Kunde_ID) REFERENCES Kunde_Test(ID)
);
```

**Faustregel:** Erstellen Sie Tabellen in der Reihenfolge ihrer Abhängigkeiten — unabhängige Tabellen zuerst, abhängige Tabellen danach.
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
        ### ⭐ Verschiedene Produkte pro Bestellung

        Wie viele **verschiedene Produkte** enthält jede Bestellung?
        Zeigen Sie Bestellnummer, Kundennamen, Datum und Anzahl verschiedener Produkte.
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- ⭐ Verschiedene Produkte pro Bestellung
        SELECT 'Ihre Lösung hier' AS Hinweis;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    b.ID AS Bestellung,
    k.Name AS Kunde,
    b.Datum,
    COUNT(bp.Produkt_ID) AS Verschiedene_Produkte,
    SUM(bp.Menge) AS Gesamtmenge
FROM Bestellung b
JOIN Kunde k ON b.Kunde_ID = k.ID
JOIN Bestellposition bp ON b.ID = bp.Bestellung_ID
GROUP BY b.ID, k.Name, b.Datum
ORDER BY Verschiedene_Produkte DESC;
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐ Bibliotheks-Schema (5 Tabellen)

        Erstellen Sie ein vollständiges Bibliotheks-Schema mit 5 Tabellen:

        - `Verlag` (ID, Name, Ort)
        - `Autor_Bib` (ID, Name, Nationalität)
        - `Buch_Komplett` (ID, Titel, ISBN, Erscheinungsjahr, Verlag_ID FK)
        - `Exemplar` (ID, Buch_ID FK, Standort)
        - `Ausleihe_Komplett` (Exemplar_ID FK, MatrikelNr FK, Ausleihdatum, Rückgabedatum)

        Vergessen Sie nicht: `Autor_Bib` und `Buch_Komplett` stehen in einer M:N-Beziehung!
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- ⭐⭐ Bibliotheks-Schema mit 5 Tabellen
        SELECT 'Ihre Lösung hier' AS Hinweis;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
CREATE TABLE IF NOT EXISTS Verlag (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Ort VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Autor_Bib (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Nationalitaet VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Buch_Komplett (
    ID INTEGER PRIMARY KEY,
    Titel VARCHAR(200) NOT NULL,
    ISBN VARCHAR(20),
    Erscheinungsjahr INTEGER,
    Verlag_ID INTEGER,
    FOREIGN KEY (Verlag_ID) REFERENCES Verlag(ID)
);

-- M:N-Beziehungstabelle Autor <-> Buch
CREATE TABLE IF NOT EXISTS Autor_Buch_Bib (
    Autor_ID INTEGER,
    Buch_ID INTEGER,
    PRIMARY KEY (Autor_ID, Buch_ID),
    FOREIGN KEY (Autor_ID) REFERENCES Autor_Bib(ID),
    FOREIGN KEY (Buch_ID) REFERENCES Buch_Komplett(ID)
);

CREATE TABLE IF NOT EXISTS Exemplar (
    ID INTEGER PRIMARY KEY,
    Buch_ID INTEGER,
    Standort VARCHAR(50),
    FOREIGN KEY (Buch_ID) REFERENCES Buch_Komplett(ID)
);

CREATE TABLE IF NOT EXISTS Ausleihe_Komplett (
    Exemplar_ID INTEGER,
    MatrikelNr INTEGER,
    Ausleihdatum DATE NOT NULL,
    Rueckgabedatum DATE,
    PRIMARY KEY (Exemplar_ID, MatrikelNr, Ausleihdatum),
    FOREIGN KEY (Exemplar_ID) REFERENCES Exemplar(ID),
    FOREIGN KEY (MatrikelNr) REFERENCES Student_Bib(MatrikelNr)
);

-- Beispieldaten
INSERT OR IGNORE INTO Verlag VALUES (1, 'Oldenbourg', 'München');
INSERT OR IGNORE INTO Autor_Bib VALUES (1, 'Kemper', 'deutsch');
INSERT OR IGNORE INTO Autor_Bib VALUES (2, 'Eickler', 'deutsch');
INSERT OR IGNORE INTO Buch_Komplett VALUES (1, 'Datenbanksysteme', '978-3-486-72139-3', 2015, 1);
INSERT OR IGNORE INTO Autor_Buch_Bib VALUES (1, 1);
INSERT OR IGNORE INTO Autor_Buch_Bib VALUES (2, 1);
INSERT OR IGNORE INTO Exemplar VALUES (1, 1, 'Regal A3');
INSERT OR IGNORE INTO Exemplar VALUES (2, 1, 'Regal A3');

SELECT a.Name AS Autor, b.Titel, v.Name AS Verlag
FROM Autor_Buch_Bib ab
JOIN Autor_Bib a ON ab.Autor_ID = a.ID
JOIN Buch_Komplett b ON ab.Buch_ID = b.ID
JOIN Verlag v ON b.Verlag_ID = v.ID;
```

**Beachten Sie:** Insgesamt 6 Tabellen (inkl. M:N-Beziehungstabelle). Die Reihenfolge der CREATE TABLE Statements folgt den Abhängigkeiten.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐⭐ Schema mit CHECK-Constraints und DEFAULT-Werten

        Erstellen Sie ein Mitarbeiter-Projekt-Schema mit erweiterten Constraints:

        - `CHECK`-Constraints für Gehalt (> 0) und Stunden (BETWEEN 0 AND 40)
        - `DEFAULT`-Werte für Einstellungsdatum und Rolle
        - `UNIQUE`-Constraint für die Email-Adresse

        Testen Sie, dass die Constraints korrekt funktionieren.
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- ⭐⭐⭐ Schema mit CHECK und DEFAULT
        SELECT 'Ihre Lösung hier' AS Hinweis;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
CREATE TABLE IF NOT EXISTS Abteilung_Adv (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Mitarbeiter_Adv (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(200) UNIQUE,
    Gehalt DECIMAL(10,2) CHECK(Gehalt > 0),
    Einstellungsdatum DATE DEFAULT CURRENT_DATE,
    Abteilung_ID INTEGER,
    FOREIGN KEY (Abteilung_ID) REFERENCES Abteilung_Adv(ID)
);

CREATE TABLE IF NOT EXISTS Projekt (
    ID INTEGER PRIMARY KEY,
    Titel VARCHAR(200) NOT NULL,
    Budget DECIMAL(12,2) CHECK(Budget >= 0),
    Startdatum DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Mitarbeiter_Projekt (
    Mitarbeiter_ID INTEGER,
    Projekt_ID INTEGER,
    Rolle VARCHAR(50) DEFAULT 'Mitglied',
    Stunden_Pro_Woche INTEGER CHECK(Stunden_Pro_Woche BETWEEN 0 AND 40),
    PRIMARY KEY (Mitarbeiter_ID, Projekt_ID),
    FOREIGN KEY (Mitarbeiter_ID) REFERENCES Mitarbeiter_Adv(ID),
    FOREIGN KEY (Projekt_ID) REFERENCES Projekt(ID)
);

INSERT OR IGNORE INTO Abteilung_Adv VALUES (1, 'Entwicklung');
INSERT OR IGNORE INTO Mitarbeiter_Adv VALUES (1, 'Müller', 'mueller@firma.de', 65000, '2024-03-01', 1);
INSERT OR IGNORE INTO Projekt VALUES (1, 'DMA-Portal', 50000, '2026-01-01');
INSERT OR IGNORE INTO Mitarbeiter_Projekt VALUES (1, 1, 'Leitung', 20);

SELECT m.Name, p.Titel, mp.Rolle, mp.Stunden_Pro_Woche
FROM Mitarbeiter_Projekt mp
JOIN Mitarbeiter_Adv m ON mp.Mitarbeiter_ID = m.ID
JOIN Projekt p ON mp.Projekt_ID = p.ID;
```

**Constraints im Überblick:**
- `CHECK(Gehalt > 0)` — kein negatives Gehalt
- `CHECK(Stunden_Pro_Woche BETWEEN 0 AND 40)` — maximal Vollzeit
- `DEFAULT CURRENT_DATE` — automatisch heutiges Datum
- `DEFAULT 'Mitglied'` — Standard-Rolle bei neuer Zuordnung
- `UNIQUE` — keine doppelten Email-Adressen
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

        | ER-Element | Transformationsregel | SQL-Umsetzung |
        |------------|---------------------|---------------|
        | **Entität** | Eigene Tabelle | `CREATE TABLE` |
        | **Attribut** | Spalte | Spalte mit Datentyp |
        | **Schlüsselattribut** | Primärschlüssel | `PRIMARY KEY` |
        | **1:N-Beziehung** | FK auf N-Seite | `FOREIGN KEY ... REFERENCES` |
        | **M:N-Beziehung** | Beziehungstabelle | Tabelle mit 2 FKs + zusammengesetztem PK |
        | **1:1-Beziehung** | Zusammenlegen oder FK | FK mit `UNIQUE` |
        | **Beziehungsattribut** | Spalte in Beziehungstabelle | z.B. `Note`, `Menge` |

        **Wichtige Regeln:**
        1. Tabellen in der **richtigen Reihenfolge** erstellen (referenzierte Tabellen zuerst)
        2. Bei 1:N steht der FK immer auf der **N-Seite**
        3. Bei M:N braucht es eine **eigene Beziehungstabelle** mit zusammengesetztem PK
        4. `CHECK`- und `DEFAULT`-Constraints schützen die Datenqualität

        **Nächste Session:** Normalisierung (1NF, 2NF, 3NF)
        """
    )
    return


if __name__ == "__main__":
    app.run()
