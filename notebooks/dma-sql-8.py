import marimo

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 8: Normalisierung",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 8: Normalisierung

        In dieser Session lernen Sie:

        - **Funktionale Abhängigkeiten** erkennen
        - **1NF**: Atomare Werte
        - **2NF**: Volle funktionale Abhängigkeit
        - **3NF**: Keine transitiven Abhängigkeiten
        - Tabellen **normalisieren**

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Rückblick: Warum Normalisierung?

        In Session 5 haben wir **Anomalien** gesehen:

        | Anomalie | Problem |
        |----------|---------|
        | **Änderung** | Inkonsistenz bei Updates |
        | **Einfügung** | Kann Daten nicht einfügen |
        | **Löschung** | Verliert ungewollt Daten |

        **Ursache:** Redundanz durch schlechtes Tabellendesign

        **Lösung:** Systematische **Normalisierung** nach definierten Regeln

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Funktionale Abhängigkeit (FD)

        **Definition:** A → B bedeutet: "Wenn ich A kenne, kenne ich auch B"

        **Beispiele:**

        | FD | Gültig? | Erklärung |
        |----|---------|-----------|
        | Matrikelnr → Name | ✅ | Jede Matrikelnr gehört zu genau einem Namen |
        | PLZ → Ort | ✅ | Jede PLZ gehört zu einem Ort (in DE) |
        | Ort → PLZ | ❌ | München hat viele PLZs |
        | ISBN → Titel | ✅ | Jede ISBN identifiziert ein Buch |

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Aufgabe 8.1: Unnormalisierte Tabelle analysieren

        Wir erstellen eine unnormalisierte Bestelltabelle und identifizieren die Probleme.
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Unnormalisierte Bestelltabelle
        CREATE TABLE IF NOT EXISTS Bestellung_Unnorm (
            Best_Nr INTEGER,
            Kunde VARCHAR(50),
            K_Stadt VARCHAR(50),
            Produkt VARCHAR(50),
            P_Preis DECIMAL(10,2),
            Menge INTEGER,
            PRIMARY KEY (Best_Nr, Produkt)
        );

        -- Beispieldaten mit Redundanz
        INSERT OR IGNORE INTO Bestellung_Unnorm VALUES (1001, 'Müller', 'München', 'Laptop', 999.00, 1);
        INSERT OR IGNORE INTO Bestellung_Unnorm VALUES (1001, 'Müller', 'München', 'Maus', 29.00, 2);
        INSERT OR IGNORE INTO Bestellung_Unnorm VALUES (1002, 'Schmidt', 'Berlin', 'Laptop', 999.00, 1);
        INSERT OR IGNORE INTO Bestellung_Unnorm VALUES (1003, 'Müller', 'München', 'Tastatur', 79.00, 1);
        INSERT OR IGNORE INTO Bestellung_Unnorm VALUES (1004, 'Weber', 'Hamburg', 'Maus', 29.00, 3);
        INSERT OR IGNORE INTO Bestellung_Unnorm VALUES (1004, 'Weber', 'Hamburg', 'Laptop', 999.00, 1);

        SELECT * FROM Bestellung_Unnorm ORDER BY Best_Nr, Produkt;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Redundanz identifizieren

        **Frage:** Welche Daten sind redundant gespeichert?
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Wie oft kommt jeder Kunde vor?
        SELECT Kunde, K_Stadt, COUNT(*) AS Anzahl
        FROM Bestellung_Unnorm
        GROUP BY Kunde, K_Stadt
        ORDER BY Anzahl DESC;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Wie oft kommt jedes Produkt mit Preis vor?
        SELECT Produkt, P_Preis, COUNT(*) AS Anzahl
        FROM Bestellung_Unnorm
        GROUP BY Produkt, P_Preis
        ORDER BY Anzahl DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:**
        - "Müller, München" steht **3x** in der Tabelle
        - "Laptop, 999" steht **3x** in der Tabelle
        - "Maus, 29" steht **2x** in der Tabelle

        Das ist **Redundanz** - die Ursache für Anomalien!

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Aufgabe 8.2: Erste Normalform (1NF)

        **Regel:** Alle Attributwerte müssen **atomar** sein (keine Listen, keine Wiederholungsgruppen).
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- NICHT in 1NF: Liste von Kursen in einer Zelle
        CREATE TABLE IF NOT EXISTS Student_Nicht1NF (
            Student VARCHAR(50) PRIMARY KEY,
            Kurse VARCHAR(200)  -- Komma-separierte Liste!
        );

        INSERT OR IGNORE INTO Student_Nicht1NF VALUES ('Anna', 'DMA, BWL, Statistik');
        INSERT OR IGNORE INTO Student_Nicht1NF VALUES ('Ben', 'DMA');
        INSERT OR IGNORE INTO Student_Nicht1NF VALUES ('Clara', 'BWL, Statistik');

        SELECT * FROM Student_Nicht1NF;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Problem:** Wie finden wir alle Studenten, die "BWL" belegen?

        ```sql
        -- Das funktioniert NICHT zuverlässig:
        SELECT * FROM Student_Nicht1NF WHERE Kurse LIKE '%BWL%';
        ```

        **Lösung:** In 1NF überführen - jeder Kurs in eigener Zeile:
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- IN 1NF: Jede Zelle enthält genau einen Wert
        CREATE TABLE IF NOT EXISTS Student_Kurs_1NF (
            Student VARCHAR(50),
            Kurs VARCHAR(50),
            PRIMARY KEY (Student, Kurs)
        );

        INSERT OR IGNORE INTO Student_Kurs_1NF VALUES ('Anna', 'DMA');
        INSERT OR IGNORE INTO Student_Kurs_1NF VALUES ('Anna', 'BWL');
        INSERT OR IGNORE INTO Student_Kurs_1NF VALUES ('Anna', 'Statistik');
        INSERT OR IGNORE INTO Student_Kurs_1NF VALUES ('Ben', 'DMA');
        INSERT OR IGNORE INTO Student_Kurs_1NF VALUES ('Clara', 'BWL');
        INSERT OR IGNORE INTO Student_Kurs_1NF VALUES ('Clara', 'Statistik');

        SELECT * FROM Student_Kurs_1NF ORDER BY Student, Kurs;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Jetzt funktioniert die Abfrage!
        SELECT Student FROM Student_Kurs_1NF WHERE Kurs = 'BWL';
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Aufgabe 8.3: Zweite Normalform (2NF)

        **Regel:** Jedes Nicht-Schlüsselattribut muss **voll funktional abhängig** vom **gesamten** Primärschlüssel sein.

        **Problem in unserer Bestelltabelle:**

        - Primärschlüssel: (Best_Nr, Produkt)
        - Aber: `Kunde` hängt nur von `Best_Nr` ab, nicht von `Produkt`!
        - Und: `P_Preis` hängt nur von `Produkt` ab, nicht von `Best_Nr`!

        Das sind **partielle Abhängigkeiten** → verletzt 2NF
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Zerlegung in 2NF

        Wir zerlegen die Tabelle so, dass partielle Abhängigkeiten verschwinden:
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Tabelle 1: Bestellungen (Best_Nr → Kunde, K_Stadt)
        CREATE TABLE IF NOT EXISTS Bestellung_2NF (
            Best_Nr INTEGER PRIMARY KEY,
            Kunde VARCHAR(50),
            K_Stadt VARCHAR(50)
        );

        INSERT OR IGNORE INTO Bestellung_2NF
        SELECT DISTINCT Best_Nr, Kunde, K_Stadt
        FROM Bestellung_Unnorm;

        SELECT * FROM Bestellung_2NF ORDER BY Best_Nr;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Tabelle 2: Produkte (Produkt → P_Preis)
        CREATE TABLE IF NOT EXISTS Produkt_2NF (
            Produkt VARCHAR(50) PRIMARY KEY,
            P_Preis DECIMAL(10,2)
        );

        INSERT OR IGNORE INTO Produkt_2NF
        SELECT DISTINCT Produkt, P_Preis
        FROM Bestellung_Unnorm;

        SELECT * FROM Produkt_2NF ORDER BY Produkt;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Tabelle 3: Bestellpositionen (Best_Nr, Produkt → Menge)
        CREATE TABLE IF NOT EXISTS Best_Position_2NF (
            Best_Nr INTEGER,
            Produkt VARCHAR(50),
            Menge INTEGER,
            PRIMARY KEY (Best_Nr, Produkt)
        );

        INSERT OR IGNORE INTO Best_Position_2NF
        SELECT Best_Nr, Produkt, Menge
        FROM Bestellung_Unnorm;

        SELECT * FROM Best_Position_2NF ORDER BY Best_Nr, Produkt;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Ergebnis:** 3 Tabellen statt 1, aber **weniger Redundanz**!

        - Laptop-Preis steht nur noch **1x** (in Produkt_2NF)
        - Aber: Müller/München steht noch **2x** (in Bestellung_2NF)

        → Wir brauchen noch **3NF**!

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Aufgabe 8.4: Dritte Normalform (3NF)

        **Regel:** Keine **transitiven Abhängigkeiten** - kein Nicht-Schlüsselattribut darf von einem anderen Nicht-Schlüsselattribut abhängen.

        **Problem in Bestellung_2NF:**

        - Best_Nr → Kunde (OK)
        - Kunde → K_Stadt (Kunde bestimmt Stadt)
        - Also: Best_Nr → Kunde → K_Stadt (**transitiv!**)

        **Lösung:** Kunde in eigene Tabelle auslagern.
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Tabelle: Kunden (Kunde → K_Stadt)
        CREATE TABLE IF NOT EXISTS Kunde_3NF (
            Kunde VARCHAR(50) PRIMARY KEY,
            K_Stadt VARCHAR(50)
        );

        INSERT OR IGNORE INTO Kunde_3NF
        SELECT DISTINCT Kunde, K_Stadt
        FROM Bestellung_2NF;

        SELECT * FROM Kunde_3NF ORDER BY Kunde;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Tabelle: Bestellungen (nur Best_Nr → Kunde als FK)
        CREATE TABLE IF NOT EXISTS Bestellung_3NF (
            Best_Nr INTEGER PRIMARY KEY,
            Kunde VARCHAR(50)
        );

        INSERT OR IGNORE INTO Bestellung_3NF
        SELECT Best_Nr, Kunde
        FROM Bestellung_2NF;

        SELECT * FROM Bestellung_3NF ORDER BY Best_Nr;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Finale Struktur in 3NF

        Aus **1 Tabelle** wurden **4 Tabellen**:

        | Tabelle | Inhalt | Primärschlüssel |
        |---------|--------|-----------------|
        | Kunde_3NF | Kundenstammdaten | Kunde |
        | Bestellung_3NF | Bestellkopf | Best_Nr |
        | Produkt_2NF | Produktstammdaten | Produkt |
        | Best_Position_2NF | Bestellpositionen | (Best_Nr, Produkt) |

        **Keine Redundanz mehr!** Jede Information steht genau einmal.
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Überprüfung: Alle Daten sind noch da!
        SELECT
            b.Best_Nr,
            k.Kunde,
            k.K_Stadt,
            p.Produkt,
            p.P_Preis,
            bp.Menge
        FROM Bestellung_3NF b
        JOIN Kunde_3NF k ON b.Kunde = k.Kunde
        JOIN Best_Position_2NF bp ON b.Best_Nr = bp.Best_Nr
        JOIN Produkt_2NF p ON bp.Produkt = p.Produkt
        ORDER BY b.Best_Nr, p.Produkt;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Quiz: Normalformen bestimmen

        Testen Sie Ihr Verständnis!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz1 = mo.ui.radio(
        options={
            "1nf": "Verletzt 1NF (nicht atomare Werte)",
            "2nf": "Verletzt 2NF (partielle Abhängigkeit)",
            "3nf": "Verletzt 3NF (transitive Abhängigkeit)",
            "ok": "Ist in 3NF (keine Verletzung)"
        },
        label="**Frage 1:** Mitarbeiter(\\underline{MitID}, Name, AbtID, AbtName) - was ist das Problem?"
    )
    quiz1
    return (quiz1,)


@app.cell(hide_code=True)
def _(mo, quiz1):
    if quiz1.value == "3nf":
        mo.output.replace(mo.md("✅ **Richtig!** MitID → AbtID → AbtName ist eine transitive Abhängigkeit."))
    elif quiz1.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Denken Sie an die Kette: MitID → AbtID → AbtName"))
    return


@app.cell(hide_code=True)
def _(mo):
    quiz2 = mo.ui.radio(
        options={
            "1nf": "Verletzt 1NF (nicht atomare Werte)",
            "2nf": "Verletzt 2NF (partielle Abhängigkeit)",
            "3nf": "Verletzt 3NF (transitive Abhängigkeit)",
            "ok": "Ist in 3NF (keine Verletzung)"
        },
        label="**Frage 2:** Buch(\\underline{ISBN, AutorID}, Titel, AutorName) - was ist das Problem?"
    )
    quiz2
    return (quiz2,)


@app.cell(hide_code=True)
def _(mo, quiz2):
    if quiz2.value == "2nf":
        mo.output.replace(mo.md("✅ **Richtig!** Titel hängt nur von ISBN ab (partiell), AutorName nur von AutorID (partiell)."))
    elif quiz2.value:
        mo.output.replace(mo.md("❌ Nicht ganz. Bei zusammengesetztem Schlüssel: Hängen alle Attribute vom *gesamten* Schlüssel ab?"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration

        Experimentieren Sie mit eigenen Beispielen!

        **Ideen:**
        - Erstellen Sie eine unnormalisierte Tabelle
        - Identifizieren Sie die funktionalen Abhängigkeiten
        - Normalisieren Sie schrittweise zu 3NF
        """
    )
    return


@app.cell
def _(mo):
    # Ihre Abfrage hier:
    _df = mo.sql(
        f"""
        -- Beispiel: Zeige alle Tabellen
        SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Normalform | Regel | Lösung |
        |------------|-------|--------|
        | **1NF** | Atomare Werte | Listen auflösen |
        | **2NF** | Volle Abhängigkeit vom Schlüssel | Partielle Abhängigkeiten auslagern |
        | **3NF** | Keine transitiven Abhängigkeiten | Transitive Abhängigkeiten auslagern |

        **Merksatz:** "Jedes Attribut hängt vom Schlüssel ab, vom ganzen Schlüssel, und von nichts außer dem Schlüssel."

        **Nächste Session:** Joins - die normalisierten Tabellen wieder zusammenführen!
        """
    )
    return


if __name__ == "__main__":
    app.run()
