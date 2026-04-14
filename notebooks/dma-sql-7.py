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
    app_title="DMA Session 7: Normalisierung — Übungen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 7: Normalisierung — Übungen

        Theorie und geführte Beispiele → **07-normalisierung-guide.py**

        **Aufgabentypen:**

        - 🟡 **Scaffolded**: Teillösung zum Ergänzen
        - 🔵 **Selbstständig**: Eigene Lösung schreiben
        - 🔴 **Debugging**: Fehler finden und beheben
        - ⭐ **Exploration**: Offene Herausforderungen
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Bestellung_Unnorm (
            Best_Nr INTEGER, Kunde VARCHAR(50), K_Stadt VARCHAR(50),
            Produkt VARCHAR(50), P_Preis DECIMAL(10,2), Menge INTEGER,
            PRIMARY KEY (Best_Nr, Produkt)
        );
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


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 2NF-Tabellen für spätere Aufgaben erstellen
        CREATE TABLE IF NOT EXISTS Bestellung_2NF (
            Best_Nr INTEGER PRIMARY KEY, Kunde VARCHAR(50), K_Stadt VARCHAR(50)
        );
        INSERT OR IGNORE INTO Bestellung_2NF
        SELECT DISTINCT Best_Nr, Kunde, K_Stadt FROM Bestellung_Unnorm;

        CREATE TABLE IF NOT EXISTS Produkt_2NF (
            Produkt VARCHAR(50) PRIMARY KEY, P_Preis DECIMAL(10,2)
        );
        INSERT OR IGNORE INTO Produkt_2NF
        SELECT DISTINCT Produkt, P_Preis FROM Bestellung_Unnorm;

        CREATE TABLE IF NOT EXISTS Best_Position_2NF (
            Best_Nr INTEGER, Produkt VARCHAR(50), Menge INTEGER,
            PRIMARY KEY (Best_Nr, Produkt)
        );
        INSERT OR IGNORE INTO Best_Position_2NF
        SELECT Best_Nr, Produkt, Menge FROM Bestellung_Unnorm;

        SELECT '2NF-Tabellen erstellt' AS Status;
        """
    )
    return


# -----------------------------------------------------------------------
# Phase 2: Funktionale Abhängigkeiten
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 2: Funktionale Abhängigkeiten
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 2.1: FD-Identifikation — Redundanz aufspüren

        Untersuchen Sie die unnormalisierte Tabelle auf Redundanz.
        Welche Daten werden mehrfach gespeichert?
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Wie oft kommt jede Kombination Kunde/K_Stadt vor?
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
        -- Wie oft kommt jede Kombination Produkt/P_Preis vor?
        SELECT Produkt, P_Preis, COUNT(*) AS Anzahl
        FROM Bestellung_Unnorm
        GROUP BY Produkt, P_Preis
        ORDER BY Anzahl DESC;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    armstrong_quiz = mo.ui.radio(
        options={
            "Matrikelnr → Stadt": "a_stadt",
            "Stadt → Name": "stadt_name",
            "Name → Matrikelnr": "name_matrikel",
            "Stadt → Matrikelnr": "stadt_matrikel",
        },
        label="**Quiz — Transitivität:** Gegeben: Matrikelnr → Student, Student → Stadt. Welche FD lässt sich per Transitivität ableiten?",
    )
    return (armstrong_quiz,)


@app.cell(hide_code=True)
def _(mo, armstrong_quiz):
    if armstrong_quiz.value == "a_stadt":
        _result = (
            mo.md(
                "✅ **Richtig!** Transitivität: Matrikelnr → Student und Student → Stadt ergibt **Matrikelnr → Stadt**."
            )
        )
    elif armstrong_quiz.value:
        _result = (
            mo.md(
                "❌ Nicht ganz. Bei der Transitivität gilt: Wenn A → B und B → C, dann A → C. Hier: Matrikelnr → Student → Stadt, also Matrikelnr → Stadt."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([armstrong_quiz, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    aug_quiz = mo.ui.radio(
        options={
            "ISBN, Verlag → Titel, Verlag": "correct",
            "Verlag → Titel": "wrong1",
            "Titel → ISBN, Verlag": "wrong2",
            "ISBN, Titel → Verlag": "wrong3",
        },
        label="**Quiz — Verstärkung:** Gegeben: ISBN → Titel. Welche FD folgt per Verstärkung (Augmentation) mit Verlag?",
    )
    return (aug_quiz,)


@app.cell(hide_code=True)
def _(mo, aug_quiz):
    if aug_quiz.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** Verstärkung: Wenn A → B, dann A,C → B,C. Also ISBN,Verlag → Titel,Verlag."
            )
        )
    elif aug_quiz.value:
        _result = (
            mo.md(
                "❌ Nicht ganz. Verstärkung fügt auf **beiden Seiten** das gleiche Attribut hinzu: ISBN → Titel wird zu ISBN,Verlag → Titel,Verlag."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([aug_quiz, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 2.2: Armstrong-Axiome anwenden (Scaffolded)

        Leiten Sie aus den gegebenen FDs die Abhängigkeit **A → D** ab.
        Ergänzen Sie die fehlenden Schritte:
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Gegeben: A → B, B → C, C → D
        -- Leiten Sie A → D ab.
        -- Schritt 1: A → B und B → C ergibt per Transitivität: A → ???
        -- Schritt 2: A → C und C → D ergibt per Transitivität: A → ???
        SELECT 'Leiten Sie A → D schrittweise ab' AS Aufgabe
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🔑 Musterlösung": mo.md(
                """
**Schritt 1:** A → B und B → C ⟹ **A → C** (Transitivität)

**Schritt 2:** A → C und C → D ⟹ **A → D** (Transitivität)

Die Transitivität kann beliebig oft hintereinander angewandt werden, um längere Abhängigkeitsketten abzuleiten.
"""
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.3: FDs identifizieren (Selbstständig)

        Gegeben: **Kurs(KursNr, Titel, DozentName, DozentBüro)**

        Identifizieren Sie alle funktionalen Abhängigkeiten in dieser Tabelle.

        *Hinweis: Welche Attribute bestimmen welche anderen? Gibt es transitive Abhängigkeiten?*
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung: Listen Sie alle FDs auf
        -- Tipp: KursNr bestimmt welche Attribute?
        --        DozentName bestimmt welche Attribute?
        SELECT 'Notieren Sie alle FDs als Kommentar' AS Aufgabe
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🔑 Musterlösung": mo.md(
                """
**Funktionale Abhängigkeiten:**

1. **KursNr → Titel** (Jeder Kurs hat genau einen Titel)
2. **KursNr → DozentName** (Jeder Kurs hat genau einen Dozenten)
3. **DozentName → DozentBüro** (Jeder Dozent hat genau ein Büro)
4. **KursNr → DozentBüro** (transitiv: KursNr → DozentName → DozentBüro)

Die transitive Abhängigkeit (4) zeigt: Diese Tabelle ist **nicht** in 3NF!
"""
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 2.4: Ungültige FD erkennen (Debugging)

        Ein Kollege behauptet: "Ort → PLZ ist eine gültige funktionale Abhängigkeit."
        Stimmt das? Begründen Sie anhand der Daten!
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 🔴 Ein Kollege behauptet: "Ort → PLZ ist eine gültige funktionale Abhängigkeit"
        -- Stimmt das? Begründen Sie!
        SELECT 'München' AS Ort, '80331' AS PLZ
        UNION ALL SELECT 'München', '80333'
        UNION ALL SELECT 'München', '80335'
        UNION ALL SELECT 'Berlin', '10115'
        UNION ALL SELECT 'Berlin', '10117'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🔑 Lösung": mo.md(
                """
**FALSCH!** Die Behauptung Ort → PLZ ist **ungültig**.

München hat **mehrere** PLZs (80331, 80333, 80335) — wenn Sie nur den Ort kennen, können Sie die PLZ **nicht** eindeutig bestimmen.

**Aber:** PLZ → Ort **ist** gültig! Jede PLZ gehört zu genau einem Ort (in Deutschland).

**Merke:** Eine FD A → B bedeutet: Jeder Wert von A ist mit **genau einem** Wert von B verknüpft. Wenn ein A-Wert mehrere B-Werte haben kann, gilt die FD nicht.
"""
            )
        }
    )
    return


# -----------------------------------------------------------------------
# Phase 4: 1NF und 2NF
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: 1NF und 2NF
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.1: 1NF verstehen — Nicht-atomare Werte

        Die folgende Tabelle verletzt die 1NF. Warum?
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS Student_Nicht1NF (
            Student VARCHAR(50) PRIMARY KEY,
            Kurse VARCHAR(200)
        );
        INSERT OR IGNORE INTO Student_Nicht1NF VALUES ('Anna', 'DMA, BWL, Statistik');
        INSERT OR IGNORE INTO Student_Nicht1NF VALUES ('Ben', 'DMA');
        INSERT OR IGNORE INTO Student_Nicht1NF VALUES ('Clara', 'BWL, Statistik');
        SELECT * FROM Student_Nicht1NF;
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 4.2: Zerlegung in 2NF (Scaffolded)

        Zerlegen Sie `Bestellung_Unnorm` in drei 2NF-Tabellen.
        Ergänzen Sie die fehlenden Teile (`???`):
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Zerlegen Sie Bestellung_Unnorm in 2NF (3 Tabellen)
        -- Tabelle 1: Bestellungen (Best_Nr ist PK)
        CREATE TABLE IF NOT EXISTS Bestellung_2NF_Ueb (
            Best_Nr INTEGER PRIMARY KEY,
            ??? VARCHAR(50),
            ??? VARCHAR(50)
        );
        -- Tipp: Welche Attribute hängen nur von Best_Nr ab?
        INSERT OR IGNORE INTO Bestellung_2NF_Ueb
        SELECT DISTINCT Best_Nr, Kunde, K_Stadt FROM Bestellung_Unnorm;
        SELECT * FROM Bestellung_2NF_Ueb ORDER BY Best_Nr;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🔑 Musterlösung — Alle 3 Tabellen": mo.md(
                """
**Tabelle 1: Bestellungen** (Best_Nr → Kunde, K_Stadt)
```sql
CREATE TABLE Bestellung_2NF (
    Best_Nr INTEGER PRIMARY KEY,
    Kunde VARCHAR(50),
    K_Stadt VARCHAR(50)
);
INSERT INTO Bestellung_2NF
SELECT DISTINCT Best_Nr, Kunde, K_Stadt FROM Bestellung_Unnorm;
```

**Tabelle 2: Produkte** (Produkt → P_Preis)
```sql
CREATE TABLE Produkt_2NF (
    Produkt VARCHAR(50) PRIMARY KEY,
    P_Preis DECIMAL(10,2)
);
INSERT INTO Produkt_2NF
SELECT DISTINCT Produkt, P_Preis FROM Bestellung_Unnorm;
```

**Tabelle 3: Bestellpositionen** ((Best_Nr, Produkt) → Menge)
```sql
CREATE TABLE Best_Position_2NF (
    Best_Nr INTEGER,
    Produkt VARCHAR(50),
    Menge INTEGER,
    PRIMARY KEY (Best_Nr, Produkt)
);
INSERT INTO Best_Position_2NF
SELECT Best_Nr, Produkt, Menge FROM Bestellung_Unnorm;
```

**Warum 2NF?** Jedes Nicht-Schlüsselattribut hängt jetzt voll funktional vom gesamten Primärschlüssel seiner Tabelle ab. Keine partiellen Abhängigkeiten mehr!
"""
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.3: Mitarbeiter-Tabelle normalisieren (Selbstständig)

        Gegeben: **Mitarbeiter(MitID, Name, ProjektNr, ProjektName, Stunden)**

        - PK ist **(MitID, ProjektNr)**
        - Name hängt nur von MitID ab
        - ProjektName hängt nur von ProjektNr ab
        - Stunden hängt vom gesamten Schlüssel ab

        Zerlegen Sie die Tabelle in 2NF.
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung: Zerlegen Sie in 3 Tabellen
        -- Tipp: Welche Attribute hängen von welchem Teil des Schlüssels ab?
        SELECT 'Schreiben Sie Ihre CREATE TABLE Statements' AS Aufgabe
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🔑 Musterlösung": mo.md(
                """
**Tabelle 1: Mitarbeiter** (MitID → Name)
```sql
CREATE TABLE Mitarbeiter (
    MitID INTEGER PRIMARY KEY,
    Name VARCHAR(50)
);
```

**Tabelle 2: Projekt** (ProjektNr → ProjektName)
```sql
CREATE TABLE Projekt (
    ProjektNr INTEGER PRIMARY KEY,
    ProjektName VARCHAR(100)
);
```

**Tabelle 3: Zuordnung** ((MitID, ProjektNr) → Stunden)
```sql
CREATE TABLE Zuordnung (
    MitID INTEGER,
    ProjektNr INTEGER,
    Stunden INTEGER,
    PRIMARY KEY (MitID, ProjektNr)
);
```

**Erklärung:** Name ist partiell abhängig (nur MitID), ProjektName ist partiell abhängig (nur ProjektNr). Nur Stunden hängt vom gesamten Schlüssel ab.
"""
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 4.4: Menge in der falschen Tabelle (Debugging)

        Ein Kollege hat die Menge in die Bestellungstabelle geschrieben.
        Warum ist das falsch?
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 🔴 Ein Kollege hat die Menge in die falsche Tabelle geschrieben!
        -- Warum gehört Menge NICHT in die Bestellung_2NF Tabelle?
        CREATE TABLE IF NOT EXISTS Bestellung_Falsch (
            Best_Nr INTEGER PRIMARY KEY,
            Kunde VARCHAR(50),
            K_Stadt VARCHAR(50),
            Menge INTEGER  -- <-- Gehört das hierhin?
        );
        SELECT 'Warum ist Menge hier falsch?' AS Frage;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🔑 Lösung": mo.md(
                """
**Problem:** Menge hängt von **(Best_Nr, Produkt)** ab — nicht nur von Best_Nr!

Bestellung 1001 enthält z.B.:
- Laptop: Menge **1**
- Maus: Menge **2**

Die Menge ist pro **Bestellposition** unterschiedlich. Wenn wir Menge nur mit Best_Nr speichern, verlieren wir die Information, welches Produkt welche Menge hat.

**Richtig:** Menge gehört in die Tabelle **Best_Position_2NF** mit dem zusammengesetzten Schlüssel (Best_Nr, Produkt).
"""
            )
        }
    )
    return


# -----------------------------------------------------------------------
# Phase 6: 3NF
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: 3NF
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.1: Von 2NF zu 3NF — Transitive Abhängigkeit beseitigen

        In Bestellung_2NF gilt: Best_Nr → Kunde → K_Stadt (transitiv!).
        Wir zerlegen in Kunde_3NF + Bestellung_3NF:
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Kundentabelle: Kunde → K_Stadt
        CREATE TABLE IF NOT EXISTS Kunde_3NF (
            Kunde VARCHAR(50) PRIMARY KEY,
            K_Stadt VARCHAR(50)
        );
        INSERT OR IGNORE INTO Kunde_3NF
        SELECT DISTINCT Kunde, K_Stadt FROM Bestellung_2NF;
        SELECT * FROM Kunde_3NF ORDER BY Kunde;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Bestellungstabelle: Best_Nr → Kunde (FK)
        CREATE TABLE IF NOT EXISTS Bestellung_3NF (
            Best_Nr INTEGER PRIMARY KEY,
            Kunde VARCHAR(50)
        );
        INSERT OR IGNORE INTO Bestellung_3NF
        SELECT Best_Nr, Kunde FROM Bestellung_2NF;
        SELECT * FROM Bestellung_3NF ORDER BY Best_Nr;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz1 = mo.ui.radio(
        options={
            "Verletzt 1NF (nicht atomare Werte)": "1nf",
            "Verletzt 2NF (partielle Abhängigkeit)": "2nf",
            "Verletzt 3NF (transitive Abhängigkeit)": "3nf",
            "Ist in 3NF (keine Verletzung)": "ok",
        },
        label="**Frage 1:** Mitarbeiter(MitID, Name, AbtID, AbtName) — was ist das Problem?",
    )
    return (quiz1,)


@app.cell(hide_code=True)
def _(mo, quiz1):
    if quiz1.value == "3nf":
        _result = (
            mo.md(
                "✅ **Richtig!** MitID → AbtID → AbtName ist eine transitive Abhängigkeit."
            )
        )
    elif quiz1.value:
        _result = (
            mo.md(
                "❌ Nicht ganz. Denken Sie an die Kette: MitID → AbtID → AbtName"
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([quiz1, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    quiz2 = mo.ui.radio(
        options={
            "Verletzt 1NF (nicht atomare Werte)": "1nf",
            "Verletzt 2NF (partielle Abhängigkeit)": "2nf",
            "Verletzt 3NF (transitive Abhängigkeit)": "3nf",
            "Ist in 3NF (keine Verletzung)": "ok",
        },
        label="**Frage 2:** Buch(ISBN, AutorID, Titel, AutorName) mit PK = (ISBN, AutorID) — was ist das Problem?",
    )
    return (quiz2,)


@app.cell(hide_code=True)
def _(mo, quiz2):
    if quiz2.value == "2nf":
        _result = (
            mo.md(
                "✅ **Richtig!** Titel hängt nur von ISBN ab (partiell), AutorName nur von AutorID (partiell)."
            )
        )
    elif quiz2.value:
        _result = (
            mo.md(
                "❌ Nicht ganz. Bei zusammengesetztem Schlüssel: Hängen alle Attribute vom *gesamten* Schlüssel ab?"
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([quiz2, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    quiz3 = mo.ui.radio(
        options={
            "Verletzt 1NF (nicht atomare Werte)": "1nf",
            "Verletzt 2NF (partielle Abhängigkeit)": "2nf",
            "Verletzt 3NF (transitive Abhängigkeit)": "3nf",
            "Ist in 3NF (keine Verletzung)": "ok",
        },
        label="**Frage 3:** Kurs(KursNr, Titel, DozentName, DozentBüro) mit KursNr → Titel, KursNr → DozentName, DozentName → DozentBüro",
    )
    return (quiz3,)


@app.cell(hide_code=True)
def _(mo, quiz3):
    if quiz3.value == "3nf":
        _result = (
            mo.md(
                "✅ **Richtig!** KursNr → DozentName → DozentBüro ist eine transitive Abhängigkeit. DozentBüro hängt über DozentName indirekt vom Schlüssel ab."
            )
        )
    elif quiz3.value:
        _result = (
            mo.md(
                "❌ Nicht ganz. Schauen Sie auf die Kette: KursNr → DozentName → DozentBüro. Das DozentBüro hängt nicht direkt vom Schlüssel ab."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([quiz3, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 6.2: Kunde_3NF erstellen und verlustfreie Zerlegung prüfen (Scaffolded)

        Erstellen Sie eine eigene Kundentabelle und prüfen Sie, ob die Zerlegung verlustfrei ist.
        Ergänzen Sie die fehlenden Teile (`???`):
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Erstellen Sie Kunde_3NF und prüfen Sie die verlustfreie Zerlegung
        CREATE TABLE IF NOT EXISTS Kunde_3NF_Ueb (
            Kunde VARCHAR(50) PRIMARY KEY,
            ??? VARCHAR(50)
        );
        INSERT OR IGNORE INTO Kunde_3NF_Ueb
        SELECT DISTINCT ???, ???
        FROM Bestellung_2NF;
        -- Tipp: Kunde, K_Stadt
        SELECT * FROM Kunde_3NF_Ueb ORDER BY Kunde;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🔑 Musterlösung": mo.md(
                """
```sql
CREATE TABLE IF NOT EXISTS Kunde_3NF_Ueb (
    Kunde VARCHAR(50) PRIMARY KEY,
    K_Stadt VARCHAR(50)
);
INSERT OR IGNORE INTO Kunde_3NF_Ueb
SELECT DISTINCT Kunde, K_Stadt
FROM Bestellung_2NF;
SELECT * FROM Kunde_3NF_Ueb ORDER BY Kunde;
```

**Ergebnis:** 3 Zeilen (Müller/München, Schmidt/Berlin, Weber/Hamburg) — jede Kombination steht nur einmal. Die transitive Abhängigkeit Best_Nr → Kunde → K_Stadt ist beseitigt.
"""
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.3: Buchungstabelle normalisieren (Selbstständig)

        Gegeben: **Buchung(BuchungsNr, Gast, GastStadt, Hotel, HotelStadt, Preis)**

        FDs:
        - BuchungsNr → Gast
        - Gast → GastStadt
        - BuchungsNr → Hotel
        - Hotel → HotelStadt
        - BuchungsNr → Preis

        Normalisieren Sie diese Tabelle in **3NF**.
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung: Zerlegen Sie in 3NF-Tabellen
        -- Tipp: Welche transitiven Abhängigkeiten gibt es?
        -- BuchungsNr → Gast → GastStadt
        -- BuchungsNr → Hotel → HotelStadt
        SELECT 'Schreiben Sie Ihre CREATE TABLE Statements' AS Aufgabe
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🔑 Musterlösung": mo.md(
                """
**Tabelle 1: Gast** (Gast → GastStadt)
```sql
CREATE TABLE Gast (
    Gast VARCHAR(50) PRIMARY KEY,
    GastStadt VARCHAR(50)
);
```

**Tabelle 2: Hotel** (Hotel → HotelStadt)
```sql
CREATE TABLE Hotel (
    Hotel VARCHAR(50) PRIMARY KEY,
    HotelStadt VARCHAR(50)
);
```

**Tabelle 3: Buchung** (BuchungsNr → Gast, Hotel, Preis)
```sql
CREATE TABLE Buchung (
    BuchungsNr INTEGER PRIMARY KEY,
    Gast VARCHAR(50),
    Hotel VARCHAR(50),
    Preis DECIMAL(10,2)
);
```

**Erklärung:** Die transitiven Abhängigkeiten BuchungsNr → Gast → GastStadt und BuchungsNr → Hotel → HotelStadt werden durch Auslagern in eigene Tabellen beseitigt.
"""
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.4: Ist diese Tabelle wirklich in 3NF? (Debugging)

        Ein Kollege behauptet, die folgende Tabelle sei in 3NF. Stimmt das?
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        -- 🔴 Ist diese Tabelle wirklich in 3NF?
        -- Kurs(KursNr, Titel, DozentName, DozentBüro)
        -- FDs: KursNr → Titel, KursNr → DozentName, DozentName → DozentBüro

        SELECT 'KursNr → DozentName → DozentBüro: Transitive Abhängigkeit!' AS Problem;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🔑 Lösung": mo.md(
                """
**NEIN, die Tabelle ist NICHT in 3NF!**

**Problem:** DozentBüro hängt transitiv vom Schlüssel ab:
- KursNr → DozentName (direkt)
- DozentName → DozentBüro (direkt)
- Also: KursNr → DozentName → DozentBüro (**transitiv!**)

**Lösung — Zerlegung in 3NF:**
```sql
-- Tabelle 1: Kurs (ohne DozentBüro)
CREATE TABLE Kurs (
    KursNr INTEGER PRIMARY KEY,
    Titel VARCHAR(100),
    DozentName VARCHAR(50)
);

-- Tabelle 2: Dozent
CREATE TABLE Dozent (
    DozentName VARCHAR(50) PRIMARY KEY,
    DozentBüro VARCHAR(20)
);
```

Jetzt hängt jedes Nicht-Schlüsselattribut direkt und nicht-transitiv vom Primärschlüssel ab.
"""
            )
        }
    )
    return


# -----------------------------------------------------------------------
# Exploration
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Exploration

        Offene Herausforderungen für Fortgeschrittene.

        **Tipp:** Diskutieren Sie mit Ihrem Nachbarn — besonders bei Normalisierungsentscheidungen gibt es Abwägungen, die vom Kontext abhängen!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Exploration 1: Verlustfreie Zerlegung per JOIN verifizieren

        Prüfen Sie, ob der JOIN aller 3NF-Tabellen exakt die Originaldaten reproduziert.
        Vergleichen Sie die Zeilenanzahl.
        """
    )
    return


@app.cell
def _(mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Vergleichen Sie Original und Rekonstruktion
        -- Tipp: JOIN über Bestellung_3NF, Kunde_3NF, Best_Position_2NF, Produkt_2NF
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS Hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🔑 Musterlösung": mo.md(
                """
```sql
-- Originalanzahl
SELECT COUNT(*) AS Original_Zeilen FROM Bestellung_Unnorm;

-- Rekonstruktion durch JOIN der 3NF-Tabellen
SELECT COUNT(*) AS Rekonstruierte_Zeilen
FROM Bestellung_3NF b
JOIN Kunde_3NF k ON b.Kunde = k.Kunde
JOIN Best_Position_2NF bp ON b.Best_Nr = bp.Best_Nr
JOIN Produkt_2NF p ON bp.Produkt = p.Produkt;
```

**Beide Zählungen ergeben 6!** Das beweist: Die Normalisierung war **verlustfrei** — keine Information ging beim Aufteilen verloren.
"""
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐ Exploration 2: Film-Tabelle normalisieren

        Gegeben: **Film(FilmID, Titel, RegisseurName, RegisseurLand, Hauptdarsteller, DarstellerNationalität)**

        FDs:
        - FilmID → Titel, RegisseurName, Hauptdarsteller
        - RegisseurName → RegisseurLand
        - Hauptdarsteller → DarstellerNationalität

        Normalisieren Sie in 3NF.
        """
    )
    return


@app.cell
def _(mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Normalisieren Sie die Film-Tabelle in 3NF
        -- Tipp: Identifizieren Sie die transitiven Abhängigkeiten
        SELECT 'Schreiben Sie Ihre Lösung hier' AS Hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "🔑 Musterlösung": mo.md(
                """
**Transitive Abhängigkeiten:**
- FilmID → RegisseurName → RegisseurLand
- FilmID → Hauptdarsteller → DarstellerNationalität

**Zerlegung in 3NF:**

```sql
-- Tabelle 1: Regisseur
CREATE TABLE Regisseur (
    RegisseurName VARCHAR(50) PRIMARY KEY,
    RegisseurLand VARCHAR(50)
);

-- Tabelle 2: Darsteller
CREATE TABLE Darsteller (
    Hauptdarsteller VARCHAR(50) PRIMARY KEY,
    DarstellerNationalität VARCHAR(50)
);

-- Tabelle 3: Film (ohne Land/Nationalität)
CREATE TABLE Film (
    FilmID INTEGER PRIMARY KEY,
    Titel VARCHAR(100),
    RegisseurName VARCHAR(50),
    Hauptdarsteller VARCHAR(50)
);
```

**Ergebnis:** Drei Tabellen ohne transitive Abhängigkeiten. RegisseurLand und DarstellerNationalität stehen jeweils nur einmal pro Regisseur bzw. Darsteller.
"""
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐⭐ Exploration 3: Wann macht Denormalisierung Sinn?

        Erstellen Sie einen denormalisierten View, der alle 3NF-Tabellen zusammenführt.
        Vergleichen Sie die Komplexität der Abfragen mit und ohne View.
        """
    )
    return


@app.cell
def _(mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Erstellen Sie einen denormalisierten View
        -- Tipp: CREATE OR REPLACE VIEW bestellung_komplett AS SELECT ... JOIN ...
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS Hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## 🎓 Übungsklausur: Relationales Modell & Normalisierung

        Hier ist eine typische Aufgabe aus der Klausur.

        Gegeben sei folgende Tabelle zur Projektverwaltung:

        | ProjektID | Projektname | Projektleiter | EntwicklerID | Entwickler | Aufgabe |
        |---|---|---|---|---|---|
        | 101 | Projekt A | Dr. Schmidt | 001 | Max Müller | Frontend |
        | 101 | Projekt A | Dr. Schmidt | 002 | Julia Fischer | KI |
        | 102 | Projekt B | Dr. Meier | 003 | Anna Schmidt | Datenbank |
        | 102 | Projekt B | Dr. Meier | 001 | Max Müller | Datenbank |
        | 102 | Projekt B | Dr. Meier | 002 | Julia Fischer | KI |

        **Aufgabe:**
        1. Identifizieren Sie **Redundanzen** in der Tabelle.
        2. Zerlegen Sie die Tabelle in die **3. Normalform**. Geben Sie die Schemata der resultierenden Tabellen an (unterstrichene Primärschlüssel).
        """
    )
    return


@app.cell
def _(mo):
    # Tragen Sie Ihre Analyse hier ein
    mo.md(
        """
        **Ihre Antwort:**

        1. Redundanzen:
           - ...

        2. Zerlegung in 3NF:
           - Tabelle 1: ...
           - Tabelle 2: ...
           - ...
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**1. Redundanzen:**
- **Projekt-Daten:** `Projektname` ("Projekt A") und `Projektleiter` ("Dr. Schmidt") werden für jeden Entwickler im Projekt wiederholt.
- **Entwickler-Daten:** `Entwickler` (Name "Max Müller") wird wiederholt, wenn er in mehreren Projekten arbeitet.

**2. Zerlegung in 3NF:**

Wir trennen die funktionalen Abhängigkeiten:
- ProjektID → Projektname, Projektleiter
- EntwicklerID → Entwickler
- (ProjektID, EntwicklerID) → Aufgabe

**Tabelle: Projekte**
- Schema: <u>ProjektID</u>, Projektname, Projektleiter

**Tabelle: Entwickler**
- Schema: <u>EntwicklerID</u>, Name

**Tabelle: Projekt_Zuweisung**
- Schema: <u>ProjektID, EntwicklerID</u>, Aufgabe
- Fremdschlüssel: ProjektID referenziert Projekte, EntwicklerID referenziert Entwickler

Damit sind alle Attribute voll funktional vom jeweiligen Primärschlüssel abhängig und transitive Abhängigkeiten sind eliminiert.
""")})
    return


# -----------------------------------------------------------------------
# Zusammenfassung
# -----------------------------------------------------------------------


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

        **Merksatz:** *"Jedes Attribut hängt vom Schlüssel ab, vom ganzen Schlüssel, und von nichts außer dem Schlüssel."*

        **Nächste Session:** JOINs — die normalisierten Tabellen wieder zusammenführen!
        """
    )
    return


if __name__ == "__main__":
    app.run()
